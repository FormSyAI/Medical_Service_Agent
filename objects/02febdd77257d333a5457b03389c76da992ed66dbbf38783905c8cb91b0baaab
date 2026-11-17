"""模型请求脱敏的回归测试：任何一次请求（所有 messages）都不得携带完整手机号、身份证号。"""

import json
import unittest

from service import CustomerServiceAgent

FULL_PHONE = "13900001234"
FULL_ID_CARD = "110105199003074219"
MASKED_PHONE = "139****1234"
MASKED_ID_CARD = "110" + "*" * 11 + "4219"


class _StubModelClient:
    """按预设工具回应；不写日志、不访问网络。"""

    def __init__(self, tool, arguments):
        self.tool = tool
        self.arguments = arguments
        self.calls = []

    def send(self, messages):
        self.calls.append(messages)
        if messages[-1]["role"] == "user":
            return {"tool": self.tool, "arguments": self.arguments}
        return "已为您查询。"


class ModelEgressTests(unittest.TestCase):
    def _run(self, tool, arguments, user_text="测试问题"):
        client = _StubModelClient(tool, arguments)
        agent = CustomerServiceAgent(model_client=client)
        agent.answer(user_text)
        for index, messages in enumerate(client.calls, start=1):
            blob = json.dumps(messages, ensure_ascii=False)
            self.assertNotIn(FULL_PHONE, blob, f"第 {index} 次请求出现完整手机号")
            self.assertNotIn(FULL_ID_CARD, blob, f"第 {index} 次请求出现完整身份证号")
            self.assertNotIn("patient_id", blob, f"第 {index} 次请求出现 patient_id")
        return agent, client

    def test_appointments_keep_only_needed_fields(self):
        agent, client = self._run("list_appointments", {"identifier": FULL_PHONE})
        view = agent.last_result
        self.assertEqual(view["patient_ref"], "P7")
        self.assertEqual(len(view["appointments"]), 2)
        self.assertEqual(sorted(view["appointments"][0]),
                         ["date", "department", "status", "time"])

    def test_masked_identifier_is_restored_in_process(self):
        agent, client = self._run("list_appointments", {"identifier": MASKED_PHONE})
        self.assertEqual(agent.last_result["patient_ref"], "P7")
        self.assertEqual(len(agent.last_result["appointments"]), 2)
        second_request = json.dumps(client.calls[1], ensure_ascii=False)
        self.assertIn(MASKED_PHONE, second_request)

    def test_full_identifier_in_user_text_is_masked_in_requests(self):
        agent, client = self._run("list_appointments", {"identifier": MASKED_PHONE},
                                  user_text=f"帮我查一下我的预约，我的手机号是 {FULL_PHONE}")
        first_request = json.dumps(client.calls[0], ensure_ascii=False)
        self.assertIn(MASKED_PHONE, first_request)
        self.assertEqual(len(agent.last_result["appointments"]), 2)

    def test_profile_masks_contact_fields(self):
        agent, client = self._run("patient_profile", {"patient_ref": "P7"})
        view = agent.last_result
        self.assertEqual(view["name"], "张三丰(虚构)")
        self.assertEqual(view["phone"], MASKED_PHONE)
        self.assertEqual(view["id_card"], MASKED_ID_CARD)

    def test_profile_single_field_masks_contact_field(self):
        agent, client = self._run("patient_profile",
                                  {"patient_ref": "P7", "field": "phone"})
        self.assertEqual(agent.last_result["phone"], MASKED_PHONE)

    def test_medications_and_bills_views(self):
        agent, client = self._run("list_medications", {"patient_ref": "P7"})
        self.assertEqual(len(agent.last_result["medications"]), 2)
        agent, client = self._run("list_bills", {"patient_ref": "P7"})
        self.assertEqual(len(agent.last_result["bills"]), 2)


if __name__ == "__main__":
    unittest.main()
