# Architecture of Automated Firewall Rule Tester

This document provides a detailed overview of the architecture and design principles behind the **Automated Firewall Rule Tester** project. It outlines the system's structure, key components, and the rationale for the design choices.

---

## Overview

The Automated Firewall Rule Tester is built to validate firewall rules by simulating network traffic and comparing the observed results with expected behaviors. The system is modular and adheres to software engineering best practices, making it maintainable, extensible, and easy to use.

---

## Design Principles

The project follows these key principles:

1. **SOLID Principles**:
   - **Single Responsibility**: Each module is responsible for a single aspect of the system (e.g., rule management, traffic simulation, validation).
   - **Open/Closed**: Modules are open for extension but closed for modification, allowing new features without altering existing code.
   - **Liskov Substitution**: Components can be replaced with implementations of the same interface without altering the system's behavior.
   - **Interface Segregation**: Each module uses minimal, specific interfaces for interaction.
   - **Dependency Inversion**: High-level modules do not depend on low-level modules; both depend on abstractions.

2. **Modularity**:
   - The system is divided into well-defined modules (`firewall_manager`, `traffic_simulator`, `rule_validator`, etc.) that can operate independently.

3. **Separation of Concerns**:
   - The system separates firewall management, traffic simulation, and result validation into distinct layers.

4. **Extensibility**:
   - Designed to support additional protocols, firewall tools (`firewalld`), and reporting formats with minimal effort.

---

## Architecture Diagram

```plaintext
+---------------------------------------------+
|          Automated Firewall Rule Tester     |
+---------------------------------------------+
|                                             |
| +---------------+   +--------------------+  |
| | Rule Loader   |   | Firewall Manager   |  |
| +---------------+   +--------------------+  |
|       |                           |         |
| +---------------+   +--------------------+  |
| | Traffic Sim   |   | Rule Validator     |  |
| +---------------+   +--------------------+  |
|       |                           |         |
|       +--------+   +-----------------------+|
|                |   | Report Generator      ||
|                +---+-----------------------+|
|                                             |
+---------------------------------------------+
```

---

## Key Components

### 1. **Firewall Manager**
**Purpose**: Manage firewall rules by interacting with `iptables`.

- **Responsibilities**:
  - Apply firewall rules from a JSON file.
  - Reset (flush) all active firewall rules.
  - Interface with `iptables` to execute commands.
- **Dependencies**: 
  - `subprocess` for running shell commands.
- **Key Methods**:
  - `apply_rule(rule: Dict)`: Applies a single rule to the firewall.
  - `reset_firewall()`: Resets all firewall rules.

---

### 2. **Traffic Simulator**
**Purpose**: Simulate network traffic to test the firewall.

- **Responsibilities**:
  - Simulate TCP, UDP, and ICMP traffic using `hping3`.
  - Generate test packets for incoming and outgoing traffic.
- **Dependencies**: 
  - `subprocess` for interacting with `hping3`.
- **Key Methods**:
  - `simulate_traffic(protocol: str, port: int, direction: str) -> str`: Simulates traffic and returns the result (`allowed` or `blocked`).

---

### 3. **Rule Validator**
**Purpose**: Validate observed firewall behavior against expected results.

- **Responsibilities**:
  - Load rules from a JSON file.
  - Validate rules by comparing expected outcomes with actual results from the `TrafficSimulator`.
  - Log validation results.
- **Dependencies**:
  - `TrafficSimulator` for observing actual firewall behavior.
- **Key Methods**:
  - `validate_rules() -> List[Dict]`: Validates all rules and returns a list of results.

---

### 4. **Report Generator**
**Purpose**: Generate reports summarizing rule validation results.

- **Responsibilities**:
  - Create user-friendly HTML reports of validation results.
- **Dependencies**:
  - `jinja2` for templating.
- **Key Methods**:
  - `generate_html_report(results: List[Dict], output_file: str)`: Creates an HTML report.

---

### 5. **Logging Utility**
**Purpose**: Centralize and standardize logging across the application.

- **Responsibilities**:
  - Write detailed logs of firewall actions, traffic simulations, and validation results.
- **Dependencies**:
  - `logging` module for log management.
- **Key Methods**:
  - `setup_logger(name: str, log_file: str) -> logging.Logger`: Sets up a logger with a file handler.

---

### 6. **Rule Definition (JSON)**
**Purpose**: Provide a structured format for defining firewall rules.

**Example JSON**:
```json
[
    {
        "rule_id": 1,
        "direction": "incoming",
        "protocol": "tcp",
        "port": 22,
        "action": "allow"
    },
    {
        "rule_id": 2,
        "direction": "outgoing",
        "protocol": "udp",
        "port": 53,
        "action": "block"
    }
]
```

---

## Workflow

1. **Load Rules**:
   - Rules are read from a JSON file and passed to the `FirewallManager` for application.

2. **Apply/Reset Rules**:
   - The `FirewallManager` applies or resets the firewall rules via `iptables`.

3. **Simulate Traffic**:
   - The `TrafficSimulator` sends test packets to determine how the firewall handles traffic.

4. **Validate Rules**:
   - The `RuleValidator` compares observed behavior with expected outcomes.

5. **Generate Report**:
   - Validation results are written to logs and an HTML report is generated.

---

## Extensibility

### Adding Support for `firewalld`
1. Implement a `FirewalldManager` class similar to `FirewallManager`.
2. Modify `main.py` to allow selecting the firewall tool (`iptables` or `firewalld`).

### Adding New Protocols
1. Extend the `TrafficSimulator` to handle additional protocols.
2. Update the JSON schema to define rules for the new protocol.

### Adding New Reporting Formats
1. Create a new `ReportGenerator` method for the desired format (e.g., CSV or JSON).
2. Modify `main.py` to include the new reporting option.

---

## Acknowledgments

This tool relies on the following technologies:
- **`iptables`**: For firewall rule management.
- **`hping3`**: For traffic simulation.
- **`tcpdump`**: For packet analysis.
- **`jinja2`**: For HTML report generation.
- **`unittest`**: For comprehensive testing.

---

## Future Enhancements

1. Multi-host testing to validate distributed firewall configurations.
2. Integration with CI/CD pipelines for automated rule validation.
3. Improved rule visualization using dashboards.

---

## Conclusion

The Automated Firewall Rule Tester is a modular and extensible solution for validating firewall configurations. Its clear separation of concerns and adherence to best practices make it a robust choice for security and compliance validation.

