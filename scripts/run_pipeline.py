#!/usr/bin/env python
import argparse
import json
import logging
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parsers.verilog_parser import VerilogParser
from src.ml.inference import ChipDesignPredictor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Run ML chip design pipeline')
    parser.add_argument('--input', type=str, required=True, help='Input file path')
    parser.add_argument('--output', type=str, default='results.json', help='Output file path')
    return parser.parse_args()


def main():
    args = parse_arguments()
    start_time = time.time()
    
    try:
        input_file = Path(args.input)
        if not input_file.exists():
            logger.error(f"Input file not found: {args.input}")
            sys.exit(1)
        
        logger.info(f"Parsing design file: {args.input}")
        parser = VerilogParser()
        modules = parser.parse(args.input)
        features = parser.extract_features(modules)
        
        logger.info("Running ML inference")
        predictor = ChipDesignPredictor()
        predictor.load_models()
        results = predictor.predict(features)
        
        results['input_file'] = str(input_file)
        results['pipeline_time'] = time.time() - start_time
        
        output_file = Path(args.output)
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to: {args.output}")
        
        print("\nAnalysis Results:")
        print(f"DRC Violations: {results['drc_violations']}")
        print(f"Power Consumption: {results['power_consumption']}W")
        print(f"Timing Status: {results['timing_status']}")
        print(f"Processing Time: {results['processing_time']:.2f}s")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()