import requests
from bs4 import BeautifulSoup

# ana_link.txt dosyasından URL'yi oku
with open("ana_link.txt", "r", encoding="utf-8") as file:
    url = file.read().strip()

# Web sayfasını iste
response = requests.get(url)

# Sayfanın içeriğini ayrıştır
soup = BeautifulSoup(response.content, "html.parser")

# <div class="channel-list"> içindeki her şeyi al
channel_list_div = soup.find_all("div", class_="channel-list")

# channel-list'in içeriğini data.html dosyasına yazdır
with open("data.html", "w", encoding="utf-8") as file:
    file.write(str(channel_list_div))

print("Channel list verileri 'data.html' dosyasına başarıyla yazıldı!")
