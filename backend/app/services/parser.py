# import httpx
# import asyncio
# from bs4 import BeautifulSoup

# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36",
#     "Referer": "https://www.elibrary.ru/defaultx.asp",
#     "Origin": "https://www.elibrary.ru",
#     "Content-Type": "application/x-www-form-urlencoded"
# }

# async def search_by_doi_and_print_article(doi: str):
#     search_url = "https://www.elibrary.ru/query_results.asp"

#     payload = {
#         "ftext": doi,
#         "where_name": "on",
#         "where_affiliation": "on",
#         "where_abstract": "on",
#         "where_fulltext": "on",
#         "where_keywords": "on",
#         "type_article": "on",
#         "orderby": "rank",
#         "order": "rev",
#     }

#     async with httpx.AsyncClient(follow_redirects=True) as client:
#         await client.get("https://www.elibrary.ru", headers=HEADERS)

#         response = await client.post(search_url, data=payload, headers=HEADERS)
#         soup = BeautifulSoup(response.text, "lxml")
#         link_tag = soup.select_one('table#restab a[href^="/item.asp"]')

#         if not link_tag:
#             print("❌ Статья по DOI не найдена")
#             return

#         article_url = "https://www.elibrary.ru" + link_tag["href"]
#         print(f"🔗 Найдена статья: {article_url}")

#         article_response = await client.get(article_url, headers=HEADERS)

#         # Сохраняем HTML в файл
#         with open("article.html", "w", encoding="utf-8") as f:
#             f.write(article_response.text)

#         print("✅ HTML статьи сохранён в 'article.html'")

#         # Также печатаем кусок в консоль
#         print("📄 HTML статьи (первые 2000 символов):")
#         print(article_response.text[:2000])

# # Пример использования
# doi = "10.31951/2658-3518-2023-A-4-119"
# asyncio.run(search_by_doi_and_print_article(doi))
import httpx
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.elibrary.ru/defaultx.asp",
    "Origin": "https://www.elibrary.ru",
    "Content-Type": "application/x-www-form-urlencoded"
}

async def fetch_article_info_from_doi(doi: str):
    search_url = "https://www.elibrary.ru/query_results.asp"
    payload = {
        "ftext": doi,
        "where_name": "on",
        "where_affiliation": "on",
        "where_abstract": "on",
        "where_fulltext": "on",
        "where_keywords": "on",
        "type_article": "on",
        "orderby": "rank",
        "order": "rev",
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        await client.get("https://www.elibrary.ru", headers=HEADERS)
        response = await client.post(search_url, data=payload, headers=HEADERS)

    soup = BeautifulSoup(response.text, "lxml")
    row = soup.select_one("table#restab tr[id^=a]")
    if not row:
        return None

    cols = row.find_all("td")
    info_block = cols[1]

    title = info_block.select_one("a[href^='/item.asp'] span")
    title = title.get_text(strip=True) if title else "Без названия"

    authors_tag = info_block.select_one("font i")
    authors = [a.strip() for a in authors_tag.get_text(strip=True).split(",")] if authors_tag else []

    journal_info = info_block.find_all("font")[-1].get_text(" ", strip=True)
    journal = journal_info.split(".")[0].strip()
    year = int(re.search(r"\b(19|20)\d{2}\b", journal_info).group()) if re.search(r"\b(19|20)\d{2}\b", journal_info) else None
    number = re.search(r"№\s*([\dA-Z]+)", journal_info)
    number = number.group(1) if number else None
    pages = re.search(r"С\.\s*([\d\-–]+)", journal_info)
    pages = pages.group(1) if pages else ""

    return {
        "title": title,
        "authors": authors,
        "journal": journal,
        "year": year,
        "number": number,
        "pages": pages,
        "doi": doi,
    }
