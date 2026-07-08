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

## Sprint Dokümantasyonu

### 🎯 Sprint 1 Hedefi (Sprint Goal)
Kullanıcının hangi alanlara ve mesleklere yatkın olduğunu anlamasını sağlayacak Holland Meslek Tercih Envanteri tabanlı, dinamik ve akıcı bir ön yüz (frontend) arayüzünün tasarlanması; arka planda bu cevapları deterministik bir algoritmayla işleyip Gemini API (response_schema ve Pydantic) üzerinden tutarlı 5 üniversite bölümü önerecek yapay zeka mimarisinin uçtan uca tamamlanması.

### 🛠️ Sprint İçerisinde Tamamlanan Görevler (Done)
 * **Task 1.1 (Soru Havuzu):** Holland Meslek Tercih Envanteri'ni temel alan 90 soruluk veri seti assets/questions.json formatında projeye entegre edildi.
 * **Task 1.2 (LLM Prompt & Şema Tasarımı):**
   * Yapay zekanın halüsinasyon görmesini engellemek adına katı kurallar ve few-shot örnekler içeren system_prompt.py yazıldı.
   * Gemini API'nin her zaman kararlı ve frontend tarafından doğrudan okunabilir veri üretmesini garanti eden Pydantic çıktı şeması (schemas.py ve llm_service.py) kuruldu.
   * Gerçek API anahtarı ile yapılan 3 tekrarlı testlerde tutarlılık ve DoD şartları doğrulandı.
 * **Task 1.3 (Frontend Arayüz Kodlaması):**
  
-Backend Serverı:
<img width="1892" height="856" alt="image" src="https://github.com/user-attachments/assets/31bda041-78d0-490f-8afc-2cec4b751635" />

-Karşılama Ekranı
<img width="1915" height="869" alt="image" src="https://github.com/user-attachments/assets/5e3224ef-a549-47f7-bec7-6bd3b89cca4e" />

-İlerleme çubuklu (Progress Bar) Test Ekranı 
<img width="1915" height="876" alt="image" src="https://github.com/user-attachments/assets/5198f93b-2a8c-4a10-8cdf-f809adb177de" />
<img width="1916" height="859" alt="image" src="https://github.com/user-attachments/assets/337b1a61-851f-4ef4-be04-28704fb9ecd4" />

-"Sonuçlar Hesaplanıyor" animasyonlu Yüklenme Ekranı 
<img width="1910" height="852" alt="image" src="https://github.com/user-attachments/assets/f6a476e2-a6c4-46f6-8c7f-0c92d79f0d36" />

-Uyum skorlarını içeren Sonuç Ekranı 
<img width="1902" height="865" alt="image" src="https://github.com/user-attachments/assets/71ae6e18-d670-4e6a-9a42-f620b3300944" />

tamamen kodlandı.
   * Cevapların arka planda {soru_no: deger} formatında (Hoşlanırım=1, Farketmez=0, Hoşlanmam=-1) toplanma mekanizması kuruldu.


### 📊 Sprint Durumu & Ekran Görüntüleri
 * **Arayüz Çıktıları:** Geliştirilen GuideAI ön yüz mimarisine ait 4 temel ekranın (Giriş, Test Süreci, Hesaplama Katmanı ve Uyum Raporu) çalışan ekran görüntüleri dökümantasyona eklenmiştir
 * **Kanban Board Durumu:** Katman 1'e ait olan Task 1.1, Task 1.2 ve Task 1.3 görevleri başarıyla **DONE** sütununa taşınmıştır.
<img width="1262" height="895" alt="WhatsApp Image 2026-07-03 at 14 38 06" src="https://github.com/user-attachments/assets/85083e92-2c2f-4069-855d-ae4296aec06a" />
<img width="1911" height="785" alt="image" src="https://github.com/user-attachments/assets/35520afe-5f32-413d-a4b2-12f7333bf467" />

 * **Slack / Daily Scrum Notları:** Ekip içi entegrasyon kanalları üzerinden veri formatları ({soru_no: deger}) paylaşılarak frontend ve backend arasındaki kontrat doğrulanmıştır.
<img width="1453" height="374" alt="image (3)" src="https://github.com/user-attachments/assets/cd7790f3-7e3c-4f02-848f-1f3e9989396b" />
<img width="1451" height="851" alt="image (2)" src="https://github.com/user-attachments/assets/89663577-1320-449e-855c-02d005b2ea88" />
<img width="1466" height="753" alt="image (1)" src="https://github.com/user-attachments/assets/dcbd89c4-598f-4980-9b84-a24160329b2c" />
<img width="954" height="688" alt="image" src="https://github.com/user-attachments/assets/17c2f40c-b940-4e16-bdde-d777b4aedeaa" />
<img width="1462" height="942" alt="image (4)" src="https://github.com/user-attachments/assets/b73dd776-2a22-4e00-9216-770611e4517d" />

* **Sprint 1 - Review**
* Projenin temel backend mimarisi FastAPI kullanılarak ayağa kaldırıldı."
* Holland Code kişilik testi mantığı backend algoritmasına entegre edildi ve ilk API uç noktaları (endpoints) başarıyla test edildi.

 * **Sprint Retrospective:** Takım içi iletişim kanalları verimli kullanıldı. Gelecek sprintlerde kod kalitesini artırmak adına commit mesajları ve branch yönetim standartlarına daha sıkı uyulması kararlaştırıldı.
 <img width="1453" height="374" alt="image (1)" src="https://github.com/user-attachments/assets/1b526179-1735-4181-92a3-10b7e518a2aa" />
<img width="1467" height="930" alt="image" src="https://github.com/user-attachments/assets/79763e73-3146-4ed9-b139-fbb1619a7e28" />

