"""工具：预约查询（已接入院内预约接口）。"""

from hospital_api import HospitalAPI
from patient_store import find_by_identifier, resolve_authorized_patient


def list_appointments(identifier, date=None):
    patient_ref = find_by_identifier(identifier)
    if patient_ref is None:
        raise ValueError(f"未找到与 {identifier} 匹配的患者")
    patient_id = resolve_authorized_patient(patient_ref)
    result = HospitalAPI().query_appointments(patient_id, date)
    return {"patient_ref": patient_ref, **result}
