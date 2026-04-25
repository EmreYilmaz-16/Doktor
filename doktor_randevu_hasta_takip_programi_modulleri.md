# Doktor Randevu, Hasta Takip ve Muayene Yönetim Programı Gereksinim Dokümanı

> Amaç: Doktorların randevu alabilmesi, hasta bilgilerini yönetebilmesi, muayene sonuçlarını kaydedebilmesi, reçete yazabilmesi, geçmiş muayeneleri görebilmesi ve hasta belgelerini/resimlerini güvenli şekilde saklayabilmesi için web tabanlı bir klinik/muayenehane yönetim sistemi tasarlamak.

---

## 1. Genel Sistem Vizyonu

Bu program; küçük/orta ölçekli muayenehaneler, poliklinikler, özel klinikler veya çok doktorlu sağlık merkezleri için geliştirilecek bir **Hasta Takip + Randevu + Muayene + Reçete + Belge Yönetimi** uygulamasıdır.

Sistemin temel amacı:

- Hasta kayıtlarını tek merkezde toplamak
- Doktor randevularını yönetmek
- Muayene geçmişini kronolojik görmek
- Doktorun muayene notu, tanı, tetkik, reçete ve belge girişini kolaylaştırmak
- Hasta dosyalarını dijitalleştirmek
- Yetkiye göre güvenli erişim sağlamak
- Klinik iş akışını hızlandırmak

---

## 2. Benzer Uygulamalarda Görülen Ortak Modüller

Araştırılan klinik/practice management ve EMR/EHR sistemlerinde en sık görülen modüller şunlardır:

1. Randevu ve takvim yönetimi
2. Hasta kayıt ve hasta profili
3. Elektronik sağlık kaydı / muayene kaydı
4. Reçete ve ilaç yönetimi
5. Belge, laboratuvar sonucu, röntgen ve görsel dosya arşivi
6. Doktor paneli
7. Sekreter / danışma paneli
8. Hasta portalı
9. SMS, WhatsApp, e-posta bildirimleri
10. Faturalama / ödeme / kasa
11. Raporlama ve istatistik
12. Yetkilendirme ve güvenlik
13. Denetim kayıtları / işlem geçmişi
14. Çok doktorlu ve çok şubeli yapı
15. Şablonlar, hızlı notlar ve hazır reçete şablonları
16. Laboratuvar / radyoloji / tetkik entegrasyonu
17. Online randevu alma
18. Sıra / bekleme salonu yönetimi
19. Hasta onam formları
20. KVKK uyum ve veri güvenliği

---

## 3. Kullanıcı Rolleri

### 3.1 Sistem Yöneticisi

- Kullanıcı ekleme / silme / güncelleme
- Rol ve yetki tanımlama
- Klinik bilgilerini yönetme
- Doktor çalışma saatlerini tanımlama
- Sistem parametrelerini yönetme
- Log kayıtlarını görüntüleme
- Yedekleme ayarlarını yönetme

### 3.2 Doktor

- Kendi randevularını görüntüleme
- Hasta geçmişini görüntüleme
- Muayene kaydı oluşturma
- Tanı, şikayet, bulgu ve tedavi planı girme
- Reçete oluşturma
- Tetkik isteme
- Hasta belgelerini görüntüleme / yükleme
- Kontrol randevusu oluşturma
- Kendi raporlarını görüntüleme

### 3.3 Sekreter / Danışma

- Hasta kaydı oluşturma
- Randevu oluşturma / güncelleme / iptal etme
- Doktor takvimini görüntüleme
- Hasta kabul işlemi yapma
- Ödeme / tahsilat girişi yapma
- Hasta iletişim bilgilerini güncelleme
- Randevu hatırlatma gönderme

### 3.4 Hasta

Opsiyonel hasta portalı veya mobil arayüz için:

- Randevu talebi oluşturma
- Geçmiş randevularını görüntüleme
- Reçete ve muayene özetlerini görüntüleme
- Belge / tetkik sonucu yükleme
- Doktora mesaj gönderme
- Kişisel bilgilerini güncelleme

### 3.5 Muhasebe / Finans

- Tahsilat kayıtları
- Fatura / makbuz takibi
- Günlük kasa raporu
- Doktor bazlı gelir raporu
- Hizmet bazlı gelir analizi

---

## 4. Ana Modüller ve Yetenekler

## 4.1 Hasta Yönetimi Modülü

### Temel Hasta Kartı

Hasta için saklanabilecek bilgiler:

- Hasta ID
- T.C. kimlik no / pasaport no
- Ad soyad
- Doğum tarihi
- Cinsiyet
- Telefon
- E-posta
- Adres
- Kan grubu
- Acil durum kişisi
- Meslek
- Medeni durum
- Sigorta bilgisi
- Kayıt tarihi
- Aktif / pasif durumu

