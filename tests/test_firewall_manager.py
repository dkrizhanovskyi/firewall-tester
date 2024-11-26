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
from src.firewall_manager import FirewallManager

class TestFirewallManager(unittest.TestCase):
    def setUp(self):
        """Set up a FirewallManager instance with a sample rule file."""
        self.rule_file = "rules/sample_rules.json"
        self.manager = FirewallManager(self.rule_file)

    @patch("src.firewall_manager.subprocess.run")
    def test_reset_firewall(self, mock_subprocess):
        """
        Test the reset_firewall method to ensure it executes the correct iptables command.
        """
        mock_subprocess.return_value = MagicMock()
        
        self.manager.reset_firewall()
        
        mock_subprocess.assert_called_once_with("sudo iptables -F", shell=True, check=True)

    @patch("src.firewall_manager.subprocess.run")
    def test_apply_rule(self, mock_subprocess):
        """
        Test the apply_rule method with a sample rule.
        """
        mock_subprocess.return_value = MagicMock()
        
        rule = {
            "rule_id": 1,
            "direction": "incoming",
            "protocol": "tcp",
            "port": 22,
            "action": "allow"
        }
        
        self.manager.apply_rule(rule)
        
        expected_command = "sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT"
        mock_subprocess.assert_called_once_with(expected_command, shell=True, check=True)

    @patch("src.firewall_manager.subprocess.run")
    def test_apply_all_rules(self, mock_subprocess):
        """
        Test the apply_all_rules method to ensure all rules are applied.
        """
        mock_subprocess.return_value = MagicMock()

        # Mock _load_rules to return a test set of rules
        with patch.object(FirewallManager, "_load_rules", return_value=[
            {"rule_id": 1, "direction": "incoming", "protocol": "tcp", "port": 22, "action": "allow"},
            {"rule_id": 2, "direction": "outgoing", "protocol": "udp", "port": 53, "action": "block"}
        ]):
            self.manager.apply_all_rules()

        # Check that subprocess.run was called twice with expected commands
        expected_calls = [
            unittest.mock.call("sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT", shell=True, check=True),
            unittest.mock.call("sudo iptables -A OUTPUT -p udp --dport 53 -j DROP", shell=True, check=True)
        ]
        mock_subprocess.assert_has_calls(expected_calls, any_order=True)

    def test_load_rules(self):
        """
        Test the _load_rules method to ensure it reads and parses the rules file correctly.
        """
        with patch("builtins.open", unittest.mock.mock_open(read_data="""
        [
            {"rule_id": 1, "direction": "incoming", "protocol": "tcp", "port": 22, "action": "allow"}
        ]
        """)):
            rules = self.manager._load_rules()
            self.assertEqual(len(rules), 1)
            self.assertEqual(rules[0]["rule_id"], 1)
            self.assertEqual(rules[0]["direction"], "incoming")
            self.assertEqual(rules[0]["protocol"], "tcp")
            self.assertEqual(rules[0]["port"], 22)
            self.assertEqual(rules[0]["action"], "allow")

if __name__ == "__main__":
    unittest.main()
