import json
import unittest
from datetime import datetime
from unittest.mock import patch, Mock

from safety.formatters.json import JsonReport
from packaging.version import parse

from safety.models import CVE, Vulnerability, Package


class TestJSONFormatter(unittest.TestCase):

    def setUp(self) -> None:
        self.formatter = JsonReport()
        self.maxDiff = None

    @patch('safety.formatters.json.datetime', Mock(
        now=Mock(return_value=datetime(2022, month=3, day=3, hour=16, minute=31, second=30, microsecond=46504))))
    @patch('safety.formatters.json.get_report_brief_info')
    def test_render_vulnerabilities_with_remediations(self, get_report_brief_info):
        get_report_brief_info.return_value = {'scan_target': 'environment',
                                              'scanned': ['/usr/local/lib/python3.9/site-packages'],
                                              'api_key_used': True,
                                              'packages_found': 2,
                                              'timestamp': '2022-03-03 16:31:30',
                                              'safety_version': '2.0.0.dev6'}

        affected_package = Package(name='django', version='4.0.1',
                                   found='/usr/local/lib/python3.9/site-packages',
                                   insecure_versions=['4.0.1'], secure_versions=['4.0.4', '3.2.13', '2.2.28'],
                                   latest_version_without_known_vulnerabilities='',
                                   latest_version='4.0.4',
                                   more_info_url='https://pyup.io/packages/pypi/django/')

        remediations = {
            'django': {'vulns_found': 1, 'version': '4.0.1', 'secure_versions': ['2.2.28', '3.2.13', '4.0.4'],
                       'closest_secure_version': {'major': parse('4.0.4'),
                                                  'minor': None},
                       'more_info_url': 'https://pyup.io/packages/pypi/django/'}}
        vulnerabilities = [Vulnerability(name='django', pkg=affected_package,
                                         ignored=False, reason='', expires='', vulnerable_spec='>=4.0a1,<4.0.2',
                                         all_vulnerable_specs=['>=4.0a1,<4.0.2'],
                                         analyzed_version='4.0.1',
                                         advisory='The {% debug %} template tag in Django',
                                         vulnerability_id='44742', is_transitive=False, published_date='2022-Feb-03',
                                         fixed_versions=['2.2.27', '3.2.12', '4.0.2'],
                                         closest_versions_without_known_vulnerabilities=[],
                                         resources=['https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-22818'],
                                         CVE=CVE(name='CVE-2022-22818',
                                                 cvssv2={'base_score': 4.3, 'impact_score': 2.9,
                                                         'vector_string': 'AV:N/AC:M/Au:N/C:N/I:P/A:N'},
                                                 cvssv3={'base_score': 6.1, 'impact_score': 2.7,
                                                         'base_severity': 'MEDIUM',
                                                         'vector_string': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N'}),
                                         affected_versions=['4.0.1'],
                                         more_info_url='https://pyup.io/vulnerabilities/CVE-2022-22818/44742/')]
        packages = [Package(name='secure-package', version='0.1.0',
                            found='/usr/local/lib/python3.9/site-packages',
                            insecure_versions=[], secure_versions=['0.1.0'],
                            latest_version_without_known_vulnerabilities='',
                            latest_version='0.1.0',
                            more_info_url='https://pyup.io/packages/pypi/secure-package/'),
                    affected_package]

        result = self.formatter.render_vulnerabilities(announcements=[], vulnerabilities=vulnerabilities,
                                                       remediations=remediations, full=True, packages=packages)

        expected_result = json.dumps(
            {
                "generated_at": "2022-03-03 16:31:30.046504",
                "report": {
                    "scan_target": "environment",
                    "scanned": [
                        "/usr/local/lib/python3.9/site-packages"
                    ],
                    "api_key_used": True,
                    "packages_found": 2,
                    "timestamp": "2022-03-03 16:31:30",
                    "safety_version": "2.0.0.dev6"
                },
                "scanned_packages": {
                    "secure-package": {
                        "name": "secure-package",
                        "version": "0.1.0"
                    },
                    "django": {
                        "name": "django",
                        "version": "4.0.1"
                    },
                },
                "affected_packages": {
                    "django": {
                        "name": "django",
                        "version": "4.0.1",
                        "found": "/usr/local/lib/python3.9/site-packages",
                        "insecure_versions": [
                            "4.0.1"
                        ],
                        "secure_versions": [
                            "4.0.4",
                            "3.2.13",
                            "2.2.28"
                        ],
                        "latest_version_without_known_vulnerabilities": "",
                        "latest_version": "4.0.4",
                        "more_info_url": "https://pyup.io/packages/pypi/django/"
                    }
                },
                "announcements": [],
                "vulnerabilities": [
                    {
                        "name": "django",
                        "ignored": False,
                        "reason": "",
                        "expires": "",
                        "vulnerable_spec": ">=4.0a1,<4.0.2",
                        "all_vulnerable_specs": [
                            ">=4.0a1,<4.0.2"
                        ],
                        "analyzed_version": "4.0.1",
                        "advisory": "The {% debug %} template tag in Django",
                        "vulnerability_id": "44742",
                        "is_transitive": False,
                        "published_date": "2022-Feb-03",
                        "fixed_versions": [
                            "2.2.27",
                            "3.2.12",
                            "4.0.2"
                        ],
                        "closest_versions_without_known_vulnerabilities": [],
                        "resources": [
                            "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-22818"
                        ],
                        "CVE": {
                            "name": "CVE-2022-22818",
                            "cvssv2": {
                                "base_score": 4.3,
                                "impact_score": 2.9,
                                "vector_string": "AV:N/AC:M/Au:N/C:N/I:P/A:N"
                            },
                            "cvssv3": {
                                "base_score": 6.1,
                                "impact_score": 2.7,
                                "base_severity": "MEDIUM",
                                "vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N"
                            }
                        },
                        "affected_versions": [
                            "4.0.1",
                        ],
                        "more_info_url": "https://pyup.io/vulnerabilities/CVE-2022-22818/44742/"
                    },
                ],
                "ignored_vulnerabilities": [],
                "remediations": {
                    "django": {
                        "vulns_found": 1,
                        "version": "4.0.1",
                        "recommended": "4.0.4",
                        "other_recommended_versions": [
                            "2.2.28",
                            "3.2.13"
                        ],
                        "more_info_url": "https://pyup.io/packages/pypi/django/"
                    }
                }
            },
            indent=4
        )
        self.assertEqual(result, expected_result)
