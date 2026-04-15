import re
import logging
from typing import Dict, List, Any
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VerilogParser:
    """Parser for Verilog HDL files"""
    
    def __init__(self):
        self.modules = []
        self.current_module = None
        
        self.module_pattern = re.compile(r'module\s+(\w+)\s*(?:\#\([^)]*\))?\s*\((.*?)\);', re.DOTALL)
        self.port_pattern = re.compile(r'(input|output|inout)\s+(?:\[([^]]+)\])?\s*(\w+(?:\s*,\s*\w+)*)')
        self.wire_pattern = re.compile(r'(wire|reg)\s+(?:\[([^]]+)\])?\s*(\w+(?:\s*,\s*\w+)*)')
        self.instance_pattern = re.compile(r'(\w+)\s+(?:\#\([^)]*\))?\s*(\w+)\s*\((.*?)\);', re.DOTALL)
        
    def parse(self, filepath: str) -> List[Dict[str, Any]]:
        logger.info(f"Parsing Verilog file: {filepath}")
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            content = self._remove_comments(content)
            self.modules = []
            self._parse_modules(content)
            
            logger.info(f"Parsed {len(self.modules)} modules")
            return self.modules
            
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
    
    def _remove_comments(self, content: str) -> str:
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        return content
    
    def _parse_modules(self, content: str):
        lines = content.split('\n')
        in_module = False
        module_content = []
        
        for line in lines:
            if 'module' in line and not in_module:
                in_module = True
                module_content = [line]
            elif in_module:
                module_content.append(line)
                if 'endmodule' in line:
                    module_text = '\n'.join(module_content)
                    module = self._parse_single_module(module_text)
                    if module:
                        self.modules.append(module)
                    in_module = False
                    module_content = []
    
    def _parse_single_module(self, module_text: str) -> Dict[str, Any]:
        module = {
            'name': '',
            'ports': [],
            'wires': [],
            'instances': [],
            'io_summary': {'input': 0, 'output': 0, 'inout': 0}
        }
        
        module_match = self.module_pattern.search(module_text)
        if not module_match:
            return None
            
        module['name'] = module_match.group(1)
        
        for match in self.port_pattern.finditer(module_text):
            direction = match.group(1)
            width = match.group(2) if match.group(2) else '0:0'
            names = [n.strip() for n in match.group(3).split(',')]
            
            for name in names:
                port = {
                    'direction': direction,
                    'width': width,
                    'name': name
                }
                module['ports'].append(port)
                module['io_summary'][direction] += 1
        
        for match in self.wire_pattern.finditer(module_text):
            wire_type = match.group(1)
            width = match.group(2) if match.group(2) else '0:0'
            names = [n.strip() for n in match.group(3).split(',')]
            
            for name in names:
                wire = {
                    'type': wire_type,
                    'width': width,
                    'name': name
                }
                module['wires'].append(wire)
        
        return module
    
    def extract_features(self, modules: List[Dict[str, Any]]) -> Dict[str, Any]:
        features = {
            'num_modules': len(modules),
            'total_ports': 0,
            'total_wires': 0,
            'total_instances': 0,
            'design_complexity': 0.0
        }
        
        for module in modules:
            features['total_ports'] += len(module['ports'])
            features['total_wires'] += len(module['wires'])
        
        features['design_complexity'] = (
            features['num_modules'] * 100 +
            features['total_ports'] * 10
        )
        
        return features