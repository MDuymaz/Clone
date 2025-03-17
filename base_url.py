import requests
import re
from bs4 import BeautifulSoup

# ana_link.txt dosyasından URL'yi oku
with open("ana_link.txt", "r") as file:
    url = file.read().strip()

# User-Agent ekleyerek isteği yap (bazı siteler botları engeller)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

# Sayfanın kaynak kodunu al
response = requests.get(url, headers=headers)

# Eğer sayfa yüklenmezse hata mesajı ver
if response.status_code != 200:
    print("Sayfa yüklenemedi!")
    exit()

# Sayfa içeriğini BeautifulSoup ile parse et
soup = BeautifulSoup(response.text, 'html.parser')

# "selcukbeinspor" ifadesini içeren öğeyi bul ve data-url değerini al
element = soup.find(attrs={"data-url": True, "data-url": lambda x: x and "selcukbeinspor" in x})

# Eğer öğe bulunursa, data-url değerini yazdır ve HTML içeriğini al
if element:
    data_url = element['data-url']
    print("data-url değeri:", data_url)
    
    # Data-url ile yeni bir istek yap
    response_data_url = requests.get(data_url, headers=headers)
    
    # Eğer URL'ye başarıyla erişildiyse, HTML içeriğini yazdır
    if response_data_url.status_code == 200:
        print("Data URL'nin HTML içeriği alındı.")

        # JavaScript'teki this.baseStreamUrl değerini almak için düzenli ifade kullan
        base_stream_url_match = re.search(r"this\.baseStreamUrl\s*=\s*['\"](.*?)['\"]", response_data_url.text)

        # Eğer eşleşme bulunursa, baseStreamUrl değerini yazdır
        if base_stream_url_match:
            base_stream_url = base_stream_url_match.group(1)
            print("Base Stream URL:", base_stream_url)

            # Base Stream URL'yi base_url.txt dosyasına yaz
            with open("base_url.txt", "w") as file:
                file.write(base_stream_url)
            print("Base Stream URL, base_url.txt dosyasına yazıldı.")
        else:
            print("this.baseStreamUrl değeri bulunamadı.")
    else:
        print(f"Data URL'ye erişilemedi. HTTP Durum Kodu: {response_data_url.status_code}")
else:
    print("'selcukbeinspor' ifadesini içeren data-url bulunamadı.")
