import requests
from bs4 import BeautifulSoup
import string
from pathlib import Path
from requests.exceptions import RequestException


class ArticleCollector:
    def __init__(self, max_pages, target_category):
        self.max_pages = max_pages
        self.target_category = target_category
        self.web_address = "https://www.nature.com/nature/articles"
        self.http_client = requests.Session()
        # Настройка заголовков для обхода блокировок
        self.http_client.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        })

    def _format_file_name(self, raw_name):
        """Создает безопасное имя файла на основе заголовка."""
        # Удаляем лишние символы и заменяем пробелы
        chars_to_remove = string.punctuation.replace('-', '').replace('_', '')
        mapping = str.maketrans('', '', chars_to_remove)
        safe_name = raw_name.translate(mapping).replace(' ', '_')
        return f"{safe_name[:100]}.txt"

    def _fetch_url(self, target_url, query_params=None):
        """Выполняет запрос к серверу с контролем исключений."""
        try:
            output = self.http_client.get(target_url, params=query_params, timeout=25)
            output.raise_for_status()
            return output
        except RequestException as error:
            print(f"[!] Сбой при доступе к {target_url}: {error}")
            return None

    def _extract_body_text(self, link):
        """Находит и собирает текстовое содержимое статьи."""
        web_page = self._fetch_url(link)
        if not web_page:
            return None

        parser = BeautifulSoup(web_page.text, "html.parser")

        # Селекторы для поиска контента
        blocks = [
            "article.c-article-body",
            "div.main-content",
            "div[itemprop='articleBody']"
        ]

        for css_path in blocks:
            container = parser.select_one(css_path)
            if container:
                lines = container.find_all("p")
                merged_text = "\n".join(line.get_text(strip=True) for line in lines)
                if merged_text.strip():
                    return merged_text

        # Запасной вариант: краткое описание (teaser)
        short_desc = parser.find("p", class_="article__teaser")
        return short_desc.get_text(strip=True) if short_desc else ""

    def _scan_page_index(self, index):
        """Парсит одну страницу из общего списка."""
        print(f"[*] Изучение страницы №{index}...")

        params = {
            "searchType": "journalSearch",
            "sort": "PubDate",
            "year": "2024",  # Установлен текущий год
            "page": index
        }

        response = self._fetch_url(self.web_address, query_params=params)
        if not response:
            return

        parser = BeautifulSoup(response.text, "html.parser")

        # Подготовка папки для результатов
        target_dir = Path(f"Folder_Page_{index}")
        target_dir.mkdir(exist_ok=True)

        items = parser.find_all("article")
        if not items:
            print(f"[-] Страница {index} пуста.")
            return

        for entry in items:
            # Сверяем тип статьи
            label = entry.find("span", {"data-test": "article.type"})
            if not label or label.text.strip() != self.target_category:
                continue

            link_tag = entry.find("a", {"data-track-action": "view article"})
            if not link_tag:
                continue

            headline = link_tag.text.strip()
            full_link = "https://www.nature.com" + link_tag.get("href")

            print(f"    + Загрузка: {headline[:50]}...")

            body_content = self._extract_body_text(full_link)
            if body_content:
                filename = self._format_file_name(headline)
                destination = target_dir / filename
                try:
                    destination.write_text(body_content, encoding="utf-8")
                except IOError as err:
                    print(f"[!] Ошибка записи {filename}: {err}")

    def start_workflow(self):
        """Инициализация процесса сбора данных."""
        for p in range(1, self.max_pages + 1):
            self._scan_page_index(p)
        print("\n[+] Готово. Файлы распределены по папкам.")


def execute_scraper():
    while True:
        try:
            count = int(input("Введите количество страниц для обработки:\n> "))
            if count > 0:
                break
        except ValueError:
            pass
        print("Ошибка: необходимо положительное число.")

    genre = input("Укажите тип контента (например, Research Highlight):\n> ").strip()

    worker = ArticleCollector(count, genre)
    worker.start_workflow()


if __name__ == "__main__":
    execute_scraper()