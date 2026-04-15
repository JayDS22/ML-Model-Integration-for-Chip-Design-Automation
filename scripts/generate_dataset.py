#!/usr/bin/env python
import argparse
import json
import logging
import numpy as np
import random
from pathlib import Path
from typing import Dict
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SyntheticVerilogGenerator:
    def __init__(self, seed=42):
        random.seed(seed)
        np.random.seed(seed)
    
    def generate(self, num_samples: int, output_dir: Path):
        logger.info(f"Generating {num_samples} synthetic Verilog designs")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        metadata = []
        
        for i in tqdm(range(num_samples), desc="Generating designs"):
            num_ports = random.randint(4, 20)
            num_instances = random.randint(5, 50)
            
            verilog_code = self._generate_verilog_code(f"design_{i}", num_ports)
            power = self._calculate_power(num_instances, num_ports)
            timing = self._generate_timing(num_instances)
            drc = self._generate_drc(num_instances)
            
            design_data = {
                'design_id': f'synthetic_{i:06d}',
                'num_ports': num_ports,
                'num_instances': num_instances,
                'design_complexity': num_ports * 10 + num_instances * 50,
                'labels': {
                    'power_consumption': power,
                    'timing_status': timing,
                    'drc_violations': drc
                }
            }
            
            verilog_file = output_dir / f"design_{i:06d}.v"
            with open(verilog_file, 'w') as f:
                f.write(verilog_code)
            
            meta_file = output_dir / f"design_{i:06d}.json"
            with open(meta_file, 'w') as f:
                json.dump(design_data, f, indent=2)
            
            metadata.append(design_data)
        
        return metadata
    
    def _generate_verilog_code(self, module_name: str, num_ports: int) -> str:
        code = f"module {module_name} (\n"
        
        ports = []
        for i in range(num_ports // 2):
            width = random.choice([1, 8, 16])
            if width == 1:
                ports.append(f"    input wire clk")
            else:
                ports.append(f"    input wire [{width-1}:0] in_{i}")
                ports.append(f"    output reg [{width-1}:0] out_{i}")
        
        code += ",\n".join(ports[:num_ports]) + "\n);\n\n"
        
        for i in range(3):
            code += f"    wire internal_{i};\n"
        
        code += "\nendmodule\n"
        return code
    
    def _calculate_power(self, num_instances: int, num_ports: int) -> Dict:
        base_power = (num_instances / 100) * 0.8 + (num_ports / 50) * 0.2
        total = max(0.1, base_power + np.random.normal(0, 0.05))
        
        return {
            'total': round(total, 4),
            'dynamic': round(total * 0.65, 4),
            'static': round(total * 0.35, 4)
        }
    
    def _generate_timing(self, num_instances: int) -> Dict:
        if random.random() < 0.3:
            status = random.choice(['WARNING', 'FAIL'])
            violations = random.randint(1, 5)
        else:
            status = 'PASS'
            violations = 0
        
        return {'status': status, 'violations': violations}
    
    def _generate_drc(self, num_instances: int) -> Dict:
        if random.random() < 0.4:
            count = random.randint(1, 10)
        else:
            count = 0
        
        return {'count': count}


def parse_args():
    parser = argparse.ArgumentParser(description='Generate synthetic chip design dataset')
    parser.add_argument('--num-samples', type=int, default=100,
                        help='Number of samples to generate')
    parser.add_argument('--output', type=str, default='data/raw/synthetic',
                        help='Output directory')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed')
    return parser.parse_args()


def main():
    args = parse_args()
    
    output_path = Path(args.output)
    
    generator = SyntheticVerilogGenerator(seed=args.seed)
    metadata = generator.generate(args.num_samples, output_path)
    
    stats = {
        'total_samples': len(metadata),
        'seed': args.seed
    }
    
    with open(output_path / 'dataset_stats.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    logger.info(f"Dataset generation complete")
    logger.info(f"Total samples: {stats['total_samples']}")
    logger.info(f"Output directory: {output_path}")


if __name__ == '__main__':
    main()