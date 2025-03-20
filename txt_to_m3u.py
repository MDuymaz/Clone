# ana_link.txt dosyasını oku
with open('ana_link.txt', 'r', encoding='utf-8') as file:
    base_url = file.read().strip()  # Ana URL'yi al

# data.txt dosyasını oku
with open('data.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# M3U başlık
m3u_header = "#EXTM3U\n"
m3u_content = ""

# Veri satırlarını 3'erli gruplar halinde işle
for i in range(0, len(lines), 4):  # Satırları 4'erli olarak al
    if i + 2 < len(lines):
        group_line = lines[i].strip()
        channel_name_line = lines[i+1].strip()
        url_line = lines[i+2].strip()

        # "=" karakterini kontrol et
        if "=" in group_line and "=" in channel_name_line and "=" in url_line:
            group = group_line.split('=', 1)[1].strip().strip('"')  # Grup adını al
            channel_name = channel_name_line.split('=', 1)[1].strip().strip('"')  # Kanal adı al
            url = url_line.split('=', 1)[1].strip().strip('"')  # URL al

            # Eğer değerler boş değilse devam et
            if group and channel_name and url:
                # M3U formatına uygun içerik oluştur
                m3u_content += (
                    f'#EXTINF:-1 tvg-name="{channel_name}" tvg-language="Turkish" tvg-country="TR" tvg-logo="https://www.selcuksportshd1727.xyz/img/logo.png" '
                    f'group-title="{group}",{channel_name}\n'
                    f'#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)\n'
                    f'#EXTVLCOPT:http-referrer={base_url}\n'
                    f'{url}\n\n'
                )

# M3U dosyasını oluştur
m3u_file_content = m3u_header + m3u_content

# Dosyaya yazma
with open('output.m3u', 'w', encoding='utf-8') as m3u_file:
    m3u_file.write(m3u_file_content)

print("M3U dosyası oluşturuldu: output.m3u")
