#!/usr/bin/env python3

# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.

import sys
import os
from pathlib import Path
import random

def parse_config(filepath: str) -> dict:
    """
    Parse config file (key=value format) into dictionary.

    Args:
        filepath: Path to q2_config.txt

    Returns:
        dict: Configuration as key-value pairs

    Example:
        >>> config = parse_config('q2_config.txt')
        >>> config['sample_data_rows']
        '100'
    """
    # TODO: Read file, split on '=', create dict
    cfg = {}
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line:
                key, value = line.split("=", 1)
                cfg[key.strip()] = value.strip()
    return cfg



def validate_config(config: dict) -> dict:
    """
    Validate configuration values using if/elif/else logic.

    Rules:
    - sample_data_rows must be an int and > 0
    - sample_data_min must be an int and >= 1
    - sample_data_max must be an int and > sample_data_min

    Args:
        config: Configuration dictionary

    Returns:
        dict: Validation results {key: True/False}

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> results = validate_config(config)
        >>> results['sample_data_rows']
        True
    """
    # TODO: Implement with if/elif/else
    results = {}
    if config['sample_data_rows'].isdigit() and int(config['sample_data_rows']) > 0:
        results['sample_data_rows'] = True
    else:
        results['sample_data_rows'] = False
    if config['sample_data_min'].isdigit() and int(config['sample_data_min']) >= 1:
        results['sample_data_min'] = True
    else:
        results['sample_data_min'] = False
    if config['sample_data_max'].isdigit() and int(config['sample_data_max']) > int(config['sample_data_min']):
        results['sample_data_max'] = True
    else:
        results['sample_data_max'] = False
    
    return results


def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random numbers for testing, one number per row with no header.
    Uses config parameters for number of rows and range.

    Args:
        filename: Output filename (e.g., 'sample_data.csv')
        config: Configuration dictionary with sample_data_rows, sample_data_min, sample_data_max

    Returns:
        None: Creates file on disk

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> generate_sample_data('sample_data.csv', config)
        # Creates file with 100 random numbers between 18-75, one per row
        >>> import random
        >>> random.randint(18, 75)  # Returns random integer between 18-75
    """
    # TODO: Parse config values (convert strings to int)
    # TODO: Generate random numbers and save to file
    # TODO: Use random module with config-specified range
    num_rows = int(config.get('sample_data_rows', 0))
    min_value = int(config.get('sample_data_min', 0))
    max_value = int(config.get('sample_data_max', 0))
    with open(filename, 'w') as output_file:
        for count in range(num_rows):
            random_number = random.randint(min_value, max_value)
            output_file.write(f"{random_number}\n")


def _median_from_list(nums):
    """Return median of a list of numbers as float."""
    n = len(nums)
    if n == 0:
        return 0.0
    sorted_nums = sorted(nums)
    mid = n // 2
    if n % 2 == 1:
        return float(sorted_nums[mid])
    else:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0


def calculate_statistics(data: list) -> dict:
    """
    Calculate basic statistics.

    Args:
        data: List of numbers

    Returns:
        dict: {mean, median, sum, count}

    Example:
        >>> stats = calculate_statistics([10, 20, 30, 40, 50])
        >>> stats['mean']
        30.0
    """
    # TODO: Calculate stats
    """
    Calculate Statistics (Mean, Median, Sum, Count)
    """
    if not data:
        return {'mean': 0.0, 'median': 0.0, 'sum': 0, 'count': 0}

    nums = [int(x) for x in data]
    total = sum(nums)
    count = len(nums)
    mean = total / count
    sorted_nums = sorted(nums)             
    mid = count // 2
    median = float(sorted_nums[mid]) if (count % 2 == 1) else (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0

    return {'mean': mean, 'median': median, 'sum': total, 'count': count}


if __name__ == '__main__':
    # TODO: Test your functions with sample data
    # Example:
    # config = parse_config('q2_config.txt')
    # validation = validate_config(config)
    # generate_sample_data('data/sample_data.csv', config)
    # 
    # TODO: Read the generated file and calculate statistics
    # TODO: Save statistics to output/statistics.txt
    cfg = parse_config("q2_config.txt")
    checks = validate_config(cfg)
    print("Validation:", checks)
    if not (checks["sample_data_rows"] and checks["sample_data_min"] and checks["sample_data_max"]):
        print("Invalid q2_config.txt")
    else:
        sample_path = "data/sample_data.csv"
        generate_sample_data(sample_path, cfg)
        with open(sample_path, "r") as fh:               
            nums = [line.strip() for line in fh if line.strip()]
        stats = calculate_statistics(nums)
        from pathlib import Path
        Path("output").mkdir(parents=True, exist_ok=True)
        with open("output/statistics.txt", "w") as out:  
            out.write(f"count:  {stats['count']}\n")
            out.write(f"sum:    {stats['sum']}\n")
            out.write(f"mean:   {stats['mean']}\n")
            out.write(f"median: {stats['median']}\n")