### Sağlık Bilgileri

- Kronik hastalıklar
- Alerjiler
- Sürekli kullanılan ilaçlar
- Geçirilmiş ameliyatlar
- Aile hastalık geçmişi
- Sigara / alkol bilgisi
- Gebelik bilgisi
- Özel notlar
- Risk uyarıları

### Hasta Geçmişi

- Geçmiş randevular
- Geçmiş muayeneler
- Reçeteler
- Tanılar
- Tedavi planları
- Yüklenen belgeler
- Laboratuvar / görüntüleme sonuçları
- Ödemeler
- Doktor notları

### Önerilen Özellikler

- Hasta hızlı arama
- Telefon, T.C. kimlik, ad soyad ile arama
- Hasta kartında kronolojik zaman çizelgesi
- Tekrarlı hasta kontrolü
- Hasta birleştirme özelliği
- Hasta etiketleri: VIP, kronik, riskli, kontrol bekliyor vb.
- Hasta notları ve uyarı kutusu

---

## 4.2 Randevu ve Takvim Yönetimi Modülü

### Temel Yetenekler

- Doktor bazlı takvim
- Günlük / haftalık / aylık görünüm
- Randevu oluşturma
- Randevu güncelleme
- Randevu iptal etme
- Randevu erteleme
- Randevu çakışma kontrolü
- Randevu süresi belirleme
- Doktor çalışma saatleri
- Resmi tatil / izin tanımı
- Randevusuz hasta kabulü
- Kontrol randevusu oluşturma

### Randevu Durumları

- Bekliyor
- Onaylandı
- Geldi
- Muayenede
- Tamamlandı
- İptal edildi
- Gelmedi
- Ertelendi

### Gelişmiş Özellikler

- SMS / WhatsApp / e-posta hatırlatma
- Otomatik hatırlatma şablonları
- No-show takibi
- Doktor doluluk oranı
- Online randevu talebi
- Hasta tarafından randevu iptali
- Randevu bekleme listesi
- Sıra numarası üretme
- Bekleme salonu ekranı
- Randevu notu
- Hizmet türüne göre süre belirleme

---

## 4.3 Muayene Yönetimi / EMR Modülü

Bu modül sistemin en kritik bölümüdür. Doktor, hastanın tüm klinik kaydını buradan yönetir.

### Muayene Kaydı Alanları

- Muayene tarihi
- Doktor
- Hasta
- Randevu bağlantısı
- Şikayet
- Hikaye / anamnez
- Fizik muayene bulguları
- Ön tanı
- Kesin tanı
- ICD-10 tanı kodu
- Tedavi planı
- Doktor notu
- Kontrol tarihi
- Tetkik istemleri
- Reçete bağlantısı
- Ek dosyalar
- Muayene sonucu
- Sonraki işlem önerisi

### Vital Bulgular

- Boy
- Kilo
- Vücut kitle indeksi
- Ateş
- Nabız
- Tansiyon
- Solunum sayısı
- Oksijen satürasyonu
- Kan şekeri
- Ağrı skoru

### Klinik Not Şablonları

- Genel muayene şablonu
- Dahiliye şablonu
- Çocuk hastalıkları şablonu
- Kadın doğum şablonu
- Göz muayenesi şablonu
- Diş muayenesi şablonu
- Fizik tedavi şablonu
- Psikiyatri görüşme şablonu
- Özel branş şablonları

### Gelişmiş Özellikler

- Önceki muayeneyi kopyalayarak yeni muayene oluşturma
- Hızlı not şablonları
- Sesle not alma
- Otomatik ICD-10 önerisi
- Muayene sırasında belge yükleme
- Doktor iç notu / hasta ile paylaşılabilir not ayrımı
- Klinik karar destek uyarıları
- Alerji ve ilaç etkileşim uyarısı
- Muayene çıktısı alma
- PDF rapor üretme

---

## 4.4 Reçete Yönetimi Modülü

### Temel Yetenekler

- Reçete oluşturma
- İlaç ekleme
- Doz, kullanım şekli, süre bilgisi girme
- Açıklama ekleme
- Reçete şablonu oluşturma
- Sık kullanılan ilaç listesi
- Hasta alerji uyarısı
- Reçete çıktısı / PDF
- Reçete geçmişi
- Aynı reçeteden tekrar oluşturma

### Reçete Alanları

- Reçete ID
- Hasta
- Doktor
- Muayene
- Reçete tarihi
- İlaç adı
- Etken madde
- Doz
- Kullanım sıklığı
- Kullanım süresi
- Kullanım talimatı
- Reçete açıklaması
- Tanı ilişkisi
- Doktor imzası
- Durum

