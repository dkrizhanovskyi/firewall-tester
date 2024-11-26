# This file is part of the Automated Firewall Rule Tester.
# 
# Automated Firewall Rule Tester is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Automated Firewall Rule Tester is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Automated Firewall Rule Tester. If not, see <https://www.gnu.org/licenses/>.
import argparse
from src.firewall_manager import FirewallManager
from src.rule_validator import RuleValidator
from src.report_generator import ReportGenerator

def main():
    """
    Main function to execute the Automated Firewall Rule Tester.
    Provides an interactive interface for managing and testing firewall rules.
    """
    parser = argparse.ArgumentParser(description="Automated Firewall Rule Tester")
    parser.add_argument(
        "--apply-rules", 
        action="store_true", 
        help="Apply firewall rules from the rules JSON file."
    )
    parser.add_argument(
        "--reset-firewall", 
        action="store_true", 
        help="Reset the firewall by flushing all rules."
    )
    parser.add_argument(
        "--validate-rules", 
        action="store_true", 
        help="Validate firewall rules and generate a report."
    )
    parser.add_argument(
        "--generate-report", 
        action="store_true", 
        help="Generate an HTML report from the last validation."
    )
    args = parser.parse_args()

    # File paths
    rules_file = "rules/sample_rules.json"
    log_file = "logs/validation.log"
    report_file = "reports/validation_report.html"

    if args.reset_firewall:
        print("Resetting the firewall...")
        manager = FirewallManager(rules_file)
        manager.reset_firewall()
        print("Firewall rules have been reset.")
    elif args.apply_rules:
        print("Applying firewall rules...")
        manager = FirewallManager(rules_file)
        manager.apply_all_rules()
        print("Firewall rules applied successfully.")
    elif args.validate_rules:
        print("Validating firewall rules...")
        validator = RuleValidator(rules_file)
        validation_results = validator.validate_rules()

        # Print summary
        print("\nValidation Summary:")
        for result in validation_results:
            print(f"Rule {result['rule_id']}: {result['status']}")
            print(f"  Protocol: {result['protocol']}, Port: {result['port']}")
            print(f"  Direction: {result['direction']}")
            print(f"  Expected: {result['expected_action']}, Observed: {result['observed_action']}")

        # Generate HTML report
        ReportGenerator.generate_html_report(validation_results, report_file)
        print(f"\nValidation report generated: {report_file}")
    elif args.generate_report:
        print("Generating report from the last validation results...")
        validator = RuleValidator(rules_file)
        validation_results = validator.validate_rules()
        ReportGenerator.generate_html_report(validation_results, report_file)
        print(f"Report generated: {report_file}")
    else:
        print("No valid option provided. Use --help to see available options.")

if __name__ == "__main__":
    main()
