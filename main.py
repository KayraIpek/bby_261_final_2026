# Dosya Adı: uygulama.py
import requests
import re
from bs4 import BeautifulSoup
from rommenu import MenuSistemi

# Tarayıcı taklidi yapan başlık bilgileri (Bot korumasını aşmak için)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
}

def etkinlikleri_listele():
    # Kaynak: Hacettepe BBY Duyurular
    url = "https://bby.hacettepe.edu.tr/duyurular.php"
    print(f"\n--- BBY Duyuruları Listeleniyor ({url}) ---")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        # Türkçe karakter sorununu çözmek için encoding ayarı
        response.encoding = response.apparent_encoding 

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # YÖNTEM: Sadece detay sayfasına giden linkleri bul (href içinde 'duyurudetay' geçenler)
            # Bu sayede 'Hakkımızda', 'İletişim' gibi menü linkleri elenir.
            duyuru_linkleri = soup.find_all("a", href=lambda href: href and "duyurudetay" in href)
            
            sayac = 0
            yazdirilanlar = set()
            
            # Başlık çıktısı
            print(f"{'No':<4} {'Tarih':<12} {'Başlık'}")
            print("-" * 70)
            
            for link in duyuru_linkleri:
                baslik = link.get_text(strip=True)
                
                # Başlık çok kısaysa (örn: "Devamı") atla
                if not baslik or len(baslik) < 5:
                    continue
                
                # Tarihi bulmak için: Linkin bulunduğu satırın (tr veya div) metnine bak
                kapsayici = link.find_parent().find_parent()
                if kapsayici:
                    kapsayici_metin = kapsayici.get_text()
                    # Metin içinde GG.AA.YYYY formatında tarih ara
                    tarih_bul = re.search(r'\d{2}\.\d{2}\.\d{4}', kapsayici_metin)
                    tarih = tarih_bul.group() if tarih_bul else "   -   "
                else:
                    tarih = "   -   "
                
                # Tekrar eden duyuruları engelle
                ozgun_id = f"{tarih}_{baslik}"
                
                if ozgun_id not in yazdirilanlar:
                    sayac += 1
                    print(f"{sayac:<4} {tarih:<12} {baslik}")
                    yazdirilanlar.add(ozgun_id)
                    
                    if sayac >= 15: # En fazla 15 duyuru göster
                        break
            
            if sayac == 0:
                print("Listelenecek duyuru bulunamadı.")
        else:
            print(f"Siteye erişilemedi. Durum Kodu: {response.status_code}")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")

def haberleri_listele():
    # Kaynak: Hacettepe Gazete
    url = "https://gazete.hacettepe.edu.tr/tr/haberler"
    print(f"\n--- Haberler Listeleniyor ({url}) ---")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Gazete sitesinde başlıklar genelde h2 veya h3 içindedir
            haberler = soup.find_all(["h3", "h2"])
            
            # Eğer başlık etiketiyle bulamazsa linkleri tara
            if not haberler:
                haberler = soup.find_all("a")
            
            sayac = 0
            yazdirilanlar = set()
            
            for haber in haberler:
                metin = haber.get_text(strip=True)
                
                # Haber filtresi (kısa yazılar ve menü elemanlarını ele)
                if (metin and len(metin) > 20 and len(metin) < 200 and 
                    "Devamını" not in metin and 
                    "Copyright" not in metin and
                    metin not in yazdirilanlar):
                    
                    sayac += 1
                    print(f"{sayac}- {metin}")
                    yazdirilanlar.add(metin)
                    
                    if sayac >= 10:
                        break
            
            if sayac == 0:
                print("Haber bulunamadı.")
                
        else:
            print(f"Siteye erişilemedi. Hata Kodu: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Bağlantı hatası: {e}")

# --- Ana Program Akışı ---
if __name__ == "__main__":
    menu_map = {
        "Etkinlikleri/Duyuruları Listele (BBY)": etkinlikleri_listele,
        "Haberleri Listele (Gazete)": haberleri_listele
    }
    
    MenuSistemi.karsilama("Hacettepe Bilgi Sistemi v4.0")
    MenuSistemi.menuyuCalistir(menu_map)