### Gelişmiş Özellikler

- Hazır reçete şablonları
- İlaç veri tabanı entegrasyonu
- İlaç etkileşim kontrolü
- Alerji kontrolü
- Kronik ilaç takibi
- Barkod / karekod üretimi
- E-imza entegrasyonu
- E-reçete / MEDULA entegrasyonu için altyapı
- Reçete paylaşım linki
- Reçete PDF arşivi

> Not: Türkiye'de resmi e-reçete / MEDULA / Sağlık Bakanlığı entegrasyonları için mevzuat ve yetkili kurum süreçleri ayrıca araştırılmalı ve resmi entegrasyon izinleri alınmalıdır.

---

## 4.5 Belge, Resim ve Dosya Yönetimi Modülü

### Yüklenebilecek Dosyalar

- Laboratuvar sonucu
- Röntgen
- MR / BT görüntüsü
- Ultrason görüntüsü
- EKG
- Epikriz
- Önceki reçete
- Hasta onam formu
- Kimlik görüntüsü
- Sigorta belgesi
- Fotoğraf
- PDF rapor
- Word / Excel dosyası
- DICOM dosyası, ileri seviye için

### Özellikler

- Hasta kartına dosya yükleme
- Muayeneye bağlı dosya yükleme
- Dosya kategorilendirme
- Açıklama ekleme
- Dosya önizleme
- Dosya indirme
- Dosya silme / arşivleme
- Doktor bazlı erişim
- Hasta portalından belge yükleme
- Versiyonlama
- Dosya erişim logları
- Büyük dosya desteği
- Güvenli depolama
- Virüs taraması
- Dosya boyutu sınırı
- Dosya türü kısıtlaması

### Önerilen Kategoriler

- Laboratuvar
- Radyoloji
- Fotoğraf
- Onam Formu
- Reçete
- Rapor
- Kimlik / Sigorta
- Diğer

---

## 4.6 Doktor Paneli

Doktorun günlük iş akışını hızlıca yönetebileceği ana ekrandır.

### Ekran İçeriği

- Bugünkü randevular
- Sıradaki hasta
- Geciken randevular
- Muayene bekleyen hastalar
- Son muayene edilen hastalar
- Kontrol zamanı gelen hastalar
- Hızlı hasta arama
- Hızlı reçete oluşturma
- Hızlı muayene başlatma
- Hasta uyarıları
- Tamamlanmamış muayene kayıtları

### Gelişmiş Özellikler

- Doktor performans özeti
- Günlük hasta sayısı
- En sık tanılar
- En sık kullanılan reçeteler
- Açık görevler
- Kişisel notlar
- Takvim entegrasyonu

---

## 4.7 Sekreter / Hasta Kabul Paneli

### Temel Özellikler

- Hasta arama
- Yeni hasta kaydı
- Randevu oluşturma
- Randevu durum güncelleme
- Hasta geldi işaretleme
- Doktora yönlendirme
- Bekleme listesi
- Ödeme alma
- Makbuz oluşturma
- Günlük randevu listesi
- Randevu hatırlatma gönderme

### Kullanışlı Ek Özellikler

- Telefon araması sırasında hasta kartı açma
- Hızlı randevu ekranı
- Doktor uygunluk görünümü
- Randevu çakışma uyarısı
- Hasta borç uyarısı
- Hasta özel not uyarısı

---

## 4.8 Hasta Portalı / Mobil Hasta Ekranı

Opsiyonel ama güçlü bir modüldür.

### Hasta Tarafı Yetenekler

- Online randevu talebi
- Randevu geçmişi
- Reçete görüntüleme
- Muayene özeti görüntüleme
- Belge yükleme
- Laboratuvar sonuçlarını görüntüleme
- Doktora mesaj gönderme
- Ödeme geçmişi
- Kişisel bilgileri güncelleme
- Bildirim tercihleri
- KVKK onayları

### Güvenlik

- SMS doğrulama
- E-posta doğrulama
- İki faktörlü giriş
- Hasta verisi maskeleme
- Hasta sadece kendi kayıtlarını görebilmeli

---

## 4.9 Bildirim ve Hatırlatma Modülü

### Bildirim Kanalları

- SMS
- WhatsApp
- E-posta
- Mobil push bildirimi
- Sistem içi bildirim

### Kullanım Alanları

- Randevu hatırlatma
- Randevu iptali
- Randevu değişikliği
- Kontrol muayenesi hatırlatma
- Tetkik sonucu hazır bildirimi
- Ödeme hatırlatma
- Doğum günü mesajı
- Kampanya / duyuru
- Reçete yenileme hatırlatma

### Şablonlar

