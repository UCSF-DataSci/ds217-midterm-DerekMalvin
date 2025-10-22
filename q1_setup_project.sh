#!/bin/bash
set -euo pipefail

# Assignment 5, Question 1: Project Setup Script
# This script creates the directory structure for the clinical trial analysis project
# TODO: Make this script executable (if not already)
# chmod +x q1_setup_project.sh

# TODO: Create the following directories:
#   - data/
#   - output/
#   - reports/
mkdir -p data output reports

# TODO: Generate the dataset
#       Run: python3 generate_data.py
#       This creates data/clinical_trial_raw.csv with 10,000 patients
python3 generate_data.py

# TODO: Save the directory structure to reports/directory_structure.txt
#       Hint: Use 'ls -la' or 'tree' command
if command -v tree >/dev/null 2>&1; then
  tree -a > reports/directory_structure.txt
else
  ls -laR > reports/directory_structure.txt
fi