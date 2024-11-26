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
from src.traffic_simulator import TrafficSimulator
from src.report_generator import ReportGenerator
from src.logger import setup_logger
import json

class RuleValidator:
    """Class to validate firewall rules against observed traffic behavior."""

    def __init__(self, rule_file: str):
        """
        Initialize RuleValidator with the path to a JSON file containing rules.
        :param rule_file: Path to the JSON file with firewall rules.
        """
        self.rule_file = rule_file
        self.simulator = TrafficSimulator()
        self.logger = setup_logger("RuleValidator", "logs/validation.log")

    def load_rules(self):
        """
        Load firewall rules from the JSON file.
        :return: List of rules.
        """
        try:
            with open(self.rule_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to load rules file: {e}")
            raise

    def validate_rules(self):
        """
        Validate each rule by simulating traffic and comparing expected vs observed results.
        :return: List of validation results.
        """
        rules = self.load_rules()
        results = []

        for rule in rules:
            protocol = rule["protocol"]
            port = rule["port"]
            direction = rule["direction"]
            expected_action = rule["action"]

            observed_action = self.simulator.simulate_traffic(protocol, port, direction)

            # Normalize observed_action to match expected_action vocabulary
            normalized_observed = "allow" if observed_action == "allowed" else "block"

            result = {
                "rule_id": rule["rule_id"],
                "protocol": protocol,
                "port": port,
                "direction": direction,
                "expected_action": expected_action,
                "observed_action": normalized_observed,
                "status": "pass" if expected_action == normalized_observed else "fail"
            }
            results.append(result)

            # Log the result
            self.logger.info(f"Rule {rule['rule_id']} validation: {result['status']}")

        return results


if __name__ == "__main__":
    # Example usage
    validator = RuleValidator("rules/sample_rules.json")
    validation_results = validator.validate_rules()

    # Print results
    for result in validation_results:
        print(f"Rule {result['rule_id']}: {result['status']}")
        print(f"  Protocol: {result['protocol']}, Port: {result['port']}")
        print(f"  Direction: {result['direction']}")
        print(f"  Expected: {result['expected_action']}, Observed: {result['observed_action']}")

    # Generate HTML report
    ReportGenerator.generate_html_report(validation_results, "reports/validation_report.html")

