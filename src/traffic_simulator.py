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
from typing import Dict

class TrafficSimulator:
    """Class to simulate network traffic using hping3."""

    def simulate_traffic(self, protocol: str, port: int, direction: str) -> str:
        """
        Simulate network traffic and return the result.
        :param protocol: The protocol to use ('tcp', 'udp', or 'icmp').
        :param port: The port to test.
        :param direction: The traffic direction ('incoming' or 'outgoing').
        :return: 'allowed' if the traffic passes, 'blocked' otherwise.
        """
        target = "127.0.0.1"  # Test traffic locally
        flags = {
            "tcp": "-S",   # TCP SYN flag
            "udp": "--udp",  # UDP traffic
            "icmp": "--icmp"  # ICMP ping
        }

        # Construct the hping3 command
        if direction == "incoming":
            cmd = f"sudo hping3 {target} {flags[protocol]} -p {port} -c 1"
        else:  # Simulate outgoing traffic
            cmd = f"sudo hping3 -c 1 -s {port} {target} {flags[protocol]}"

        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            # Parse hping3 output
            if "flags=SA" in result.stdout:  # TCP response for allowed traffic
                return "allowed"
            elif "Operation not permitted" in result.stderr:  # Blocked traffic
                return "blocked"
            elif "ICMP Packet received" in result.stdout:  # ICMP allowed
                return "allowed"
            else:
                return "blocked"
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"

if __name__ == "__main__":
    # Example usage
    simulator = TrafficSimulator()

    # Test TCP port 22 (incoming)
    result = simulator.simulate_traffic("tcp", 22, "incoming")
    print(f"TCP port 22 (incoming): {result}")

    # Test UDP port 53 (outgoing)
    result = simulator.simulate_traffic("udp", 53, "outgoing")
    print(f"UDP port 53 (outgoing): {result}")
