# Doktor Randevu & Hasta Takip — Proje Durum Dosyası

> Bu dosya, AI asistan için hazırlanmış teknik bağlam ve ilerleme kaydıdır.
> Güncellenme: 26 Nisan 2026

---

## 1. Proje Özeti

Küçük/orta ölçekli klinikler için **web tabanlı hasta yönetim sistemi** (EMR/HIS).

### Teknoloji Stack
| Katman | Teknoloji |
|---|---|
| Framework | Django 4.2.13, Python 3.11-slim |
| Veritabanı | PostgreSQL 15-alpine (`doktor-db-1`) |
| Reverse Proxy | Nginx 1.25-alpine, port **8200** → 80 |
| WSGI | Gunicorn 21.2.0, 3 worker, `0.0.0.0:8000` |
| Auth | `AUTH_USER_MODEL = 'accounts.CustomUser'` |
| Forms | django-crispy-forms 2.1 + crispy-bootstrap5 0.7 |
| Env | python-decouple 3.8 → `.env` dosyasını okur |
| PDF | reportlab 4.0.9 + xhtml2pdf 0.2.15 |
| Filtre | django-filters |

### Kritik Kural: Env Değişkenleri
`python-decouple` OS env değil **`.env` dosyasını** okur.
Bu yüzden `docker compose restart` yetmez, `--force-recreate` gerekir.

---

## 2. Docker Altyapısı

```
docker compose up -d --force-recreate web   # env değişikliği sonrası
docker compose restart web                  # sadece kod değişikliği sonrası
docker compose exec web sh -c "..."         # shell komutu çalıştırma
```

Çalışan containerlar: `doktor-db-1`, `doktor-web-1`, (nginx varsa)
URL: `http://localhost:8200`

---

## 3. Kullanıcı Rolleri ve Varsayılan Hesaplar

```python
class Role(TextChoices):
    ADMIN      = 'ADMIN'       # Sistem Yöneticisi
    DOCTOR     = 'DOCTOR'      # Doktor
    SECRETARY  = 'SECRETARY'   # Sekreter (varsayılan rol)
    ACCOUNTANT = 'ACCOUNTANT'  # Muhasebe
    PATIENT    = 'PATIENT'     # Hasta
```

Varsayılan admin: `admin / Admin1234!`

`CustomUser` üzerinde property'ler var: `is_admin`, `is_doctor`, `is_secretary`, `is_accountant`

### Doctor Modeli (appointments.Doctor)
`Doctor` ayrı bir modeldir, `CustomUser`'a OneToOne bağlıdır. DOCTOR rolündeki kullanıcılar için bu profil **ayrıca** oluşturulmalıdır.
→ `accounts/views.py`'de `UserCreateView` ve `UserUpdateView` içinde `Doctor.objects.get_or_create(user=user)` ile otomatik oluşturuluyor.

---

## 4. Uygulama Modülleri (Django Apps)

```
app/
├── accounts/      # CustomUser, rol yönetimi, kullanıcı CRUD
├── appointments/  # Doctor, Branch, Appointment modelleri
├── core/          # AuditLog, mixin'ler, ortak araçlar
├── documents/     # Hasta belgesi yükleme
├── examinations/  # Muayene kaydı (EMR çekirdeği)
├── patients/      # Patient, PatientMedicalInfo, PatientConsent
├── payments/      # Ödeme kayıtları
├── prescriptions/ # Reçete ve ilaç kalemleri
├── reports/       # İstatistik/grafik sayfaları
└── config/        # settings.py, urls.py
```

---

## 5. Önemli URL'ler

```
/                                              → dashboard
/hastalar/                                     → patients:list
/hastalar/<pk>/                                → patients:detail
/hastalar/yeni/                                → patients:create
/hastalar/<pk>/onamlar/                        → patients:consents (KVKK)
/randevular/                                   → appointments:list
/randevular/<pk>/                              → appointments:detail
/randevular/yeni/                              → appointments:create
/muayeneler/                                   → examinations:list
/muayeneler/hasta/<patient_pk>/yeni/           → examinations:create
/muayeneler/hasta/<p_pk>/randevu/<a_pk>/yeni/  → examinations:create_from_appointment
/muayeneler/<pk>/                              → examinations:detail
/muayeneler/<pk>/duzenle/                      → examinations:update
/receteler/muayene/<examination_pk>/yeni/      → prescriptions:create
/receteler/<pk>/                               → prescriptions:detail
/receteler/<pk>/pdf/                           → prescriptions:pdf
/belgeler/hasta/<patient_pk>/                  → documents:list
/odemeler/                                     → payments:list
/raporlar/                                     → reports:dashboard
/kullanicilar/                                 → accounts:user_list
/bildirimler/                                  → core:notifications
/bildirimler/sayac/                            → core:notification_count (JSON)
/sekreter/                                     → core:secretary_dashboard
/django-admin/                                 → Django admin
```

