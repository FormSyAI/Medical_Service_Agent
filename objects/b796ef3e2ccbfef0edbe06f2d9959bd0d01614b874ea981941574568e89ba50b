"""工具：患者档案查询（已上线）。"""

from hospital_api import HospitalAPI
from patient_store import resolve_authorized_patient


def patient_profile(patient_ref, field=None):
    patient_id = resolve_authorized_patient(patient_ref)
    result = HospitalAPI().patient_profile(patient_id)
    if field:
        return {field: result["patient"].get(field)}
    return result
