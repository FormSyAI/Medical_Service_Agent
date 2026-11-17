"""客服 Agent 主流程：模型选择工具 -> 执行 -> 工具结果回填模型 -> 生成回答。"""

import json

from model_client import ModelClient
from privacy import mask_id_card, mask_phone, restore_arguments, sanitize_messages
from tools.appointments import list_appointments
from tools.bills import list_bills
from tools.medications import list_medications
from tools.patient_profile import patient_profile

TOOLS = {
    "patient_profile": patient_profile,
    "list_medications": list_medications,
    "list_bills": list_bills,
    "list_appointments": list_appointments,
}


def _model_view(name, arguments, result):
    """把工具结果投影为可回填给模型的最小字段：完整手机号、身份证号不进入模型请求。"""
    patient_ref = arguments.get("patient_ref") or result.get("patient_ref")
    if name == "patient_profile":
        if "patient" in result:
            patient = result["patient"]
            view = {"patient_ref": patient_ref, "name": patient.get("name")}
            if patient.get("phone"):
                view["phone"] = mask_phone(patient["phone"])
            if patient.get("id_card"):
                view["id_card"] = mask_id_card(patient["id_card"])
            return view
        view = {"patient_ref": patient_ref}
        for field, value in result.items():
            if field == "phone":
                view["phone"] = mask_phone(value)
            elif field == "id_card":
                view["id_card"] = mask_id_card(value)
            elif field != "patient_id":
                view[field] = value
        return view
    if name == "list_appointments":
        return {
            "patient_ref": patient_ref,
            "appointments": [
                {
                    "date": row.get("date"),
                    "time": row.get("time"),
                    "department": row.get("department"),
                    "status": row.get("status"),
                }
                for row in result.get("appointments", [])
            ],
        }
    if name in ("list_medications", "list_bills"):
        key = "medications" if name == "list_medications" else "bills"
        return {"patient_ref": patient_ref, key: result.get(key, [])}
    raise ValueError(f"没有为工具 {name} 定义可回填模型的视图")


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

    def _send(self, messages):
        """所有模型请求统一经此脱敏后发出：完整手机号、身份证号不进入请求体。"""
        return self.model.send(sanitize_messages(messages))

    def answer(self, user_text):
        first = self._send([
            self._system_message(),
            {"role": "user", "content": user_text},
        ])
        if not isinstance(first, dict) or "tool" not in first:
            return first if isinstance(first, str) else "请说明您想查询的内容。"

        name = first["tool"]
        if name not in TOOLS:
            return "暂不支持该查询。"
        arguments = restore_arguments(first.get("arguments") or {})
        result = TOOLS[name](**arguments)
        view = _model_view(name, arguments, result)
        self.last_result = view

        return self._send([
            self._system_message(),
            {"role": "user", "content": user_text},
            {"role": "assistant", "tool_call": {"name": name, "arguments": arguments}},
            {"role": "tool", "name": name, "content": view},
        ])
