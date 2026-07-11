import pandas as pd
import os
import re
import sqlite3


def turkish_upper(text):
    if not isinstance(text, str):
        return ""
    mapping = {
        "i": "İ",
        "ı": "I",
        "ş": "Ş",
        "ğ": "Ğ",
        "ü": "Ü",
        "ö": "Ö",
        "ç": "Ç"
    }
    upper_text = ""
    for char in text:
        upper_text += mapping.get(char, char.upper())
    return upper_text


def clean_uni_name(name):
    name = turkish_upper(name)
    re_space = re.compile(r'\s+')
    return re_space.sub(' ', name).strip()


target_mappings = {
    "HACETTEPE ÜNİVERSİTESİ (ANKARA) (Devlet Üniversitesi)": "Hacettepe Üniversitesi",
    "İSTANBUL TEKNİK ÜNİVERSİTESİ (Devlet Üniversitesi)": "İstanbul Teknik Üniversitesi (İTÜ)",
    "ANKARA ÜNİVERSİTESİ (Devlet Üniversitesi)": "Ankara Üniversitesi",
    "GAZİ ÜNİVERSİTESİ (ANKARA) (Devlet Üniversitesi)": "Gazi Üniversitesi",
    "KOÇ ÜNİVERSİTESİ (İSTANBUL) (Vakıf Üniversitesi)": "Koç Üniversitesi",
    "İSTANBUL ÜNİVERSİTESİ (Devlet Üniversitesi)": "İstanbul Üniversitesi",
    "EGE ÜNİVERSİTESİ (İZMİR) (Devlet Üniversitesi)": "Ege Üniversitesi",
    "ATATÜRK ÜNİVERSİTESİ (ERZURUM) (Devlet Üniversitesi)": "Atatürk Üniversitesi",
    "ORTA DOĞU TEKNİK ÜNİVERSİTESİ (ANKARA) (Devlet Üniversitesi)": "Orta Doğu Teknik Üniversitesi (ODTÜ)",
    "SAĞLIK BİLİMLERİ ÜNİVERSİTESİ (İSTANBUL) (Devlet Üniversitesi)": "Sağlık Bilimleri Üniversitesi",
    "YAKIN DOĞU ÜNİVERSİTESİ (KKTC-LEFKOŞA)": "Yakın Doğu Üniversitesi (KKTC)",
    "İSTANBUL ÜNİVERSİTESİ-CERRAHPAŞA (Devlet Üniversitesi)": "İstanbul Üniversitesi - Cerrahpaşa",
    "YILDIZ TEKNİK ÜNİVERSİTESİ (İSTANBUL) (Devlet Üniversitesi)": "Yıldız Teknik Üniversitesi",
    "MARMARA ÜNİVERSİTESİ (İSTANBUL) (Devlet Üniversitesi)": "Marmara Üniversitesi",
    "ERCİYES ÜNİVERSİTESİ (KAYSERİ) (Devlet Üniversitesi)": "Erciyes Üniversitesi",
    "FIRAT ÜNİVERSİTESİ (ELAZIĞ) (Devlet Üniversitesi)": "Fırat Üniversitesi",
    "DOKUZ EYLÜL ÜNİVERSİTESİ (İZMİR) (Devlet Üniversitesi)": "Dokuz Eylül Üniversitesi",
    "SELÇUK ÜNİVERSİTESİ (KONYA) (Devlet Üniversitesi)": "Selçuk Üniversitesi",
    "SAKARYA ÜNİVERSİTESİ (Devlet Üniversitesi)": "Sakarya Üniversitesi",
    "AKDENİZ ÜNİVERSİTESİ (ANTALYA) (Devlet Üniversitesi)": "Akdeniz Üniversitesi",
    "ÇUKUROVA ÜNİVERSİTESİ (ADANA) (Devlet Üniversitesi)": "Çukurova Üniversitesi",
    "KARADENİZ TEKNİK ÜNİVERSİTESİ (TRABZON) (Devlet Üniversitesi)": "Karadeniz Teknik Üniversitesi (KTÜ)",
    "İSTİNYE ÜNİVERSİTESİ (İSTANBUL) (Vakıf Üniversitesi)": "İstinye Üniversitesi",
    "ONDOKUZ MAYIS ÜNİVERSİTESİ (SAMSUN) (Devlet Üniversitesi)": "Ondokuz Mayıs Üniversitesi",
    "BOĞAZİÇİ ÜNİVERSİTESİ (İSTANBUL) (Devlet Üniversitesi)": "Boğaziçi Üniversitesi",
    "BURSA ULUDAĞ ÜNİVERSİTESİ (Devlet Üniversitesi)": "Bursa Uludağ Üniversitesi",
    "İHSAN DOĞRAMACI BİLKENT ÜNİVERSİTESİ (ANKARA) (Vakıf Üniversitesi)": "İhsan Doğramacı Bilkent Üniversitesi",
    "SABANCI ÜNİVERSİTESİ (İSTANBUL) (Vakıf Üniversitesi)": "Sabancı Üniversitesi",
    "KOCAELİ ÜNİVERSİTESİ (Devlet Üniversitesi)": "Kocaeli Üniversitesi",
    "SİVAS CUMHURİYET ÜNİVERSİTESİ (Devlet Üniversitesi)": "Sivas Cumhuriyet Üniversitesi"
}


