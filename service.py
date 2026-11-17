"""客服 Agent 主流程：模型选择工具 -> 执行 -> 工具结果回填模型 -> 生成回答。"""

import json

from model_client import ModelClient
from tools.bills import list_bills
from tools.medications import list_medications
from tools.patient_profile import patient_profile

TOOLS = {
    "patient_profile": patient_profile,
    "list_medications": list_medications,
    "list_bills": list_bills,
}


class CustomerServiceAgent:
    def __init__(self, model_client=None):
        self.model = model_client or ModelClient()
        self.last_result = None

    def _system_message(self):
        return {
            "role": "system",
            "content": ("你是医院客服助手。根据患者问题选择合适的工具，参数使用 patient_ref。"
                        "工具返回后用中文回答。不要编造工具未返回的信息。"),
            "tools": sorted(TOOLS),
        }

    def answer(self, user_text):
        first = self.model.send([
            self._system_message(),
            {"role": "user", "content": user_text},
        ])
        if not isinstance(first, dict) or "tool" not in first:
            return first if isinstance(first, str) else "请说明您想查询的内容。"

        name = first["tool"]
        if name not in TOOLS:
            return "暂不支持该查询。"
        arguments = first.get("arguments") or {}
        result = TOOLS[name](**arguments)
        self.last_result = result

        return self.model.send([
            self._system_message(),
            {"role": "user", "content": user_text},
            {"role": "assistant", "tool_call": {"name": name, "arguments": arguments}},
            {"role": "tool", "name": name, "content": result},
        ])
