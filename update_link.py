import requests
import re

# Настройки каналов (Название, URL страницы, Регулярное выражение для поиска ссылки)
# Регулярка r'https://[^"\']+?\.m3u8(?:\?key=[^"\']*)?' универсальна для многих сайтов
CHANNELS = [
    {
        "name": "Суспільне Спорт",
        "url": "https://suspilne.media/sport/live/",
        "regex": r'https://[^\s"\'<>]+?\.m3u8\?key=[^\s"\'<>]+',
        "logo": "https://suspilne.media/favicon.ico"
    },
    {
        "name": "Суспільне Харків",
        "url": "https://suspilne.media/kharkiv/live/",
        "regex": r'https://[^\s"\'<>]+?\.m3u8\?key=[^\s"\'<>]+',
        "logo": "https://suspilne.media/favicon.ico"
    },
    {
        "name": "ТВ-3 (Viks)",
        "url": "http://live.viks.tv/tv3/",
        # Для Viks регулярка может быть чуть другой, пробуем универсальную:
        "regex": r'https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*',
        "logo": "http://viks.tv/favicon.ico"
    }
]

FILE_NAME = "playlist.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_stream_link(channel):
    try:
        print(f"Ищу ссылку для: {channel['name']}...")
        response = requests.get(channel['url'], headers=HEADERS, timeout=15)
        response.raise_for_status()
        print(f"Длина полученного кода страницы: {len(response.text)}")
if "Контент недоступний" in response.text or "not available" in response.text:
    print(f"ВНИМАНИЕ: Похоже, сайт заблокировал доступ для сервера GitHub")

match = re.search(channel['regex'], response.text)
        if match:
            return match.group(0)
    except Exception as e:
        print(f"Ошибка при поиске {channel['name']}: {e}")
    return None

def main():
    playlist_content = "#EXTM3U\n"
    found_count = 0

    for ch in CHANNELS:
        link = get_stream_link(ch)
        if link:
            playlist_content += f"#EXTINF:-1 tvg-logo=\"{ch['logo']}\" group-title=\"Украина\", {ch['name']}\n"
            playlist_content += f"{link}\n"
            found_count += 1
            print(f"Успех для {ch['name']}")
        else:
            print(f"Не удалось найти ссылку для {ch['name']}")

    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write(playlist_content)
    
    print(f"\nГотово! Собрано каналов: {found_count} из {len(CHANNELS)}")

if __name__ == "__main__":
    main()
