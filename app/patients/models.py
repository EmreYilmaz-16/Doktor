from django.db import models


class PatientStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Aktif'
    PASSIVE = 'PASSIVE', 'Pasif'


class Gender(models.TextChoices):
    MALE = 'M', 'Erkek'
    FEMALE = 'F', 'Kadın'
    OTHER = 'O', 'Diğer'


class BloodType(models.TextChoices):
    A_POS = 'A+', 'A+'
    A_NEG = 'A-', 'A-'
    B_POS = 'B+', 'B+'
    B_NEG = 'B-', 'B-'
    AB_POS = 'AB+', 'AB+'
    AB_NEG = 'AB-', 'AB-'
    O_POS = 'O+', 'O+'
    O_NEG = 'O-', 'O-'
    UNKNOWN = '?', 'Bilinmiyor'


class Patient(models.Model):
    identity_no = models.CharField(max_length=20, blank=True, verbose_name='T.C. / Pasaport No')
    name = models.CharField(max_length=100, verbose_name='Ad')
    surname = models.CharField(max_length=100, verbose_name='Soyad')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True, verbose_name='Cinsiyet')
    phone = models.CharField(max_length=20, verbose_name='Telefon')
    email = models.EmailField(blank=True, verbose_name='E-posta')
    address = models.TextField(blank=True, verbose_name='Adres')
    blood_type = models.CharField(max_length=3, choices=BloodType.choices, default=BloodType.UNKNOWN, verbose_name='Kan Grubu')
    emergency_contact_name = models.CharField(max_length=150, blank=True, verbose_name='Acil Kişi Adı')
    emergency_contact_phone = models.CharField(max_length=20, blank=True, verbose_name='Acil Kişi Telefonu')
    insurance_info = models.CharField(max_length=200, blank=True, verbose_name='Sigorta Bilgisi')
    occupation = models.CharField(max_length=100, blank=True, verbose_name='Meslek')
    notes = models.TextField(blank=True, verbose_name='Notlar / Uyarılar')
    status = models.CharField(max_length=10, choices=PatientStatus.choices, default=PatientStatus.ACTIVE, verbose_name='Durum')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hasta'
        verbose_name_plural = 'Hastalar'
        ordering = ['surname', 'name']

    def __str__(self):
        return f'{self.name} {self.surname}'

    @property
    def full_name(self):
        return f'{self.name} {self.surname}'

    @property
    def age(self):
        if not self.birth_date:
            return None
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )


class PatientMedicalInfo(models.Model):
    patient = models.OneToOneField(
        Patient, on_delete=models.CASCADE, related_name='medical_info', verbose_name='Hasta'
    )
    allergies = models.TextField(blank=True, verbose_name='Alerjiler')
    chronic_diseases = models.TextField(blank=True, verbose_name='Kronik Hastalıklar')
    regular_medicines = models.TextField(blank=True, verbose_name='Sürekli Kullanılan İlaçlar')
    surgeries = models.TextField(blank=True, verbose_name='Geçirilmiş Ameliyatlar')
    family_history = models.TextField(blank=True, verbose_name='Aile Hastalık Geçmişi')
    smoking = models.CharField(max_length=50, blank=True, verbose_name='Sigara')
    alcohol = models.CharField(max_length=50, blank=True, verbose_name='Alkol')
    pregnancy_info = models.CharField(max_length=100, blank=True, verbose_name='Gebelik Bilgisi')
    special_notes = models.TextField(blank=True, verbose_name='Özel Notlar')

    class Meta:
        verbose_name = 'Tıbbi Bilgi'
        verbose_name_plural = 'Tıbbi Bilgiler'

    def __str__(self):
        return f'{self.patient.full_name} - Tıbbi Bilgi'


class PatientConsent(models.Model):
    class ConsentType(models.TextChoices):
        KVKK = 'KVKK', 'KVKK Aydınlatma Metni'
        COMMUNICATION = 'COMMUNICATION', 'İletişim İzni'
        TREATMENT = 'TREATMENT', 'Tedavi Onamı'
        SURGERY = 'SURGERY', 'Ameliyat Onamı'
        PHOTOGRAPHY = 'PHOTOGRAPHY', 'Fotoğraf / Video İzni'
        OTHER = 'OTHER', 'Diğer'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consents', verbose_name='Hasta')
    consent_type = models.CharField(max_length=20, choices=ConsentType.choices, default=ConsentType.KVKK, verbose_name='Onay Türü')
    approved = models.BooleanField(default=False, verbose_name='Onaylandı')
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name='Onay Tarihi')
    approved_by = models.ForeignKey(
        'accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Kaydeden', related_name='recorded_consents',
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP Adresi')
    consent_text_version = models.CharField(max_length=20, default='1.0', verbose_name='Metin Versiyonu')
    notes = models.TextField(blank=True, verbose_name='Notlar')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'KVKK Onay'
        verbose_name_plural = 'KVKK Onayları'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.patient.full_name} — {self.get_consent_type_display()} — {"✓" if self.approved else "✗"}'
