from pydantic import BaseModel, Field

# --- Kategori Skrining ---

class CardioScreening(BaseModel):
    riwayat_hipertensi_dm: bool = Field(..., description="Apakah pernah dinyatakan Hipertensi/DM?")
    riwayat_kardiovaskular: bool = Field(..., description="Apakah pernah Stroke/Jantung/Ginjal?")
    keluarga_ptm: bool = Field(..., description="Apakah keluarga inti sakit PTM (Penyakit Tidak Menular)?")
    merokok: bool = Field(..., description="Apakah merokok?")
    alkohol: bool = Field(..., description="Apakah mengkonsumsi alkohol?")
    aktivitas_fisik_kurang: bool = False 

class DiabetesMellitus(BaseModel):
    hipertensi: bool = Field(..., description="Apakah Anda menderita Hipertensi?")

class Thalasemia(BaseModel):
    riwayat_keluarga_thalasemia_trfdarah: bool = Field(..., description="Apakah keluarga inti pernah didiagnosis Thalasemia atau menjalani transfusi darah rutin?")
    riwayat_keluarga_sifat_thalasemia: bool = Field(..., description="Apakah keluarga inti pernah didiagnosis sebagai pembawa sifat Thalasemia?")

class TBC(BaseModel):
    kontak_tbc: bool = Field(..., description="Apakah pernah kontak serumah dengan penderita TBC?")
    riwayat_dm: bool = Field(..., description="Apakah pernah dinyatakan menderita Diabetes Melitus?")
    hiv: bool = Field(..., description="Apakah Anda penderita HIV (ODHIV)?")
    batuk_2_minggu: bool = Field(..., description="Apakah sedang mengalami batuk lebih dari 2 minggu?")

class HepatitisBnC(BaseModel):
    # Gabungan pertanyaan Hep B dan C untuk efisiensi input
    hbsag_positif: bool = Field(..., description="Riwayat pemeriksaan HBsAg reaktif/positif?")
    keluarga_hepatitis_b: bool = Field(..., description="Keluarga inti mengidap Hepatitis B?")
    sex_berisiko_hep_b: bool = Field(..., description="Hubungan seksual berisiko (Hep B)?")
    sex_berisiko_hep_c: bool = Field(..., description="Hubungan seksual berisiko (Hep C)?")
    riwayat_tfdarah: bool = Field(..., description="Riwayat transfusi darah?")
    riwayat_cucidarah: bool = Field(..., description="Riwayat cuci darah/hemodialisa?")
    napza: bool = Field(..., description="Pengguna NAPZA suntik?")
    hiv_positif: bool = Field(..., description="Mengidap HIV positif?")
    riwayat_pengobatan_hepatitisc: bool = Field(..., description="Riwayat pengobatan Hepatitis C tapi tidak sembuh?")

# --- Wrapper Utama --- 

class ScreeningInput(BaseModel):
    """
    Wrapper untuk semua kategori skrining. 
    Input JSON harus mengikuti struktur ini. 
    """
    cardio: CardioScreening 
    dm: DiabetesMellitus 
    thalasemia: Thalasemia 
    tbc: TBC 
    hepatitisbnc: HepatitisBnC