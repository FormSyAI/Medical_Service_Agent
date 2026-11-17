"""模型客户端：本机演示写请求日志，不访问外网。"""

import json
import os

EVIDENCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence")
REQUEST_LOG = os.path.join(EVIDENCE_DIR, "model-requests.jsonl")


class ModelClient:
    def __init__(self, log_path=None):
        self.log_path = log_path or REQUEST_LOG

    def send(self, messages):
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"event": "model_request", "messages": messages},
                                ensure_ascii=False) + "\n")
        if messages[-1]["role"] == "user":
            return {"tool": "patient_profile", "arguments": {"patient_ref": "P7"}}
        return "已为您查询。"