- Randevu onay mesajı
- Randevu hatırlatma mesajı
- Randevu iptal mesajı
- Kontrol hatırlatma mesajı
- Muayene sonrası bilgilendirme
- Ödeme hatırlatma

---

## 4.10 Faturalama, Ödeme ve Kasa Modülü

### Temel Özellikler

- Muayene ücreti tanımlama
- Hizmet / işlem tanımlama
- Tahsilat kaydı
- Nakit / kredi kartı / havale ödeme tipi
- Borç takibi
- İndirim uygulama
- Günlük kasa raporu
- Doktor bazlı gelir raporu
- Hasta ödeme geçmişi
- Makbuz / fatura çıktısı

### Gelişmiş Özellikler

- Paket hizmet satışı
- Taksitli ödeme
- Sigorta / kurum anlaşması
- e-Fatura / e-Arşiv entegrasyonu
- Cari hesap mantığı
- İade işlemleri
- Kasa kapatma işlemi

---

## 4.11 Raporlama ve İstatistik Modülü

### Operasyonel Raporlar

- Günlük randevu listesi
- Doktor bazlı randevu sayısı
- Gelmeyen hasta raporu
- İptal edilen randevu raporu
- Kontrol bekleyen hastalar
- Yeni hasta sayısı
- Aktif hasta sayısı

### Klinik Raporlar

- Tanı bazlı hasta listesi
- İlaç kullanım raporu
- Kronik hasta listesi
- Alerjisi olan hastalar
- Muayene sayıları
- Doktor performansı
- Branş bazlı işlem dağılımı

### Finansal Raporlar

- Günlük kasa
- Aylık gelir
- Doktor bazlı gelir
- Hizmet bazlı gelir
- Borçlu hastalar
- Tahsilat raporu
- İndirim raporu

### Yönetim Paneli Grafik Önerileri

- Günlük hasta sayısı grafiği
- Randevu doluluk oranı
- Yeni / tekrar gelen hasta oranı
- En yoğun saatler
- En yoğun doktorlar
- Gelmeyen randevu oranı
- Aylık gelir trendi

---

## 4.12 Yetkilendirme ve Güvenlik Modülü

Sağlık verileri özel nitelikli kişisel veri olduğu için bu modül kritik önemdedir.

### Güvenlik Gereksinimleri

- Kullanıcı adı / şifre
- Güçlü şifre politikası
- Rol bazlı yetkilendirme
- İki faktörlü doğrulama
- Oturum zaman aşımı
- IP kısıtlama
- Erişim logları
- Hasta dosyası görüntüleme logu
- Veri şifreleme
- Dosya şifreleme
- Yedekleme
- Geri yükleme
- Silinen kayıtları arşivleme
- KVKK aydınlatma ve açık rıza kayıtları
- Veriye erişim gerekçesi kaydı
- Hassas veri maskeleme

### Rol Bazlı Örnek Yetkiler

| İşlem | Admin | Doktor | Sekreter | Muhasebe | Hasta |
|---|---:|---:|---:|---:|---:|
| Hasta oluşturma | Evet | Evet | Evet | Hayır | Hayır |
| Hasta sağlık geçmişi görme | Evet | Evet | Kısıtlı | Hayır | Kendi |
| Muayene yazma | Hayır | Evet | Hayır | Hayır | Hayır |
| Reçete yazma | Hayır | Evet | Hayır | Hayır | Hayır |
| Randevu oluşturma | Evet | Evet | Evet | Hayır | Talep |
| Ödeme görme | Evet | Kısıtlı | Evet | Evet | Kendi |
| Dosya yükleme | Evet | Evet | Evet | Hayır | Kendi |
| Sistem ayarı | Evet | Hayır | Hayır | Hayır | Hayır |

---

## 4.13 KVKK ve Hukuki Uyum Modülü

### Saklanması Gereken Kayıtlar

- Aydınlatma metni onayı
- Açık rıza onayı
- İletişim izni
- Veri işleme amacı
- Onay tarihi
- Onay veren kullanıcı / hasta
- IP adresi
- Kullanılan metin versiyonu
- Onam formları
- Erişim logları
- Veri silme / anonimleştirme talepleri

### Önerilen KVKK Özellikleri

- Hasta kaydında KVKK onay durumu
- Onay metni versiyonlama
- Hasta verisi dışa aktarma
- Hasta silme / anonimleştirme talebi yönetimi
- Hassas veri görüntüleme logu
- Yetkisiz erişim uyarısı
- Veri saklama süresi tanımlama
- Kullanıcı işlem kayıtları
- Otomatik yedekleme politikası
- Gizlilik politikası ekranı

