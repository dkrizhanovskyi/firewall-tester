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
import subprocess
import json
from typing import List, Dict

class FirewallManager:
    """Class to manage firewall rules using iptables."""

    def __init__(self, rule_file: str):
        """
        Initialize FirewallManager with the path to a JSON file containing rules.
        :param rule_file: Path to the JSON file with firewall rules.
        """
        self.rule_file = rule_file
        self.rules = self._load_rules()

    def _load_rules(self) -> List[Dict]:
        """
        Load firewall rules from the JSON file.
        :return: List of rules.
        """
        try:
            with open(self.rule_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise Exception(f"Failed to load rules file: {e}")

    def apply_rule(self, rule: Dict) -> None:
        """
        Apply a single rule using iptables.
        :param rule: A dictionary containing the rule details.
        """
        direction = "INPUT" if rule["direction"] == "incoming" else "OUTPUT"
        action = "ACCEPT" if rule["action"] == "allow" else "DROP"
        protocol = rule["protocol"]
        port = rule["port"]

        cmd = f"sudo iptables -A {direction} -p {protocol} --dport {port} -j {action}"
        self._execute_command(cmd)

    def apply_all_rules(self) -> None:
        """
        Apply all rules from the JSON file.
        """
        for rule in self.rules:
            print(f"Applying Rule {rule['rule_id']}: {rule}")
            self.apply_rule(rule)

    def reset_firewall(self) -> None:
        """
        Reset the firewall by flushing all rules.
        """
        self._execute_command("sudo iptables -F")
        print("All firewall rules have been reset.")

    def _execute_command(self, command: str) -> None:
        """
        Execute a shell command and handle errors.
        :param command: Command to execute.
        """
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to execute command: {e}")

if __name__ == "__main__":
    # Example usage
    manager = FirewallManager("rules/sample_rules.json")
    manager.reset_firewall()
    manager.apply_all_rules()
