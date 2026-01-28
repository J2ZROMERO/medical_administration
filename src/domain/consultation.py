from datetime import datetime

class Consultation:
    def __init__(self, id: str, patient_id: str, date_time: datetime):
        self.id = id
        self.patient_id = patient_id
        self.date_time = date_time
