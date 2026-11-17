"""个人信息保护：完整手机号、身份证号不进入模型请求；进程内解析身份仍用完整值。"""

import re

from patient_store import PATIENTS

_PHONE_RE = re.compile(r"(?<!\d)1\d{10}(?!\d)")
_ID_CARD_RE = re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)")


def mask_phone(phone):
    """手机号脱敏展示：139****1234。"""
    if isinstance(phone, str) and len(phone) >= 8:
        return phone[:3] + "****" + phone[-4:]
    return "****"


def mask_id_card(id_card):
    """身份证号脱敏展示：仅保留前 3 位与后 4 位。"""
    if isinstance(id_card, str) and len(id_card) >= 8:
        return id_card[:3] + "*" * (len(id_card) - 7) + id_card[-4:]
    return "****"


def mask_text(text):
    """替换自由文本中的完整手机号/身份证号；对已脱敏文本为幂等操作。"""
    if not isinstance(text, str):
        return text
    text = _ID_CARD_RE.sub(lambda match: mask_id_card(match.group(0)), text)
    return _PHONE_RE.sub(lambda match: mask_phone(match.group(0)), text)


def _mask_value(value):
    if isinstance(value, str):
        return mask_text(value)
    if isinstance(value, list):
        return [_mask_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _mask_value(item) for key, item in value.items()}
    return value


def sanitize_messages(messages):
    """返回脱敏后的 messages 副本；不改动调用方数据。"""
    return [_mask_value(message) for message in messages]


def restore_identifier(value):
    """把模型侧回传的脱敏手机号/身份证号在进程内还原为完整值，其余原样返回。"""
    if not isinstance(value, str):
        return value
    candidate = value.strip()
    for patient in PATIENTS.values():
        if candidate == mask_phone(patient["phone"]):
            return patient["phone"]
        if candidate == mask_id_card(patient["id_card"]):
            return patient["id_card"]
    return value


def restore_arguments(arguments):
    """还原工具调用参数，供进程内身份解析使用完整值。"""
    return {key: restore_identifier(value) for key, value in arguments.items()}
