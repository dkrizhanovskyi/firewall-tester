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
import unittest
from unittest.mock import patch, MagicMock
from src.rule_validator import RuleValidator

class TestRuleValidator(unittest.TestCase):
    def setUp(self):
        """Set up a RuleValidator instance with a sample rule file."""
        self.rule_file = "rules/sample_rules.json"
        self.validator = RuleValidator(self.rule_file)

    @patch("src.rule_validator.TrafficSimulator.simulate_traffic")
    def test_validate_rules_pass(self, mock_simulate_traffic):
        """
        Test validate_rules for a passing case where observed and expected actions match.
        """
        # Mock traffic simulation results
        mock_simulate_traffic.side_effect = ["allowed", "blocked"]

        # Mock rules to return a test set of rules
        with patch.object(RuleValidator, "load_rules", return_value=[
            {"rule_id": 1, "direction": "incoming", "protocol": "tcp", "port": 22, "action": "allow"},
            {"rule_id": 2, "direction": "outgoing", "protocol": "udp", "port": 53, "action": "block"}
        ]):
            results = self.validator.validate_rules()

        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "pass")
        self.assertEqual(results[1]["status"], "pass")

    @patch("src.rule_validator.TrafficSimulator.simulate_traffic")
    def test_validate_rules_fail(self, mock_simulate_traffic):
        """
        Test validate_rules for a failing case where observed and expected actions differ.
        """
        # Mock traffic simulation results
        mock_simulate_traffic.side_effect = ["blocked", "allowed"]

        # Mock rules to return a test set of rules
        with patch.object(RuleValidator, "load_rules", return_value=[
            {"rule_id": 1, "direction": "incoming", "protocol": "tcp", "port": 22, "action": "allow"},
            {"rule_id": 2, "direction": "outgoing", "protocol": "udp", "port": 53, "action": "block"}
        ]):
            results = self.validator.validate_rules()

        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "fail")
        self.assertEqual(results[1]["status"], "fail")

    def test_load_rules(self):
        """
        Test load_rules to ensure it reads and parses the rules file correctly.
        """
        mock_rules = """
        [
            {"rule_id": 1, "direction": "incoming", "protocol": "tcp", "port": 22, "action": "allow"}
        ]
        """
        with patch("builtins.open", unittest.mock.mock_open(read_data=mock_rules)):
            rules = self.validator.load_rules()

        # Verify rules
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]["rule_id"], 1)
        self.assertEqual(rules[0]["direction"], "incoming")
        self.assertEqual(rules[0]["protocol"], "tcp")
        self.assertEqual(rules[0]["port"], 22)
        self.assertEqual(rules[0]["action"], "allow")


if __name__ == "__main__":
    unittest.main()
