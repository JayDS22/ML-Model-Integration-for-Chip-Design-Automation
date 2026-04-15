import pytest
import tempfile
from pathlib import Path

from src.parsers.verilog_parser import VerilogParser


class TestVerilogParser:
    def setup_method(self):
        self.parser = VerilogParser()
    
    def test_parser_initialization(self):
        assert len(self.parser.modules) == 0
        assert self.parser.current_module is None
    
    def test_parse_simple_module(self):
        verilog_code = """
        module test_module(
            input wire clk,
            input wire [7:0] data_in,
            output reg [7:0] data_out
        );
            wire internal_sig;
        endmodule
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.v', delete=False) as f:
            f.write(verilog_code)
            temp_path = f.name
        
        try:
            modules = self.parser.parse(temp_path)
            
            assert len(modules) == 1
            module = modules[0]
            assert module['name'] == 'test_module'
            assert len(module['ports']) >= 2
        finally:
            Path(temp_path).unlink()
    
    def test_extract_features(self):
        mock_modules = [
            {
                'name': 'test',
                'ports': [{'direction': 'input', 'width': '0:0', 'name': 'a'}],
                'wires': [{'type': 'wire', 'width': '0:0', 'name': 'b'}],
                'io_summary': {'input': 1, 'output': 0, 'inout': 0}
            }
        ]
        
        features = self.parser.extract_features(mock_modules)
        
        assert features['num_modules'] == 1
        assert features['total_ports'] == 1
        assert features['design_complexity'] > 0