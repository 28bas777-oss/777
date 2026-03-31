import requests
import re

# Настройки каналов (Название, URL страницы, Регулярное выражение для поиска ссылки)
# Регулярка r'https://[^"\']+?\.m3u8(?:\?key=[^"\']*)?' универсальна для многих сайтов
CHANNELS = [
    {
        "name": "Суспільне Спорт",
        "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
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
        "url": "https://telik.live/priklyucheniya-hd.html",
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
        print(f"--- Проверяю канал: {channel['name']} ---")
        response = requests.get(channel['url'], headers=HEADERS, timeout=15)
        
        # Твоя проверка (теперь внутри try/except)
        print(f"Длина полученного кода страницы: {len(response.text)}")
        
        if "Контент недоступний" in response.text or "not available" in response.text:
            print(f"ВНИМАНИЕ: Сайт выдает заглушку о недоступности контента!")
            return None

        # Ищем ссылку
        match = re.search(channel['regex'], response.text)
        if match:
            link = match.group(0)
            print(f"Успех! Ссылка найдена.")
            return link
        else:
            print(f"Регулярное выражение ничего не нашло. Возможно, структура сайта изменилась.")
            
    except Exception as e:
        print(f"Ошибка при запросе к {channel['name']}: {e}")
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
