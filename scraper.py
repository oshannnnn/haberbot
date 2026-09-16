import os
import requests
from bs4 import BeautifulSoup

NEWS_URL = "https://neu.edu.tr/category/haberler/"

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def get_news():
   headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://neu.edu.tr/",
    "Connection": "keep-alive",
}

response = requests.get(
    NEWS_URL,
    headers=headers,
    timeout=30
)

print("HTTP durumu:", response.status_code)

response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    news = []

    for a in soup.find_all("a", href=True):

        title = a.get_text(" ", strip=True)
        link = a["href"]

        if (
            len(title) > 20
            and "neu.edu.tr" in link
            and link != NEWS_URL
        ):
            news.append({
                "title": title,
                "link": link
            })

    return news


def send_telegram(title, link):

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    message = (
        "📰 <b>YDÜ HABER TESTİ</b>\n\n"
        f"<b>{title}</b>\n\n"
        f"🔗 {link}"
    )

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        },
        timeout=30
    )

    response.raise_for_status()


if __name__ == "__main__":

    print("YDÜ haber sayfası kontrol ediliyor...")

    news = get_news()

    print(f"{len(news)} haber bulundu.")

    if news:
        first = news[0]

        print("Gönderiliyor:")
        print(first["title"])
        print(first["link"])

        send_telegram(
            first["title"],
            first["link"]
        )

        print("Telegram mesajı gönderildi!")

    else:
        print("Haber bulunamadı.")
