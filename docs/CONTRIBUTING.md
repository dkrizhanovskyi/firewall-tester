# Security Policy

## Overview

The **Automated Firewall Rule Tester** project prioritizes security to ensure the integrity and reliability of its functionality. This document outlines the security policy for the project, including how to report vulnerabilities and best practices for securely using the tool.

---

## Supported Versions

The following versions of the project are currently supported for security updates:

| Version | Supported          |
|---------|--------------------|
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

---

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly to ensure it is addressed promptly and safely.

### Steps to Report:
1. **Do not publicly disclose the vulnerability** until it is fixed.
2. Send an email to **daniil.krizhanovskyi@hotmail.com** with the following details:
   - A clear and concise description of the vulnerability.
   - Steps to reproduce the issue.
   - Any potential impact or exploit scenarios.
3. We will acknowledge your report within **48 hours** and work with you to resolve the issue.

---

## Security Best Practices for Users

1. **Run the Tool with Proper Permissions**:
   - The tool interacts with `iptables` and requires elevated privileges (`sudo`). Ensure that only trusted individuals have access to these permissions.

2. **Keep Your Environment Updated**:
   - Regularly update your OS, including tools like `iptables`, `firewalld`, and `hping3`.

3. **Validate Rule Definitions**:
   - Ensure that `rules/sample_rules.json` contains only trusted configurations.

4. **Isolate the Testing Environment**:
   - Use a secure, isolated environment (e.g., a virtual machine) for testing to prevent accidental misconfigurations on production systems.

5. **Monitor Logs**:
   - Regularly review the `logs/validation.log` file for unexpected behavior or potential security concerns.

---

## Known Vulnerabilities

Currently, there are no known vulnerabilities in this project. This section will be updated if any issues arise.

---

## Security Updates

### How We Address Vulnerabilities:
1. Security patches will be prioritized over feature updates.
2. All users are encouraged to update to the latest version to benefit from security fixes.

---

## Contact

If you have any questions or concerns about the security of this project, feel free to contact us at **daniil.krizhanovskyi@hotmail.com**.

---

## Acknowledgments

We thank the open-source community for their contributions and vigilance in maintaining security across all projects.