> Not: Bu doküman teknik ürün gereksinimi içindir. KVKK, sağlık mevzuatı, e-reçete, e-imza, MEDULA ve resmi sağlık entegrasyonları için hukuk danışmanı ve ilgili resmi kurum dokümanlarıyla doğrulama yapılmalıdır.

---

## 5. Önerilen Ekranlar

## 5.1 Ana Dashboard

- Bugünkü randevular
- Bekleyen hastalar
- Günlük hasta sayısı
- Günlük tahsilat
- Doktor doluluk oranı
- Uyarılar
- Son işlemler
- Hızlı arama

## 5.2 Hasta Listesi

- Arama
- Filtreleme
- Hasta kartına git
- Yeni hasta ekle
- Dışa aktar
- Etiket filtreleri
- Son muayene tarihi

## 5.3 Hasta Detay Ekranı

Sekmeler:

1. Genel Bilgiler
2. Sağlık Bilgileri
3. Randevular
4. Muayeneler
5. Reçeteler
6. Belgeler
7. Ödemeler
8. Notlar
9. KVKK / Onamlar
10. Loglar

## 5.4 Randevu Takvimi

- Günlük görünüm
- Haftalık görünüm
- Doktor filtresi
- Branş filtresi
- Durum filtresi
- Sürükle-bırak ile saat değiştirme
- Randevu detay popup
- Hızlı hasta kaydı

## 5.5 Muayene Ekranı

- Hasta özet kartı
- Geçmiş muayene listesi
- Şikayet
- Anamnez
- Bulgular
- Tanı
- Tedavi planı
- Reçete
- Tetkik
- Dosya yükleme
- Kontrol tarihi
- Kaydet / tamamla

## 5.6 Reçete Ekranı

- Hasta bilgisi
- Doktor bilgisi
- İlaç arama
- Doz ve kullanım bilgisi
- Sık kullanılan ilaçlar
- Şablonlar
- Alerji uyarısı
- PDF oluştur
- Yazdır

## 5.7 Belge Arşivi

- Dosya yükleme
- Kategori
- Tarih
- Muayene bağlantısı
- Önizleme
- İndirme
- Silme
- Erişim geçmişi

## 5.8 Raporlar

- Operasyonel raporlar
- Klinik raporlar
- Finansal raporlar
- Grafikler
- Excel/PDF dışa aktarma

---

## 6. Önerilen Veritabanı Tabloları

Aşağıdaki yapı başlangıç için yeterlidir. Geliştirme ilerledikçe alt tablolara ayrılabilir.

### 6.1 users

- user_id
- name
- surname
- email
- phone
- password_hash
- role_id
- status
- last_login
- created_at
- updated_at

### 6.2 roles

- role_id
- role_name
- description

### 6.3 permissions

- permission_id
- permission_code
- permission_name

### 6.4 role_permissions

- role_id
- permission_id

### 6.5 doctors

- doctor_id
- user_id
- title
- branch_id
- diploma_no
- signature_file
- status

### 6.6 branches

- branch_id
- branch_name

### 6.7 patients

- patient_id
- identity_no
- passport_no
- name
- surname
- birth_date
- gender
- phone
- email
- address
- blood_type
- emergency_contact_name
- emergency_contact_phone
- status
- created_at
- updated_at

### 6.8 patient_medical_info

- id
- patient_id
- allergies
- chronic_diseases
- regular_medicines
- surgeries
- family_history
- smoking
- alcohol
- special_notes

### 6.9 appointments

- appointment_id
- patient_id
- doctor_id
- appointment_start
- appointment_end
- status
- appointment_type
- note
- created_by
- created_at
- updated_at

### 6.10 examinations

- examination_id
- patient_id
- doctor_id
- appointment_id
- complaint
- anamnesis
- findings
- diagnosis
- icd10_code
- treatment_plan
- doctor_note
- result
- control_date
- created_at
- updated_at

### 6.11 vital_signs

- vital_id
- examination_id
- height
- weight
- bmi
- temperature
- pulse
- systolic_bp
- diastolic_bp
- respiratory_rate
- oxygen_saturation
- blood_glucose
- pain_score

### 6.12 prescriptions

- prescription_id
- examination_id
- patient_id
- doctor_id
- prescription_date
- note
- status
- pdf_file_id
- created_at

### 6.13 prescription_items

- item_id
- prescription_id
- medicine_name
- active_ingredient
- dosage
- frequency
- duration
- usage_instruction
- note

### 6.14 documents

- document_id
- patient_id
- examination_id
- uploaded_by
- document_type
- file_name
- file_path
- mime_type
- file_size
- description
- created_at

### 6.15 payments

- payment_id
- patient_id
- appointment_id
- examination_id
- amount
- payment_type
- payment_status
- description
- created_at

### 6.16 services

- service_id
- service_name
- price
- status

### 6.17 consents

