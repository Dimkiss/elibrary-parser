import httpx
import asyncio
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36",
    "Referer": "https://elibrary.ru/querybox.asp?scope=newquery",
    "Origin": "https://elibrary.ru",
    "Content-Type": "application/x-www-form-urlencoded"
}

async def search_by_doi(doi: str):
    url = "https://www.elibrary.ru/query_results.asp"

    payload = {
        "querybox_name": "",
        "authors_all": "",
        "titles_all": "",
        "rubrics_all": "",
        "changed": "1",
        "queryid": "",
        "ftext": doi,
        "where_name": "on",
        "where_affiliation": "on",
        "where_abstract": "on",
        "where_fulltext": "on",
        "where_keywords": "on",
        "where_references": "",
        "type_article": "on",
        "search_itemboxid": "",
        "search_morph": "on",
        "begin_year": "0",
        "end_year": "0",
        "issues": "all",
        "orderby": "rank",
        "order": "rev",
        "queryboxid": "0",
        "save_queryboxid": "0"
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url, headers=HEADERS)
        cookies = response.cookies

        response = await client.post(url, data=payload, headers=HEADERS, cookies=cookies)
        print(response.status_code)

        soup = BeautifulSoup(response.text, "lxml")
        link_tag = soup.select_one('table#restab a[href^="/item.asp"]')

        if link_tag:
            article_url = "https://elibrary.ru" + link_tag["href"]
            print("Найденная статья:", article_url)
        else:
            print("Ссылка не найдена")

        # article_response = await client.get(article_url, cookies=cookie)
        # print(article_response.status_code)

doi = "10.31951/2658-3518-2023-A-4-119"
asyncio.run(search_by_doi(doi))
