import os
import requests

NEWS_URL = "https://neu.edu.tr/category/haberler/"

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def test_site():
    print("YDÜ sitesi test ediliyor...")

    response = requests.get(
        NEWS_URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    print("HTTP durumu:", response.status_code)
    print("Sayfa uzunluğu:", len(response.text))

    if response.status_code == 200:
        print("YDÜ sitesine erişim başarılı.")
    else:
        print("YDÜ sitesi isteği reddetti.")


if __name__ == "__main__":
    test_site()
