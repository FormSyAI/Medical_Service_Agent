"""模型客户端：本机演示按意图选择工具并写请求日志，不访问外网。"""

import json
import os
import re

from patient_store import PATIENTS, SESSION

EVIDENCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence")
REQUEST_LOG = os.path.join(EVIDENCE_DIR, "model-requests.jsonl")

_IDENTIFIER_RE = re.compile(r"(?<!\d)(?:\d{3}\*+\d{4}|\d{17}[\dXx]|1\d{10})(?!\d)")


def _identifier_in_text(text):
    """从消息文本中找出手机号/身份证号（完整或已脱敏形式）。"""
    if not isinstance(text, str):
        return None
    match = _IDENTIFIER_RE.search(text)
    return match.group(0) if match else None


class ModelClient:
    def __init__(self, log_path=None):
        self.log_path = log_path or REQUEST_LOG

    def send(self, messages):
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"event": "model_request", "messages": messages},
                                ensure_ascii=False) + "\n")
        if messages[-1]["role"] != "user":
            return "已为您查询。"
        text = messages[-1]["content"]
        if "预约" in text:
            identifier = _identifier_in_text(text)
            if identifier is None:
                identifier = PATIENTS[SESSION["login_patient_ref"]]["phone"]
            return {"tool": "list_appointments", "arguments": {"identifier": identifier}}
        return {"tool": "patient_profile",
                "arguments": {"patient_ref": SESSION["login_patient_ref"]}}
