"""院内业务接口（工作站风格），返回完整业务对象。"""

from patient_store import PATIENTS

APPOINTMENTS = {
    "A12": {"patient_ref": "P7", "date": "2026-11-17", "time": "09:30",
            "department": "内科", "status": "已预约"},
    "A13": {"patient_ref": "P7", "date": "2026-11-18", "time": "14:00",
            "department": "口腔科", "status": "待就诊"},
    "A21": {"patient_ref": "P8", "date": "2026-11-17", "time": "10:15",
            "department": "内科", "status": "已预约"},
}

MEDICATIONS = {
    "P7": [{"name": "二甲双胍", "dose": "0.5g", "frequency": "每日两次"},
           {"name": "阿托伐他汀", "dose": "20mg", "frequency": "每晚一次"}],
}

BILLS = {
    "P7": [{"item": "门诊诊查费", "amount": "50.00", "date": "2026-11-10"},
           {"item": "血常规", "amount": "35.00", "date": "2026-11-10"}],
}


class HospitalAPI:
    def query_appointments(self, patient_id, date=None):
        ref = next(r for r, p in PATIENTS.items() if p["patient_id"] == patient_id)
        rows = [{"appointment_id": a, **v} for a, v in APPOINTMENTS.items()
                if v["patient_ref"] == ref]
        if date:
            rows = [row for row in rows if row["date"] == date]
        return {"patient": dict(PATIENTS[ref]), "appointments": rows}

    def patient_profile(self, patient_id):
        ref = next(r for r, p in PATIENTS.items() if p["patient_id"] == patient_id)
        return {"patient": dict(PATIENTS[ref])}

    def list_medications(self, patient_id):
        ref = next(r for r, p in PATIENTS.items() if p["patient_id"] == patient_id)
        return {"patient": dict(PATIENTS[ref]), "medications": MEDICATIONS.get(ref, [])}

    def list_bills(self, patient_id):
        ref = next(r for r, p in PATIENTS.items() if p["patient_id"] == patient_id)
        return {"patient": dict(PATIENTS[ref]), "bills": BILLS.get(ref, [])}
