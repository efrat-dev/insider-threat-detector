"""
Configuration management for the Advanced Insider Threat Dataset Generator.

This module handles system configuration including:
- Logging setup
- Random seed initialization
- Output directory creation
"""

import sys
import logging
from pathlib import Path


def setup_logging(verbose=False, quiet=False):
    """Setup logging configuration"""
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('dataset_generation.log')
        ]
    )
    
    return logging.getLogger(__name__)


def setup_random_seed(seed=None):
    """Setup random seed for reproducibility"""
    if seed is not None:
        import random
        import numpy as np
        
        random.seed(seed)
        np.random.seed(seed)
        print(f"Random seed set to: {seed}")
    else:
        print("Using random seed")


def create_output_directory(output_dir):
    """Create output directory if it doesn't exist"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path