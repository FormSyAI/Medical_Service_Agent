"""患者身份：以手机号或身份证号作为唯一键。"""

PATIENTS = {
    "P7": {"patient_id": 7001, "name": "张三丰(虚构)",
           "phone": "13900001234", "id_card": "110105199003074219"},
    "P8": {"patient_id": 7002, "name": "李四合(虚构)",
           "phone": "13800005678", "id_card": "310101198512061234"},
}

# 手机号 / 身份证号 -> patient_ref
_BY_PHONE = {p["phone"]: ref for ref, p in PATIENTS.items()}
_BY_ID_CARD = {p["id_card"]: ref for ref, p in PATIENTS.items()}

# 登录人（P7）与其已授权家属
SESSION = {"login_patient_ref": "P7", "authorized_refs": {"P7", "P8"}}


def find_by_identifier(value):
    """用手机号或身份证号定位 patient_ref；找不到返回 None。"""
    if not isinstance(value, str):
        return None
    value = value.strip()
    return _BY_PHONE.get(value) or _BY_ID_CARD.get(value)


def resolve_authorized_patient(patient_ref):
    if patient_ref not in SESSION["authorized_refs"]:
        raise PermissionError(f"当前登录身份无权访问 {patient_ref}")
    return PATIENTS[patient_ref]["patient_id"]
