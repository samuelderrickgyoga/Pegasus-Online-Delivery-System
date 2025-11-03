"""
Quick Start Script - Populate Database and Generate Visualizations
Run this script to populate the database and create all visualizations in one go
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print("\n" + "="*70)
    print(f"RUNNING: {description}")
    print("="*70 + "\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True,
            check=True
        )
        print(f"\n✓ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error running {description}")
        print(f"Error: {e}")
        return False
    except FileNotFoundError:
        print(f"\n✗ Script not found: {script_name}")
        return False

def main():
    print("="*70)
    print("ODS QUICK START - DATABASE POPULATION & VISUALIZATION")
    print("="*70)
    print("\nThis script will:")
    print("  1. Populate the database with 248 sample records")
    print("  2. Generate 8 comprehensive visualizations")
    print("  3. Create a detailed summary report")
    print("\n" + "="*70)
    
    # Check if scripts exist
    if not os.path.exists('populate_database.py'):
        print("\n✗ Error: populate_database.py not found!")
        return
    
    if not os.path.exists('visualize_database.py'):
        print("\n✗ Error: visualize_database.py not found!")
        return
    
    # Ask for confirmation
    response = input("\nProceed with population and visualization? (yes/no): ")
    if response.lower() != 'yes':
        print("Operation cancelled.")
        return
    
    # Step 1: Populate database
    success = run_script('populate_database.py', 'Database Population')
    if not success:
        print("\n⚠ Database population failed. Stopping execution.")
        return
    
    # Step 2: Generate visualizations
    success = run_script('visualize_database.py', 'Visualization Generation')
    if not success:
        print("\n⚠ Visualization generation failed.")
        return
    
    # Final summary
    print("\n" + "="*70)
    print("ALL OPERATIONS COMPLETE!")
    print("="*70)
    print("\nGenerated Files:")
    print("  • visualization_1_pie_chart.png")
    print("  • visualization_2_bar_chart.png")
    print("  • visualization_3_project_status.png")
    print("  • visualization_4_demographics.png")
    print("  • visualization_5_equipment_condition.png")
    print("  • visualization_6_facility_capacity.png")
    print("  • visualization_7_outcome_impact.png")
    print("  • visualization_8_dashboard.png")
    print("  • visualization_summary_report.txt")
    print("\nDatabase:")
    print("  • 248 records created across all entities")
    print("  • Ratio: 8:7:6:5:4:3:2:1")
    print("\nNext Steps:")
    print("  • Review the visualization images")
    print("  • Read the summary report")
    print("  • Run the Flask application: python run.py")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