- consent_id
- patient_id
- consent_type
- consent_text_version
- approved
- approved_at
- ip_address
- created_at

### 6.18 audit_logs

- log_id
- user_id
- action
- entity_type
- entity_id
- old_value
- new_value
- ip_address
- user_agent
- created_at

### 6.19 notifications

- notification_id
- patient_id
- appointment_id
- channel
- message
- status
- sent_at
- created_at

---

## 7. Öncelikli MVP Kapsamı

İlk sürümde her şeyi yapmak yerine şu modüllerle başlanması önerilir:

### MVP 1 - Çekirdek Sistem

- Kullanıcı girişi
- Rol bazlı yetki
- Hasta kayıt
- Hasta listeleme
- Hasta detay ekranı
- Doktor tanımı
- Randevu takvimi
- Muayene kaydı
- Geçmiş muayene görüntüleme
- Reçete oluşturma
- Dosya yükleme
- Basit raporlar
- İşlem logları

### MVP 2 - Operasyonel Geliştirme

- SMS / WhatsApp hatırlatma
- Ödeme / kasa
- PDF çıktılar
- Reçete şablonları
- Muayene şablonları
- Kontrol randevusu
- Hasta belgeleri gelişmiş arşiv

### MVP 3 - İleri Seviye

- Hasta portalı
- Online randevu
- Mobil uygulama
- E-imza
- E-reçete altyapısı
- Laboratuvar entegrasyonu
- DICOM görüntüleme
- Yapay zeka destekli not özetleme
- Karar destek sistemi
- Çok şube desteği

---

## 8. Teknik Mimari Önerisi

### 8.1 Web Tabanlı Mimari

- Frontend: HTML5, CSS3, Bootstrap, JavaScript
- Backend: CFML / ColdFusion veya Python Django / Node.js
- Veritabanı: PostgreSQL veya SQL Server
- Dosya Depolama: Lokal disk, S3 uyumlu object storage veya NAS
- Bildirim: SMS API, WhatsApp Business API, SMTP
- PDF: Sunucu tarafı PDF üretimi
- Authentication: Session + JWT opsiyonel
- Loglama: Audit log + sistem logu

### 8.2 Önerilen Katmanlar

1. Arayüz Katmanı
2. API / Controller Katmanı
3. Servis Katmanı
4. Veri Erişim Katmanı
5. Dosya Yönetim Katmanı
6. Bildirim Katmanı
7. Raporlama Katmanı
8. Güvenlik / Yetki Katmanı

### 8.3 Örnek Klasör Yapısı

```text
/app
  /controllers
    patientController.cfc
    appointmentController.cfc
    examinationController.cfc
    prescriptionController.cfc
  /services
    PatientService.cfc
    AppointmentService.cfc
    ExaminationService.cfc
    PrescriptionService.cfc
    FileService.cfc
    NotificationService.cfc
  /views
    /patients
    /appointments
    /examinations
    /prescriptions
    /reports
  /assets
    /css
    /js
    /img
/uploads
  /patients
/logs
/config
```

---

## 9. Kritik İş Akışları

## 9.1 Yeni Hasta + Randevu Akışı

1. Sekreter hasta arar.
2. Hasta yoksa yeni hasta kaydı açılır.
3. Doktor ve uygun saat seçilir.
4. Randevu oluşturulur.
5. SMS / WhatsApp bilgilendirmesi gönderilir.
6. Randevu takvimde görünür.

## 9.2 Muayene Akışı

1. Hasta geldi olarak işaretlenir.
2. Doktor panelinde hasta görünür.
3. Doktor muayene başlatır.
4. Önceki muayeneleri inceler.
5. Şikayet, bulgu, tanı, tedavi planı girer.
6. Gerekirse reçete oluşturur.
7. Dosya / tetkik ekler.
8. Kontrol tarihi belirler.
9. Muayene tamamlanır.
10. Ödeme ekranına yönlendirilir.

## 9.3 Reçete Akışı

1. Doktor muayene içinden reçete oluşturur.
2. İlaçları ekler.
3. Kullanım talimatlarını girer.
4. Alerji / etkileşim kontrolü yapılır.
5. Reçete kaydedilir.
6. PDF çıktısı alınır.
7. Hasta dosyasında arşivlenir.

## 9.4 Belge Yükleme Akışı

1. Hasta kartı veya muayene kaydı açılır.
2. Belge kategorisi seçilir.
3. Dosya yüklenir.
4. Açıklama girilir.
5. Sistem dosyayı güvenli alana kaydeder.
6. Dosya hasta zaman çizelgesinde görünür.
7. Erişim logu tutulur.

---

## 10. Kullanıcı Deneyimi Önerileri

