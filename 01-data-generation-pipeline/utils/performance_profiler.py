"""
Performance profiling utilities for the Advanced Insider Threat Dataset Generator.

This module provides memory and performance monitoring capabilities.

Author: Advanced Security Analytics Team
Date: 2024
"""

import os


def profile_memory_usage():
    """Profile memory usage if profiling is enabled"""
    try:
        import psutil
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,  # Resident Set Size
            'vms_mb': memory_info.vms / 1024 / 1024,  # Virtual Memory Size
            'percent': process.memory_percent()
        }
    except ImportError:
        return None


def log_memory_usage(logger, stage_name, memory_info):
    """Log memory usage for a specific stage"""
    if memory_info:
        logger.info(f"{stage_name} memory usage: {memory_info['rss_mb']:.1f} MB")
    else:
        logger.debug(f"Memory profiling not available for {stage_name}")