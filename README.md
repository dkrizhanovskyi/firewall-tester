# Automated Firewall Rule Tester

## Overview

The **Automated Firewall Rule Tester** is an open-source tool designed to validate and test firewall configurations. It automates the process of simulating traffic, validating firewall rules, and generating comprehensive reports to ensure your firewall meets security and compliance standards.

### Key Features
- **Firewall Rule Management**: Apply, reset, and manage rules dynamically using `iptables`.
- **Traffic Simulation**: Simulate TCP, UDP, and ICMP traffic with `hping3`.
- **Rule Validation**: Compare expected and observed firewall behavior to detect misconfigurations.
- **Logging and Reporting**: Centralized logs and HTML reports for easy debugging and analysis.
- **Unit Testing**: Comprehensive test suite for validating the tool's reliability.

---

## Getting Started

Follow these instructions to set up and use the **Automated Firewall Rule Tester**.

### Prerequisites
1. **Fedora 40** or similar Linux OS.
2. Required tools:
   - `iptables`
   - `firewalld` (optional)
   - `hping3`
   - `tcpdump`
3. **Python 3.8+** with `pip`.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/dkrizhanovskyi/firewall-tester.git
   cd firewall-tester
   ```

2. Set up a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install required system tools:
   ```bash
   sudo dnf install -y iptables firewalld hping3 tcpdump
   ```

---

## Usage

### 1. Apply Firewall Rules
Apply the rules defined in `rules/sample_rules.json`:
```bash
python3 src/main.py --apply-rules
```

### 2. Reset Firewall Rules
Reset (flush) all active firewall rules:
```bash
python3 src/main.py --reset-firewall
```

### 3. Validate Firewall Rules
Validate firewall rules and generate a detailed report:
```bash
python3 src/main.py --validate-rules
```

### 4. View Logs and Reports
- View validation logs:
  ```bash
  cat logs/validation.log
  ```
- Open the generated HTML report:
  ```bash
  firefox reports/validation_report.html
  ```

---

## Project Structure

```
firewall-tester/
├── LICENSE                     # GNU GPLv3 License
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── rules/                      # Folder for rule definitions
│   └── sample_rules.json       # Example JSON file with rules
├── src/                        # Source code
│   ├── __init__.py             # Marks src as a Python package
│   ├── main.py                 # Entry point for the project
│   ├── firewall_manager.py     # Firewall management logic
│   ├── traffic_simulator.py    # Traffic simulation logic
│   ├── rule_validator.py       # Rule validation logic
│   ├── logger.py               # Centralized logging utility
│   └── report_generator.py     # HTML report generation logic
├── tests/                      # Unit test suite
│   ├── __init__.py             # Marks tests as a Python package
│   ├── test_firewall_manager.py # Unit tests for firewall_manager
│   ├── test_rule_validator.py  # Unit tests for rule_validator
│   └── test_traffic_simulator.py # Unit tests for traffic_simulator
├── logs/                       # Logs generated at runtime
├── reports/                    # Reports generated at runtime
```

---

## Contributions

We welcome contributions from the community! Here's how you can help:

1. Fork the repository and create a new branch.
2. Make your changes and add tests for any new functionality.
3. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the GNU General Public License v3 (GPLv3).  
You are free to use, modify, and distribute this software under the terms of the GPLv3.  

See the [LICENSE](LICENSE) file for details or visit [GNU GPL website](https://www.gnu.org/licenses/gpl-3.0.html).

---


## Acknowledgments

- **`iptables`**: The powerful Linux firewall tool.
- **`hping3`**: For traffic simulation.
- **GNU GPLv3**: For fostering open-source collaboration.

---

## Future Enhancements

Planned features for future releases:
1. Support for `firewalld` alongside `iptables`.
2. Extend reporting to include CSV and JSON formats.
3. Add support for multi-host testing.