- Hasta arama her ekranda üstte bulunmalı
- Doktor ekranı sade ve hızlı olmalı
- Muayene ekranı tek sayfada tamamlanabilmeli
- Sık kullanılan tanı, ilaç ve notlar favorilere eklenebilmeli
- Randevu takvimi renkli durum etiketleriyle gösterilmeli
- Hasta kartında önemli uyarılar kırmızı/sarı kart olarak görünmeli
- Dosya yükleme sürükle-bırak desteklemeli
- PDF çıktılar profesyonel antetli olmalı
- Mobil uyumlu tasarım kullanılmalı
- Klavye kısayolları eklenmeli
- Doktor için “son muayeneyi kopyala” özelliği olmalı

---

## 11. Entegrasyon Önerileri

### 11.1 Kısa Vadeli

- SMS API
- SMTP e-posta
- WhatsApp bildirim
- Google Calendar / Outlook Calendar
- PDF üretimi
- Excel dışa aktarma

### 11.2 Orta Vadeli

- e-Fatura / e-Arşiv
- Online ödeme
- Laboratuvar sonucu aktarımı
- İlaç veri tabanı
- E-imza
- Mobil uygulama

### 11.3 Uzun Vadeli

- MEDULA / e-reçete entegrasyonu
- e-Nabız benzeri sağlık kayıt paylaşımı için yasal entegrasyonlar
- DICOM / PACS entegrasyonu
- Yapay zeka destekli muayene notu
- Klinik karar destek sistemi
- Telemedicine / görüntülü görüşme

---

## 12. Güvenlik ve Veri Koruma Kontrol Listesi

- [ ] HTTPS zorunlu olmalı
- [ ] Şifreler hashlenmeli
- [ ] Rol bazlı erişim olmalı
- [ ] Her hasta dosyası görüntüleme loglanmalı
- [ ] Dosyalar herkese açık klasörde tutulmamalı
- [ ] Dosya erişimi token veya yetki kontrolüyle yapılmalı
- [ ] Hassas veriler maskeleme ile gösterilmeli
- [ ] Oturum zaman aşımı olmalı
- [ ] Şifre yenileme güvenli olmalı
- [ ] Kullanıcı işlem kayıtları tutulmalı
- [ ] Düzenli yedekleme yapılmalı
- [ ] Yedekler şifrelenmeli
- [ ] Veri silme / anonimleştirme politikası olmalı
- [ ] KVKK açık rıza kayıtları tutulmalı
- [ ] Sistem logları değiştirilemez şekilde saklanmalı
- [ ] Dosya yüklemelerinde virüs taraması yapılmalı
- [ ] Dosya türü ve boyutu sınırlandırılmalı
- [ ] Admin işlemleri ayrıca loglanmalı

---

## 13. Geliştirme Önceliklendirme Tablosu

| Modül | Öncelik | MVP'ye Dahil mi? | Açıklama |
|---|---:|---:|---|
| Kullanıcı / rol yönetimi | Çok yüksek | Evet | Güvenlik için şart |
| Hasta kartı | Çok yüksek | Evet | Sistemin merkezi |
| Randevu takvimi | Çok yüksek | Evet | Operasyonel temel |
| Muayene kaydı | Çok yüksek | Evet | Klinik temel |
| Geçmiş muayene | Çok yüksek | Evet | Doktor için kritik |
| Reçete | Yüksek | Evet | Temel ihtiyaç |
| Belge yükleme | Yüksek | Evet | Kullanıcının istediği temel özellik |
| SMS / WhatsApp | Orta | Hayır | MVP sonrası |
| Ödeme / kasa | Orta | Opsiyonel | Klinik ihtiyacına göre |
| Hasta portalı | Orta | Hayır | İkinci faz |
| Online randevu | Orta | Hayır | İkinci faz |
| E-reçete entegrasyonu | Yüksek ama zor | Hayır | Resmi süreç gerektirir |
| Laboratuvar entegrasyonu | Düşük/orta | Hayır | İleri faz |
| DICOM görüntüleme | Düşük | Hayır | Branşa bağlı |
| Yapay zeka destekleri | Düşük | Hayır | İleri faz |

---

## 14. Örnek Menü Yapısı

```text
Dashboard
Hastalar
  Hasta Listesi
  Yeni Hasta
  Hasta Etiketleri
Randevular
  Takvim
  Günlük Liste
  Bekleme Listesi
Muayeneler
  Muayene Listesi
  Tamamlanmamış Muayeneler
Reçeteler
  Reçete Listesi
  Reçete Şablonları
Belgeler
  Belge Arşivi
  Belge Kategorileri
Finans
  Tahsilatlar
  Kasa
  Hizmetler
Raporlar
  Randevu Raporları
  Hasta Raporları
  Finans Raporları
Ayarlar
  Kullanıcılar
  Roller
  Doktorlar
  Branşlar
  Çalışma Saatleri
  Bildirim Şablonları
  KVKK Metinleri
  Sistem Ayarları
```

