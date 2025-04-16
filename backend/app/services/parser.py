import httpx
import asyncio
from bs4 import BeautifulSoup
# COOKIES = {
#     "SCookieGUID": "30C54E2D%2D24CE%2D4076%2D9E6E%2D4CE48D57122E",
#     "SUserID": "611277066",
#     "__utma": "216042306.1731073576.1742873088.1744694199.1744696613.10",
#     "__utmz": "216042306.1744186469.4.3.utmcsr=elibrary.ru|utmccn=(referral)|utmcmd=referral|utmcct=/",
#     "_ym_d": "1742873071",
#     "_ym_isad": "1",
#     "_ym_uid": "1742873071940753857"
# }
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36",
    "Referer": "https://elibrary.ru/querybox.asp?scope=newquery",
    "Origin": "https://elibrary.ru",
    "Content-Type": "application/x-www-form-urlencoded"
}
async def login_to_elibrary(client, login: str, password: str, cookies) -> httpx.AsyncClient:
    url = "https://elibrary.ru/start_session.asp"

    payload = {
        "rpage": "https://elibrary.ru/defaultx.asp",
        "login": login,
        "password": password
    }

    print("➡️ POST на start_session.asp")
    response = await client.post(url, data=payload, headers=HEADERS, cookies=cookies)

    print("🔐 Status:", response.status_code)
    if "SUserID" not in client.cookies:
        print("❌ Не удалось залогиниться.")
    else:
        print("✅ Успешный логин!")

    return client.cookies

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

# doi = "10.31951/2658-3518-2023-A-4-119"
# asyncio.run(search_by_doi(doi))
async def main():
    url = "https://www.elibrary.ru/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        cookies = response.cookies
        print("чё-нибудь")
        await asyncio.sleep(3)
        cookies = await login_to_elibrary(client, "D1mkiss", "8vi-GdP-N6m-8LX", cookies)
    # response = await client.get("https://elibrary.ru/item.asp?id=54754003")
    # print("Статус страницы статьи:", response.status_code)
    # print(response.text[:500])  # или сохраняем в файл
    # print(client)
    # async with httpx.AsyncClient(follow_redirects=True, cookies=COOKIES, headers=HEADERS) as client:
    #     url = "https://elibrary.ru/item.asp?id=54754003"
    #     response = await client.get(url)
    #     print("🔍 Статус:", response.status_code)
    #     print(response.text[:1000])
asyncio.run(main())