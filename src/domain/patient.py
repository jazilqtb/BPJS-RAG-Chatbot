from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date

# -- Sub-Models ---

class MedicalHistoryItem(BaseModel):
    tanggal_pelayanan: date
    nama_klinik: str
    diagnosa: str
    keluhan: Optional[str] = None
    terapi: Optional[str] = None

class Geolocation(BaseModel):
    kelurahan: str
    kota: str
    lat: Optional[float] = None
    long: Optional[float] = None

class PatientProfile(BaseModel):
    id_peserta: str = Field(..., description="Anonymized ID")
    nama: str
    usia: int = Field(..., ge=0, le=120)
    gender: str = Field(..., pattern="^(L|P)$")
    domisili: Geolocation

# --- Main Context Model ---

class PatientContext(BaseModel):
    profile: PatientProfile
    medical_records: List[MedicalHistoryItem] = []

    @property
    def summary_text(self) -> str:
        """Helper untuk mengubah object jadi text ringkas bagi LLM"""
        history_str = "\n".join([f"- {r.tanggal_pelayanan}: {r.diagosa} ({r.terapi})" for r in self.medical_records])
        return (
            f"Pasien: {self.profile.nama} ({self.profile.usia}th, {self.profile.gender})\n"
            f"Domisili: {self.profile.domisili.kelurahan}, {self.profile.domisili.kota}\n"
            f"Riwayat Medis: \n{history_str if history_str else 'Tidak ada data'}"
        )