---

## 6. Crispy Forms Kuralı (KRİTİK)

`{% crispy form %}` kendi `<form>` tag'ını oluşturur → template'de zaten `<form>` varsa **iç içe form** hatası oluşur ve submit çalışmaz.

**Doğru kullanım:** `{{ form|crispy }}` veya `{{ field|as_crispy_field }}`

Düzeltilen template'ler:
- `accounts/user_form.html`
- `appointments/form.html`
- `payments/form.html`
- `patients/medical_form.html`
- `accounts/change_password.html`

---

## 7. Düzeltilen Hatalar (Tamamlanan Fixes)

| # | Hata | Kök Neden | Düzeltme |
|---|---|---|---|
| 1 | CSRF 403 | `CSRF_TRUSTED_ORIGINS` eksik | `settings.py` + `.env`'e eklendi |
| 2 | Login sonrası 500 | `base.html`'de çift `{% block content %}` | `{% else %}` branch'teki kopya silindi |
| 3 | Form submit olmuyor | `{% crispy form %}` iç içe `<form>` yaratıyor | 5 template'de `{{ form|crispy }}`'ye geçildi |
| 4 | Doktor eklenemiyor | `Doctor` profili ayrı oluşturulmalı | `UserCreateView`/`UserUpdateView`'da otomatik create |
| 5 | Randevu detay 500 | `statuses.split:","` geçersiz Django template syntax | 6 adet hardcoded buton ile değiştirildi |
| 6 | Admin muayene oluşturamıyor | `DoctorRequiredMixin` admin'i engelliyor + `doctor_profile` AttributeError | Mixin kaldırıldı, form'a `user` kwarg + doktor seçici eklendi |
| 7 | "Yeni Muayene" butonu admin'e görünmüyor | `{% if user.is_doctor %}` | `{% if user.is_doctor or user.is_admin %}` yapıldı |
| 8 | Muayene detay 500 | `{% for field, label in examination.xxx %}` geçersiz syntax | Bozuk satır silindi |
| 9 | `ExaminationForm` user kwarg çalışmıyor | Dosyada duplicate `ExaminationForm` sınıfı vardı, eski olan override ediyordu | Eski sınıf silindi |
| 10 | Hasta bakiye listesinde yanlış değerler | `Sum()` + çoklu FK traversal → JOIN satır çarpımı | `Subquery()` ile yeniden yazıldı |
| 11 | `payments/list.html` çift içerik | Template replace eski içeriği koruyordu | Shell ile ilk 96 satır korundu |
| 12 | Reçete arama 500 hatası | `patient__first_name`/`last_name` yerine `patient__name`/`surname` olmalı | Alan adları düzeltildi |
| 13 | Reçete kayıt sessiz başarısız | Template'de `status` inputu yok, form `fields=['note','status']` bekliyordu | `status` formdan çıkarıldı, view'da `ACTIVE` set ediliyor |
| 14 | Reçete `frequency`/`dosage` zorunlu alan | Model'de `blank=True` yok + formda `required` override yok → JS'siz submit başarısız | Model güncellendi, migration uygulandı, formda `required=False` || 16 | Dashboard 500 hatası | `dashboard.html` içinde hatalı `{% endblock %}` 259. satırda erken kapanıyordu | Fazla `{% endblock %}` silindi |
| 17 | Raporlar 500 hatası | `reports/views.py`'de `.filter(payment_status='PAID')` kaldırılmış alan | Filtre satırları silindi |
---

## 8. Mevcut Kod Durumu

### Cari Hesap (Ödeme) Modeli — YENİDEN YAZILDI

