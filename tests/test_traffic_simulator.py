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
from src.traffic_simulator import TrafficSimulator

class TestTrafficSimulator(unittest.TestCase):
    def setUp(self):
        """Set up a TrafficSimulator instance."""
        self.simulator = TrafficSimulator()

    @patch("src.traffic_simulator.subprocess.run")
    def test_simulate_traffic_tcp_allowed(self, mock_subprocess):
        """
        Test simulate_traffic for TCP when traffic is allowed.
        """
        # Mock subprocess.run to simulate allowed TCP traffic
        mock_subprocess.return_value = MagicMock(stdout="flags=SA")

        result = self.simulator.simulate_traffic("tcp", 22, "incoming")
        
        self.assertEqual(result, "allowed")
        mock_subprocess.assert_called_once_with(
            "sudo hping3 127.0.0.1 -S -p 22 -c 1", shell=True, capture_output=True, text=True
        )

    @patch("src.traffic_simulator.subprocess.run")
    def test_simulate_traffic_tcp_blocked(self, mock_subprocess):
        """
        Test simulate_traffic for TCP when traffic is blocked.
        """
        # Mock subprocess.run to simulate blocked TCP traffic
        mock_subprocess.return_value = MagicMock(stdout="")

        result = self.simulator.simulate_traffic("tcp", 22, "incoming")
        
        self.assertEqual(result, "blocked")
        mock_subprocess.assert_called_once_with(
            "sudo hping3 127.0.0.1 -S -p 22 -c 1", shell=True, capture_output=True, text=True
        )

    @patch("src.traffic_simulator.subprocess.run")
    def test_simulate_traffic_udp_allowed(self, mock_subprocess):
        """
        Test simulate_traffic for UDP when traffic is allowed.
        """
        # Mock subprocess.run to simulate allowed UDP traffic
        mock_subprocess.return_value = MagicMock(stdout="ICMP Packet received")

        result = self.simulator.simulate_traffic("udp", 53, "outgoing")
        
        self.assertEqual(result, "allowed")
        mock_subprocess.assert_called_once_with(
            "sudo hping3 -c 1 -s 53 127.0.0.1 --udp", shell=True, capture_output=True, text=True
        )

    @patch("src.traffic_simulator.subprocess.run")
    def test_simulate_traffic_udp_blocked(self, mock_subprocess):
        """
        Test simulate_traffic for UDP when traffic is blocked.
        """
        # Mock subprocess.run to simulate blocked UDP traffic
        mock_subprocess.return_value = MagicMock(stderr="Operation not permitted")

        result = self.simulator.simulate_traffic("udp", 53, "outgoing")
        
        self.assertEqual(result, "blocked")
        mock_subprocess.assert_called_once_with(
            "sudo hping3 -c 1 -s 53 127.0.0.1 --udp", shell=True, capture_output=True, text=True
        )

if __name__ == "__main__":
    unittest.main()
