import requests

# ana_link.txt dosyasındaki URL'yi oku
with open("ana_link.txt", "r", encoding="utf-8") as file:
    base_url = file.read().strip()

# URL'deki son sayıyı ayır (örneğin, 'selcuksportshd1724.xyz' kısmındaki '1724' sayısını al)
base_number = int(base_url.split("selcuksportshd")[-1].split(".")[0])

# Sayıyı birer birer artırarak dene
while True:
    # Yeni URL'yi oluştur (base_number'ı artırarak)
    new_url = base_url.replace(str(base_number), str(base_number + 1))
    print(f"Denenen URL: {new_url}")  # Her seferinde hangi URL'nin denendiğini yazdıralım.
    
    try:
        # URL'yi kontrol et ve yönlendirmeleri takip et
        response = requests.get(new_url, allow_redirects=True, timeout=5)
        
        # Eğer site 200 durum kodu dönerse, yani site açılıyorsa
        if response.status_code == 200:
            # Yönlendirilmiş URL'yi al
            final_url = response.url
            print(f"Yönlendirilen site: {final_url}")  # Yönlendirilmiş URL'yi yazdırıyoruz.
            
            # Eğer URL'deki sayıyı alıp bir sonraki işlemi yapmak isterseniz:
            final_number = int(final_url.split("selcuksportshd")[-1].split(".")[0])
            print(f"Yönlendirilen site numarası: {final_number}")
            
            # Yeni URL'yi ana_link.txt dosyasına yaz
            with open("ana_link.txt", "w", encoding="utf-8") as file:
                file.write(final_url)
            
            print(f"ana_link.txt dosyası güncellendi: {final_url}")
            break  # Yönlendirme başarılıysa, döngüyü sonlandır
        
        else:
            print(f"{new_url} açılmıyor, bir sonraki siteyi deniyorum.")
        
    except requests.exceptions.RequestException as e:
        # Eğer site yanıt vermezse, hata mesajını göster
        print(f"Site {new_url} yanıt vermedi. Hata: {e}")

    # Sayıyı bir artır
    base_number += 1
