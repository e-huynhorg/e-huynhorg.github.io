#!/usr/bin/env python3
"""
Script to anonymize IGNs in Maple Progression Tracker CSV files.
Replaces personal IGNs with Evan[JOB] format based on job abbreviations.
"""

import csv
import os
import re
from typing import Dict, List

def load_ign_to_job_mapping(account_file: str) -> Dict[str, str]:
    """Load IGN to job mapping from account.csv"""
    ign_to_job = {}
    try:
        with open(account_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                job_abbrev = row['jobName']
                ign = row['IGN']
                ign_to_job[ign] = job_abbrev
        print(f"Loaded {len(ign_to_job)} IGN-to-job mappings from {account_file}")
        return ign_to_job
    except Exception as e:
        print(f"Error loading IGN-to-job mapping: {e}")
        return {}

def create_ign_mapping(account_file: str) -> Dict[str, str]:
    """
    Create mapping from current IGNs to new Evan[JOB] format.
    Uses account.csv to dynamically determine job for each IGN.
    """
    # Load IGN to job mapping from account.csv
    ign_to_job = load_ign_to_job_mapping(account_file)
    if not ign_to_job:
        print("Error: Could not load IGN-to-job mapping!")
        return {}
    
    # Create the Evans[JOB] mapping
    ign_mapping = {}
    for ign, job_abbrev in ign_to_job.items():
        # Convert job abbreviation to uppercase for consistency
        job_upper = job_abbrev.upper()
        new_ign = f"Evan{job_upper}"
        ign_mapping[ign] = new_ign
    
    print(f"Created mapping for {len(ign_mapping)} IGNs")
    return ign_mapping

def process_csv_file(file_path: str, ign_mapping: Dict[str, str]) -> bool:
    """
    Process a single CSV file to replace IGNs.
    Returns True if any changes were made.
    """
    try:
        # Read the original file
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        if not rows:
            print(f"Warning: {file_path} is empty")
            return False
        
        changes_made = False
        
        # Process each row
        for row_idx, row in enumerate(rows):
            if not row:  # Skip empty rows
                continue
                
            for col_idx, cell in enumerate(row):
                if cell in ign_mapping:
                    old_ign = cell
                    new_ign = ign_mapping[cell]
                    rows[row_idx][col_idx] = new_ign
                    print(f"  {file_path}: Replaced '{old_ign}' with '{new_ign}'")
                    changes_made = True
        
        # Write back to file if changes were made
        if changes_made:
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            print(f"✓ Updated {file_path}")
        else:
            print(f"- No changes needed for {file_path}")
            
        return changes_made
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all CSV files"""
    # Set up paths
    data_dir = "data"
    account_file = os.path.join(data_dir, "account.csv")
    
    if not os.path.exists(data_dir):
        print(f"Error: Data directory '{data_dir}' not found!")
        print("Please run this script from the Maple-Progression-Tracker directory.")
        return
    
    if not os.path.exists(account_file):
        print(f"Error: Account file '{account_file}' not found!")
        return
    
    # Create IGN mapping from account.csv
    ign_mapping = create_ign_mapping(account_file)
    if not ign_mapping:
        print("Error: Could not create IGN mapping!")
        return
    
    # Get all CSV files except joblist.csv (we don't want to modify that)
    csv_files = []
    for file in os.listdir(data_dir):
        if file.endswith('.csv') and file != 'joblist.csv':
            csv_files.append(os.path.join(data_dir, file))
    
    if not csv_files:
        print("No CSV files found to process!")
        return
    
    print(f"\nFound {len(csv_files)} CSV files to process:")
    for file in csv_files:
        print(f"  - {file}")
    
    # Show the mapping that will be used
    print(f"\n=== IGN Mapping to be Applied ===")
    for old_ign, new_ign in sorted(ign_mapping.items()):
        print(f"{old_ign} -> {new_ign}")
    
    # Ask for confirmation
    print(f"\nThis will replace IGNs in {len(csv_files)} files (including account.csv).")
    confirm = input("Do you want to proceed? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    # Process each file
    print("\nProcessing files...")
    total_changes = 0
    for file_path in csv_files:
        print(f"\nProcessing {file_path}...")
        if process_csv_file(file_path, ign_mapping):
            total_changes += 1
    
    print(f"\n=== Summary ===")
    print(f"Processed {len(csv_files)} files")
    print(f"Modified {total_changes} files")
    print("Anonymization complete!")

if __name__ == "__main__":
    main()
