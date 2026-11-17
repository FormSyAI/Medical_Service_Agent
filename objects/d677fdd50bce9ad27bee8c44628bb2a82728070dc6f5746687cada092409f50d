"""既有工具的回归测试。"""

import unittest

from tools.bills import list_bills
from tools.medications import list_medications
from tools.patient_profile import patient_profile


class ToolTests(unittest.TestCase):
    def test_patient_profile_returns_full_record(self):
        result = patient_profile("P7")
        self.assertEqual(result["patient"]["patient_id"], 7001)
        self.assertEqual(result["patient"]["name"], "张三丰(虚构)")

    def test_medications_include_patient_header(self):
        result = list_medications("P7")
        self.assertIn("patient", result)
        self.assertEqual(len(result["medications"]), 2)

    def test_bills_include_patient_header(self):
        result = list_bills("P7")
        self.assertIn("patient", result)
        self.assertEqual(len(result["bills"]), 2)

    def test_unauthorized_patient_rejected(self):
        with self.assertRaises(PermissionError):
            patient_profile("P9")


if __name__ == "__main__":
    unittest.main()