**`app/payments/models.py`** — Basitleştirilmiş `Payment` modeli:
```python
class Payment(models.Model):
    patient = FK(Patient, related_name='payments')
    amount = DecimalField(max_digits=10, decimal_places=2)
    payment_type = CharField(choices=[CASH,CARD,TRANSFER,INSURANCE,OTHER])
    description = CharField(max_length=300, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    # KALDIRILDI: examination, appointment, service, payment_status, discount
```

**`app/examinations/models.py`** — `ExaminationService` eklendi:
```python
class ExaminationService(models.Model):
    examination = FK(Examination, related_name='services')
    service = FK('payments.Service', null=True, blank=True)
    description = CharField(max_length=300)
    amount = DecimalField(max_digits=10, decimal_places=2)
    discount = DecimalField(max_digits=10, decimal_places=2, default=0)
    @property
    def net_amount(self): return self.amount - self.discount
```

**`app/patients/views.py`** — `_balance_annotations()` Subquery ile:
```python
def _balance_annotations(qs):
    charges_subq = ExaminationService.objects\
        .filter(examination__patient=OuterRef('pk'))\
        .values('examination__patient')\
        .annotate(t=Sum(F('amount') - F('discount'))).values('t')
    payments_subq = Payment.objects\
        .filter(patient=OuterRef('pk'))\
        .values('patient').annotate(t=Sum('amount')).values('t')
    return qs.annotate(
        total_charges=Coalesce(Subquery(charges_subq), Value(0)),
        total_payments=Coalesce(Subquery(payments_subq), Value(0)),
    )
```
Bakiye formülü: `net_balance = total_payments - total_charges` (pozitif=alacak, negatif=borç)

**Migrations:** `payments/0002_data_migration`, `0003_remove_old_fields`, `examinations/0002_examinationservice` — hepsi uygulandı ✅

---

### Reçete Modülü — DÜZELTİLDİ

**`app/prescriptions/models.py`**:
- `PrescriptionItem.dosage` ve `frequency` → `blank=True` eklendi
- Migration: `prescriptions/0002_fix_optional_fields` uygulandı ✅

**`app/prescriptions/forms.py`**:
- `PrescriptionForm.fields = ['note']` (status kaldırıldı)
- `PrescriptionItemForm.__init__`: `frequency.required = False`, `dosage.required = False`

**`app/prescriptions/views.py`**:
- `PrescriptionCreateView.form_valid`: `form.instance.status = 'ACTIVE'` set ediliyor
- `PrescriptionListView.get_queryset`: `patient__name`/`patient__surname` kullanıyor
- `PrescriptionPrintView` eklendi → `prescriptions/print.html`

**`app/prescriptions/urls.py`**: `path('<int:pk>/yazdir/', PrescriptionPrintView, name='print')` eklendi

**`app/templates/prescriptions/print.html`**: Tarayıcı baskısı için HTML reçete sayfası ✅

---

### `app/examinations/forms.py`
```python
class ExaminationForm(forms.ModelForm):
    doctor = ModelChoiceField(queryset=Doctor.objects.filter(status=True), required=False)
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'doctor_profile'):
            self.fields['doctor'].widget = HiddenInput()  # doktordan gizle
            self.fields['doctor'].required = False
        else:
            self.fields['doctor'].required = True  # admin için zorunlu
```

### `app/examinations/views.py`
- `ExaminationCreateView(LoginRequiredMixin, CreateView)` — DoctorRequiredMixin YOK
- `get_form_kwargs()` → `kwargs['user'] = self.request.user` geçirir
- `form_valid()` → `hasattr(user, 'doctor_profile')` ile dal ayırımı

### `app/templates/patients/detail.html`
- "Yeni Muayene" butonu: `{% if user.is_doctor or user.is_admin %}`

### `app/templates/appointments/detail.html`
- "Muayene Başlat" butonu: `{% if user.is_doctor or user.is_admin %}`
- Status butonları: hardcoded HTML (CONFIRMED, ARRIVED, IN_EXAM, COMPLETED, NO_SHOW, CANCELLED)

---

## 9. Test Sonuçları (Son Çalışma Durumu)

Admin (`admin`) ile tüm kritik URL'ler 200 döndürüyor (26 Nisan 2026):
```
✅ 200 Dashboard
✅ 200 Muayene Listesi
✅ 200 Hasta Detay
✅ 200 KVKK Onamlar
✅ 200 Sekreter Paneli
✅ 200 Bildirimler
✅ 200 Belgeler (hasta bazlı)
✅ 200 Randevular
✅ 200 Receteler
✅ 200 Odemeler
✅ 200 Raporlar
```