def main():
    file_path = "tablo4_01082025d (2).xls"
    if not os.path.exists(file_path):
        print(f"Dosya bulunamadı: {file_path}")
        return

    print("Veri yükleniyor...")
    df = pd.read_excel(file_path)

    extracted_data = []
    current_uni_full = None
    current_uni_clean = None
    current_faculty = None

    for idx in range(2, len(df)):
        row = df.iloc[idx]
        code = row.iloc[0]
        name = row.iloc[1]

        if pd.isna(code):
            if isinstance(name, str):
                name_clean = clean_uni_name(name)
                is_uni = "ÜNİVERSİTESİ" in name_clean or "ÜNİVERSİTE" in name_clean or name_clean in target_mappings

                if is_uni:
                    matched = False
                    for full_key, clean_val in target_mappings.items():
                        if name_clean == clean_uni_name(full_key):
                            current_uni_full = name_clean
                            current_uni_clean = clean_val
                            current_faculty = None
                            matched = True
                            break
                    if not matched:
                        current_uni_full = None
                        current_uni_clean = None
                        current_faculty = None
                else:
                    if current_uni_clean is not None:
                        current_faculty = name.strip()
        else:
            if current_uni_clean is not None:
                prog_code = str(code).strip()
                if prog_code.endswith('.0'):
                    prog_code = prog_code[:-2]

                prog_name = str(name).strip() if not pd.isna(name) else ""
                duration = row.iloc[2]
                puan_type = row.iloc[3]
                quota_general = row.iloc[4]
                quota_first = row.iloc[5]
                rank = row.iloc[11]
                min_score = row.iloc[12]

                extracted_data.append({
                    "Üniversite (Spreadsheet)": current_uni_full,
                    "Üniversite Adı": current_uni_clean,
                    "Fakülte/Yüksekokul": current_faculty if current_faculty else "Genel",
                    "Program Kodu": prog_code,
                    "Program Adı": prog_name,
                    "Süre (Yıl)": duration,
                    "Puan Türü": puan_type,
                    "Genel Kontenjan": quota_general,
                    "Okul Birincisi Kontenjanı": quota_first,
                    "Başarı Sırası": rank,
                    "Taban Puan (En Küçük Puan)": min_score
                })

    out_df = pd.DataFrame(extracted_data)
    if len(out_df) == 0:
        print("Eşleşen veri bulunamadı.")
        return

    print("Veri tipleri optimize ediliyor...")
    out_df['Başarı Sırası'] = pd.to_numeric(out_df['Başarı Sırası'], errors='coerce').fillna(0).astype(int)
    out_df['Taban Puan (En Küçük Puan)'] = pd.to_numeric(out_df['Taban Puan (En Küçük Puan)'], errors='coerce').fillna(
        0.0)
    out_df['Puan Türü'] = out_df['Puan Türü'].astype('category')
    out_df['Süre (Yıl)'] = pd.to_numeric(out_df['Süre (Yıl)'], errors='coerce').fillna(0).astype(int)
    out_df['Genel Kontenjan'] = pd.to_numeric(out_df['Genel Kontenjan'], errors='coerce').fillna(0).astype(int)
    out_df['Okul Birincisi Kontenjanı'] = pd.to_numeric(out_df['Okul Birincisi Kontenjanı'], errors='coerce').fillna(
        0).astype(int)

    excel_output = "universite_bolum_puanlar.xlsx"
    csv_output = "universite_bolum_puanlar.csv"

    out_df.to_excel(excel_output, index=False)
    out_df.to_csv(csv_output, index=False, encoding="utf-8-sig")
    print(f"Dosyalar kaydedildi: {excel_output}, {csv_output}")

    print("SQLite veritabanı senkronizasyonu başlatılıyor...")
    conn = sqlite3.connect('universite_tercih_mvp.db')

    df_sql = out_df.drop(columns=['Üniversite (Spreadsheet)']).rename(columns={
        'Üniversite Adı': 'universite_adi',
        'Fakülte/Yüksekokul': 'fakulte',
        'Program Kodu': 'program_kodu',
        'Program Adı': 'program_adi',
        'Süre (Yıl)': 'sure',
        'Puan Türü': 'puan_turu',
        'Genel Kontenjan': 'genel_kontenjan',
        'Okul Birincisi Kontenjanı': 'okul_birincisi_kontenjani',
        'Başarı Sırası': 'basari_sirasi',
        'Taban Puan (En Küçük Puan)': 'taban_puan'
    })

    df_sql.to_sql('bolumler', conn, if_exists='replace', index=False)
    conn.close()
    print("Veritabanı tablosu güncellendi: universite_tercih_mvp.db -> bolumler")


if __name__ == "__main__":
    main()