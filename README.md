# Takım 312

## 👥 Takım Rolleri
* **Tesnim Çelik**: Product Owner
* **Mehmet Can Kabalak**: Scrum Master
* **Bilge Yılmaz**: Developer
* **Nisa Nur Yılmaz**: Developer
* **Adal Su Uygur**: Developer

---

## 🎯 Ürün Bilgileri

### Ürün İsmi: GuideAI

### Ürün Açıklaması
Üniversite ve kariyer seçim sürecinde kararsızlık yaşayan bireylere yapay zeka destekli rehberlik sunan kişiselleştirilmiş bir platformdur. Projemiz yeni veri üretmek yerine, YÖK Atlas'ın güvenilir ve resmi verilerini yapay zeka ile anlamlı, yorumlanabilir ve kişiye özel bir katmana dönüştürür.

Uygulamamız temelde **3 ana katmandan** oluşmaktadır:
1. **Kendini Tanı:** AI destekli kişilik, ilgi ve yetenek analizi.
2. **Bölüm Öner:** Analiz sonuçlarına göre YÖK Atlas verileriyle eşleşen en uygun 5 bölümün listelenmesi.
3. **Üniversite Karşılaştır:** Önerilen bölümler özelinde resmi verilerle üniversite kıyaslamaları.

### 🌟 Ürün Özellikleri (MVP)
* **AI Kişilik ve İlgi Testi:** Kullanıcıya yöneltilen 25-30 dinamik soru ile ilgi analizi yapılması.
* **Akıllı Bölüm Eşleştirme:** AI analiz sonuçlarından yola çıkarak en uyumlu 5 bölümün algoritma tarafından çıkarılması.
* **Filtrelenmiş Üniversite Verisi:** MVP kapsamında en çok tercih edilen top 20-30 üniversitenin YÖK Atlas verilerinin sunulması.
* **Gelecek Projeksiyonu:** Bölümlerin kariyer olanakları ve gerekli becerilerinin AI tarafından özetlenmesi.

### 🎯 Hedef Kitle
* Üniversite sınavına hazırlanan ve tercih yapacak kararsız adaylar (YKS öğrencileri).
* Kariyer yolunu değiştirmek veya yeteneklerini keşfetmek isteyen genç yetişkinler.
* Rehber öğretmenler ve eğitim danışmanları.

---

## 📁 Klasör Yapısı
Proje, temiz kod prensiplerine ve katmanlı mimariye uygun olarak frontend/backend ayrımıyla geliştirilmektedir[cite: 1]:
* `assets/`: Statik veri setleri ve soru havuzu.
* `backend/`: Python / FastAPI katmanı (API rotaları, LLM servisleri ve DB modelleri).
* `frontend/`: Web / Ön yüz katmanı (UI bileşenleri ve state yönetimi).

---

## 🗺️ Proje Yönetimi & Board Linkleri
* **Product Backlog Board:** https://github.com/users/AdalSuUygur/projects/8

---

## 🔄 Sprint Dokümantasyonu

📍 SPRINT 1 DOKÜMANTASYONU
### 🎯 Sprint 1 Hedefi (Sprint Goal)
Kullanıcının hangi alanlara ve mesleklere yatkın olduğunu anlamasını sağlayacak Holland Meslek Tercih Envanteri tabanlı, dinamik ve akıcı bir ön yüz (frontend) arayüzünün tasarlanması; arka planda bu cevapları deterministik bir algoritmayla işleyip Gemini API (response_schema ve Pydantic) üzerinden tutarlı 5 üniversite bölümü önerecek yapay zeka mimarisinin uçtan uca tamamlanması.
### 🛠️ Sprint İçerisinde Tamamlanan Görevler (Done)
 * **Task 1.1 (Soru Havuzu):** Holland Meslek Tercih Envanteri'ni temel alan 90 soruluk veri seti assets/questions.json formatında projeye entegre edildi.
 * **Task 1.2 (LLM Prompt & Şema Tasarımı):**
   * Yapay zekanın halüsinasyon görmesini engellemek adına katı kurallar ve few-shot örnekler içeren system_prompt.py yazıldı.
   * Gemini API'nin her zaman kararlı ve frontend tarafından doğrudan okunabilir veri üretmesini garanti eden Pydantic çıktı şeması (schemas.py ve llm_service.py) kuruldu.
   * Gerçek API anahtarı ile yapılan 3 tekrarlı testlerde tutarlılık ve DoD şartları doğrulandı.
 * **Task 1.3 (Frontend Arayüz Kodlaması):**
   * **GuideAI** markası altında; 
-Karşılama Ekranı

-İlerleme çubuklu (Progress Bar) Test Ekranı 

-"Sonuçlar Hesaplanıyor" animasyonlu Yüklenme Ekranı 

-Uyum skorlarını içeren Sonuç Ekranı 

tamamen kodlandı.
   * Cevapların arka planda {soru_no: deger} formatında (Hoşlanırım=1, Farketmez=0, Hoşlanmam=-1) toplanma mekanizması kuruldu.
### 📊 Sprint Durumu & Ekran Görüntüleri
 * **Arayüz Çıktıları:** Geliştirilen GuideAI ön yüz mimarisine ait 4 temel ekranın (Giriş, Test Süreci, Hesaplama Katmanı ve Uyum Raporu) çalışan ekran görüntüleri dökümantasyona eklenmiştir

.
 * **Kanban Board Durumu:** Katman 1'e ait olan Task 1.1, Task 1.2 ve Task 1.3 görevleri başarıyla **DONE** sütununa taşınmıştır.
 * **Slack / Daily Scrum Notları:** Ekip içi entegrasyon kanalları üzerinden veri formatları ({soru_no: deger}) paylaşılarak frontend ve backend arasındaki kontrat doğrulanmıştır.
