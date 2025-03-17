from bs4 import BeautifulSoup

# data.html dosyasını oku
with open("data.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Base URL'yi base_url.txt dosyasından oku
with open("base_url.txt", "r", encoding="utf-8") as file:
    base_url = file.read().strip()

# BeautifulSoup ile HTML içeriğini ayrıştır
soup = BeautifulSoup(html_content, "html.parser")

# Verileri alacağımız a, name, time, ve channel-list etiketlerini hedefle
channels = soup.find_all("a", attrs={"data-url": True})

# Channel ID'leri ve isimlerini eşleştir
channel_id_mapping = {
    "tab1": "Futbol",
    "tab2": "Basketbol",
    "tab3": "Tenis",
    "tab4": "Çoklu Ekran",
    "tab5": "7/24 TV",  # tab5 için istenilen ID'yi atlayacağız
    "tab6": "Sohbet"
}

# data.txt dosyasına yazma işlemi
with open("data.txt", "w", encoding="utf-8") as file:
    for channel in channels:
        # Data URL (a etiketindeki data-url)
        data_url = channel.get("data-url", "Bilinmiyor")
        
        # #poster'dan sonrasını kaldır
        if "#poster" in data_url:
            data_url = data_url.split("#poster")[0]
        
        # id= kısmından sonrasını al, diğer her şeyi sil
        if "id=" in data_url:
            data_url = data_url.split("id=")[1]

        # Kanal adı (name sınıfı altında bulunan metin)
        channel_name_tag = channel.find_next("div", class_="name")
        channel_name = channel_name_tag.text.strip() if channel_name_tag else "Bilinmiyor"
        
        # Yayın saati (time sınıfı altında bulunan metin)
        time_tag = channel.find_next("time", class_="time")
        time_info = time_tag.text.strip() if time_tag else "Bilinmiyor"

        # Kanal listesi div'inin id değerini al
        channel_list_tag = channel.find_parent("div", class_="channel-list")
        channel_list_id = channel_list_tag.get("id", "Bilinmiyor") if channel_list_tag else "Bilinmiyor"

        # Eğer ID 'tab5' ise, time_info'yu atla
        if channel_list_id == "tab5":
            channel_list_name = "7/24 TV"  # "tab5" için istenilen ismi ekleyelim
            time_info = ""  # "tab5" için time_info'yu boş bırakıyoruz
        else:
            # Channel ID'yi isme dönüştür
            channel_list_name = channel_id_mapping.get(channel_list_id, channel_list_id)

        # Saat bilgisini, kanal adı ile birlikte yazdır
        file.write(f"Saat: {time_info} - {channel_name}\n")
        
        # Base URL'yi ve /playlist.m3u8'yi ekleyerek yeni data_url oluştur
        final_data_url = f"{base_url}{data_url}/playlist.m3u8"
        
        # Yeni data_url'yi bir sonraki satıra yazdır
        file.write(f"{final_data_url}\n")
        
        # Arada boşluk bırak
        file.write("\n")

print("Veriler 'data.txt' dosyasına başarıyla kaydedildi!")