---

## 15. İlk Sürüm İçin Sayfa Bazlı Yapılacaklar

### Hasta Liste Sayfası

- Hasta arama
- Sayfalama
- Filtreleme
- Yeni hasta butonu
- Hasta detayına git
- Son muayene tarihi
- Telefon bilgisi
- Durum etiketi

### Hasta Detay Sayfası

- Hasta özet kartı
- Sağlık uyarıları
- Muayene geçmişi
- Randevu geçmişi
- Reçete geçmişi
- Belgeler
- Ödeme geçmişi
- Yeni randevu butonu
- Yeni muayene butonu

### Randevu Sayfası

- Doktor filtresi
- Takvim görünümü
- Randevu ekleme modalı
- Randevu durum renkleri
- İptal / erteleme / geldi butonları

### Muayene Sayfası

- Hasta bilgisi
- Önceki muayeneler
- Şikayet
- Anamnez
- Bulgular
- Tanı
- Tedavi planı
- Reçete oluştur
- Belge yükle
- Kaydet / tamamla

### Reçete Sayfası

- İlaç arama
- Kullanım dozu
- Kullanım sıklığı
- Süre
- Açıklama
- PDF çıktı
- Şablon kaydet

---

## 16. Kaynaklardan Çıkarılan Önemli Bulgular

- Modern klinik yönetim yazılımlarında randevu yönetimi, hasta profili, EMR/EHR kayıtları, reçete, belge yönetimi, faturalama ve raporlama birlikte sunulmaktadır.
- Çok doktorlu kliniklerde gerçek zamanlı takvim, çakışma önleme ve hasta hatırlatma mesajları önemli bir ihtiyaçtır.
- EMR/EHR sistemleri hasta geçmişi, test sonuçları, reçeteler ve tedavi planlarını tek platformda saklamaya odaklanır.
- Belge yükleme; laboratuvar, röntgen, rapor, hasta formu ve fotoğraf gibi dosyaların hasta dosyasıyla ilişkilendirilmesi için gereklidir.
- Hasta portalı; hastanın randevu, belge, reçete ve muayene geçmişine güvenli erişimini sağlar.
- Sağlık verileri özel nitelikli kişisel veri olduğu için yetkilendirme, loglama, şifreleme, onay kayıtları ve KVKK uyumu temel gereksinimdir.

---

## 17. Kaynakça

1. Orca Software - Klinik ve Sağlık Merkezi Yönetim Yazılımı Rehberi 2026  
   https://orcasoftware.com.tr/blog/klinik-saglik-merkezi-yazilimi-yonetim-2026

2. Medesk - Medical Practice Management Software  
   https://www.medesk.net/en/

3. Yolo Clinic - EMR Features  
   https://yolo.clinic/features/

4. Healthgennie - Clinics & Hospitals Management Software  
   https://doc.healthgennie.com/clinics-hospitals-management-software

5. NZCares - EMR/EHR System  
   https://www.nzcares.com/emr-ehr-system-software-development

6. LinkHMS - Medical Practice Management Software Features  
   https://linkhms.com/blog/top-medical-practice-management-software/

7. Genamet - Clinic Management Software  
   https://www.genamet.com/features/clinic-management-software

8. OpenEMR - Open Source EMR and Medical Practice Management  
   https://www.open-emr.org/

9. KVKK - Özel Nitelikli Kişisel Veriler  
   https://www.kvkk.gov.tr/Icerik/2051/Ozel-Nitelikli-Kisisel-Veriler

10. KVKK - Sağlık Verileri ve Özel Nitelikli Kişisel Veri Kararı  
    https://www.kvkk.gov.tr/Icerik/5364/2018-143

---

## 18. Sonuç

Bu sistemin ilk sürümü için en doğru yaklaşım; önce **hasta kartı + randevu + muayene + reçete + belge yükleme + yetki/loglama** çekirdeğini kurmaktır.

Daha sonra SMS/WhatsApp hatırlatma, ödeme/kasa, hasta portalı, online randevu, PDF raporlar ve resmi entegrasyonlar aşamalı olarak eklenebilir.

Önerilen MVP geliştirme sırası:

1. Veritabanı tasarımı
2. Kullanıcı ve rol sistemi
3. Hasta kayıt ekranları
4. Doktor ve randevu takvimi
5. Muayene kayıt ekranı
6. Reçete ekranı
7. Belge yükleme
8. Raporlama
9. KVKK / loglama / güvenlik
10. Bildirim ve entegrasyonlar
