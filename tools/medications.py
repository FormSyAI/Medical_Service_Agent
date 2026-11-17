"""工具：用药记录查询（已上线）。"""

from hospital_api import HospitalAPI
from patient_store import resolve_authorized_patient


def list_medications(patient_ref):
    patient_id = resolve_authorized_patient(patient_ref)
    return HospitalAPI().list_medications(patient_id)
