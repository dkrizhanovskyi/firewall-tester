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
from typing import List, Dict
from jinja2 import Template

class ReportGenerator:
    """Class to generate an HTML report for firewall rule validation."""

    @staticmethod
    def generate_html_report(results: List[Dict], output_file: str):
        """
        Generate an HTML report from validation results.
        :param results: List of validation results.
        :param output_file: Path to save the HTML report.
        """
        template = """
        <html>
        <head>
            <title>Firewall Rule Validation Report</title>
        </head>
        <body>
            <h1>Firewall Rule Validation Report</h1>
            <table border="1">
                <tr>
                    <th>Rule ID</th>
                    <th>Protocol</th>
                    <th>Port</th>
                    <th>Direction</th>
                    <th>Expected Action</th>
                    <th>Observed Action</th>
                    <th>Status</th>
                </tr>
                {% for result in results %}
                <tr>
                    <td>{{ result.rule_id }}</td>
                    <td>{{ result.protocol }}</td>
                    <td>{{ result.port }}</td>
                    <td>{{ result.direction }}</td>
                    <td>{{ result.expected_action }}</td>
                    <td>{{ result.observed_action }}</td>
                    <td>{{ result.status }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """
        html_template = Template(template)
        html_content = html_template.render(results=results)

        with open(output_file, "w") as file:
            file.write(html_content)

        print(f"Report generated: {output_file}")