## 10. Gereksinim Dokümanı vs. Mevcut Durum

### ✅ Tamamlanmış / Çalışan
- Hasta yönetimi (4.1) — CRUD, sağlık bilgileri, belgeler, ödemeler tab'ları
- Randevu/takvim (4.2) — liste, detay, oluştur, durum güncelleme
- Muayene/EMR (4.3) — liste (tarih filtresi), oluştur (admin+doktor), detay, güncelle, vital bulgular
- Reçete (4.4) — muayeneye bağlı oluştur, detay, PDF, baskı sayfası, liste+arama
- Belgeler (4.5) — hasta bazlı yükleme, **kategori filtresi + renkli badge**
- Cari Hesap / Ödemeler (4.10) — ExaminationService + Payment ayrımı, hasta bakiye (Subquery), kasa defteri
- Raporlar (4.11) — temel grafikler, aylık gelir, istatistikler
- Yetkilendirme (4.12) — rol tabanlı, audit log
- **Bildirim altyapısı (4.9)** — sistem içi bildirim, bell icon, 60s polling, okundu işaretleme ✅
- **KVKK modülü (4.13)** — PatientConsent modeli, onam kayıt + listeleme, hasta detay entegrasyonu ✅
- **Doktor paneli (4.6)** — bugünkü muayene sayısı, ARRIVED hasta uyarısı, kontrol hatırlatıcı ✅
- **Sekreter paneli** — hasta karşılama, durum butonları (Geldi/İptal/Gelmedi), hızlı erişim ✅
- **Reçete düzenleme** — kayıtlı reçete edit view + ilaç kalemlerini değiştirme ✅ YENİ
- **Muayene şablonları** — ExaminationTemplate CRUD, form'da "Şablon Uygula" dropdown + JS auto-fill ✅ YENİ
- **ICD-10 autocomplete** — `icd10_code` alanında datalist autocomplete, AJAX search endpoint ✅ YENİ

### ⚠️ Kısmen Var / Eksik Özellikler
- (yok — tüm planlanan özellikler tamamlandı)

### ❌ Hiç Yapılmamış
- **Online randevu / hasta portalı (4.8)**: yok
- **Sıra/bekleme yönetimi**: yok
- **e-Fatura, e-Reçete, MEDULA**: yok (scope dışı)

---

## 11. Bir Sonraki Adımlar (Öncelik Sırasıyla)

1. **Hasta randevu hatırlatıcı** — e-mail veya SMS (celery task)
2. **Online randevu / hasta portalı** — public URL ile randevu alma (4.8)
3. **Sıra/bekleme ekranı** — bekleme odasında gösterim
4. **İlaç etkileşim uyarısı** — reçete yazarken basit kontrol

---

## 12. Bilinenler / Dikkat Edilecekler

- **Template cache**: `docker compose restart` sonrası eski template cache kalabilir → `--force-recreate` ile temizlenir
- **DoctorRequiredMixin**: `core/mixins.py`'de var, artık Examination view'larında KULLANILMIYOR
- **VitalSigns prefix**: Form POST'ta `vitals-fieldname` prefix'i kullanılıyor
- **AppointmentStatus**: `PENDING, CONFIRMED, ARRIVED, IN_EXAM, COMPLETED, CANCELLED, NO_SHOW, RESCHEDULED`
- **PatientMedicalInfo**: hasta oluşturulurken `get_or_create` ile otomatik oluşturuluyor
- **AuditLog**: `core.mixins.create_audit_log()` ile tüm CRUD işlemleri loglanıyor
- **Belgeler URL'i**: `/belgeler/` genel route YOK, hasta bazlı `/belgeler/hasta/<pk>/` şeklinde
- **Payment.payment_status** alanı KALDIRILDI — `reports/views.py` ve `core/views.py` güncellendi
- **PatientConsent.ConsentType**: `KVKK, COMMUNICATION, TREATMENT, SURGERY, PHOTOGRAPHY, OTHER`
- **Notification modeli**: `core.models.Notification` — recipient, type, title, message, link, is_read
- **Sekreter paneli URL**: `/sekreter/` → `core:secretary_dashboard`, sidebar'da sadece `is_secretary` için görünür
