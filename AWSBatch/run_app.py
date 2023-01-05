"""
Script to link all other necessary scripts to process app
"""

import weather
import validate_input_data
import reconcile_data
import analyze_data

weather.load_initial_data()
validate_input_data.run_json_validation()
reconcile_data.data_reconcile()
analyze_data.analyze()

