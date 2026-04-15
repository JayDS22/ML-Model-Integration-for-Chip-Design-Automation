import struct
import logging
from typing import Dict, List, Tuple, Any
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GDSIIParser:
    """Parser for GDSII binary layout files"""
    
    HEADER = 0x0002
    BGNLIB = 0x0102
    LIBNAME = 0x0206
    UNITS = 0x0305
    ENDLIB = 0x0400
    BGNSTR = 0x0502
    STRNAME = 0x0606
    ENDSTR = 0x0700
    BOUNDARY = 0x0800
    PATH = 0x0900
    LAYER = 0x0D02
    DATATYPE = 0x0E02
    XY = 0x1003
    ENDEL = 0x1100
    
    def __init__(self):
        self.current_position = 0
        self.library_name = ""
        self.units = (1e-9, 1e-3)
        self.cells = []
        self.layers = set()
        
    def parse(self, filepath: str) -> Dict[str, Any]:
        logger.info(f"Parsing GDSII file: {filepath}")
        
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
                
            self.current_position = 0
            self._parse_library(data)
            
            result = {
                'library_name': self.library_name,
                'units': self.units,
                'cells': self.cells,
                'layers': sorted(list(self.layers)),
                'num_cells': len(self.cells),
                'num_layers': len(self.layers)
            }
            
            logger.info(f"Parsed {len(self.cells)} cells with {len(self.layers)} layers")
            return result
            
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
    
    def _read_record(self, data: bytes) -> Tuple[int, int, bytes]:
        if self.current_position + 4 > len(data):
            return None, None, None
            
        record_size = struct.unpack('>H', data[self.current_position:self.current_position+2])[0]
        record_type = struct.unpack('>H', data[self.current_position+2:self.current_position+4])[0]
        
        if record_size < 4:
            return None, None, None
            
        record_data = data[self.current_position+4:self.current_position+record_size]
        self.current_position += record_size
        
        return record_size, record_type, record_data
    
    def _parse_library(self, data: bytes):
        while self.current_position < len(data):
            size, rec_type, rec_data = self._read_record(data)
            
            if rec_type is None:
                break
                
            if rec_type == self.LIBNAME:
                self.library_name = rec_data.decode('ascii').rstrip('\x00')
                
            elif rec_type == self.UNITS:
                if len(rec_data) >= 16:
                    self.units = struct.unpack('>dd', rec_data[:16])
                    
            elif rec_type == self.BGNSTR:
                cell = self._parse_structure(data)
                if cell:
                    self.cells.append(cell)
                    
            elif rec_type == self.ENDLIB:
                break
    
    def _parse_structure(self, data: bytes) -> Dict[str, Any]:
        cell = {
            'name': '',
            'elements': [],
            'layers': set()
        }
        
        while self.current_position < len(data):
            size, rec_type, rec_data = self._read_record(data)
            
            if rec_type is None:
                break
                
            if rec_type == self.STRNAME:
                cell['name'] = rec_data.decode('ascii').rstrip('\x00')
                
            elif rec_type in [self.BOUNDARY, self.PATH]:
                element = self._parse_element(data, rec_type)
                if element:
                    cell['elements'].append(element)
                    if 'layer' in element:
                        cell['layers'].add(element['layer'])
                        self.layers.add(element['layer'])
                        
            elif rec_type == self.ENDSTR:
                cell['layers'] = sorted(list(cell['layers']))
                return cell
        
        return cell
    
    def _parse_element(self, data: bytes, element_type: int) -> Dict[str, Any]:
        element = {
            'type': 'boundary' if element_type == self.BOUNDARY else 'path',
            'layer': 0,
            'datatype': 0,
            'xy': []
        }
        
        while self.current_position < len(data):
            size, rec_type, rec_data = self._read_record(data)
            
            if rec_type is None:
                break
                
            if rec_type == self.LAYER:
                element['layer'] = struct.unpack('>h', rec_data)[0]
                
            elif rec_type == self.DATATYPE:
                element['datatype'] = struct.unpack('>h', rec_data)[0]
                
            elif rec_type == self.XY:
                num_coords = len(rec_data) // 4
                coords = struct.unpack(f'>{num_coords}i', rec_data)
                element['xy'] = [(coords[i], coords[i+1]) for i in range(0, len(coords), 2)]
                
            elif rec_type == self.ENDEL:
                return element
        
        return element
    
    def extract_features(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        features = {
            'total_elements': sum(len(cell['elements']) for cell in parsed_data['cells']),
            'num_layers': parsed_data['num_layers'],
            'num_cells': parsed_data['num_cells'],
            'layer_distribution': {},
            'design_complexity': 0.0
        }
        
        for cell in parsed_data['cells']:
            for element in cell['elements']:
                layer = element.get('layer', 0)
                features['layer_distribution'][layer] = features['layer_distribution'].get(layer, 0) + 1
        
        features['design_complexity'] = (
            features['total_elements'] * 0.4 +
            features['num_layers'] * 100 +
            features['num_cells'] * 50
        )
        
        return features