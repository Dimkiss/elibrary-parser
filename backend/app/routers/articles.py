from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db import AsyncSessionLocal
from app.models import Publication, JournalIssue

from fastapi import UploadFile, File
from bs4 import BeautifulSoup
from app.models import Publication, Author, Journal, JournalIssue
from sqlalchemy.exc import IntegrityError
import re

router = APIRouter()

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/parse")
async def parse_by_doi(doi: str = Query(..., description="DOI статьи"), session: AsyncSession = Depends(get_session)):
    from sqlalchemy.orm import selectinload
    from app.models import JournalIssue

    result = await session.execute(
        select(Publication)
        .options(
            selectinload(Publication.authors),
            selectinload(Publication.journal),
            selectinload(Publication.issue).selectinload(JournalIssue.journal)
        )
        .where(Publication.doi == doi)
    )
    publication = result.scalars().first()

    if not publication:
        raise HTTPException(status_code=404, detail="DOI not found")

    # подгружаем всё до выхода из сессии
    authors_data = [
        {
            "formatted": f"{a.lastname} {a.name[0]}.{(a.patronymic[0] + '.') if a.patronymic else ''}",
            "full": {
                "lastname": a.lastname,
                "name": a.name,
                "patronymic": a.patronymic,
                "affiliation": a.affiliation.split(";"),
                "ORCID": a.ORCID,
            }
        }
        for a in publication.authors
    ]

    journal_info = publication.journal
    issue_info = publication.issue

    return {
        "publication": {
            "title": publication.title,
            "authors": [a["formatted"] for a in authors_data],
            "doi": publication.doi,
            "keywords": publication.keywords.split(","),
            "abstract": publication.abstract,
            "journal": journal_info.title if journal_info else None,
            "year": publication.year,
            "volume": publication.volume,
            "number": publication.number,
            "pages": publication.pages,
        },
        "authors_info": [a["full"] for a in authors_data],
        "journal_issue": {
            "journal": issue_info.journal.title if issue_info and issue_info.journal else None,
            "year": issue_info.year if issue_info else None,
            "WoS": issue_info.WoS if issue_info else None,
            "Quartile_WoS": issue_info.Quartile_WoS if issue_info else None,
            "Scopus": issue_info.Scopus if issue_info else None,
            "Quartile_Scopus": issue_info.Quartile_Scopus if issue_info else None,
            "WhiteList": issue_info.WhiteList if issue_info else None,
            "Quartile_WL": issue_info.Quartile_WL if issue_info else None,
            "RINC_core": issue_info.RINC_core if issue_info else None,
        } if issue_info else None,
        "journal_info": {
            "title": journal_info.title if journal_info else None,
            "ISSN": journal_info.ISSN,
            "eISSN": journal_info.eISSN,
            "publisher": journal_info.publisher,
        } if journal_info else None,
    }

@router.post("/parse-local-article")
async def parse_local_article(session: AsyncSession = Depends(get_session)):
    with open("article.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Извлечение данных
    title = soup.title.string.strip()

    doi_tag = soup.find("meta", {"name": "doi"})
    doi = doi_tag["content"] if doi_tag else None

    abstract_block = soup.find("div", id="abstract1")
    abstract = abstract_block.get_text(strip=True) if abstract_block else ""

    keywords_block = soup.find(text=re.compile("КЛЮЧЕВЫЕ СЛОВА", re.I))
    if keywords_block:
        keyword_links = keywords_block.find_parent("table").find_all("a")
        keywords = [kw.get_text(strip=True) for kw in keyword_links]
    else:
        keywords = []

    journal_block = soup.find("a", href=re.compile("contents\.asp\?id="))
    journal_title = journal_block.get_text(strip=True) if journal_block else "Unknown Journal"

    year_match = re.search(r"Год:\s*([\d]{4})", soup.text)
    year = int(year_match.group(1)) if year_match else None

    volume = None  # Не найдено в статье
    number_match = re.search(r"Номер:\s*([\dA-Z]+)", soup.text)
    number = number_match.group(1) if number_match else None

    pages_match = re.search(r"Страницы:\s*([\d\-–]+)", soup.text)
    pages = pages_match.group(1) if pages_match else ""

    authors_raw = soup.find_all("span", class_="help pointer")
    authors = []
    for a in authors_raw:
        full = a.get_text(strip=True).replace(u'\xa0', ' ')
        initials = full.split()
        if len(initials) >= 2:
            lastname = initials[0].title()
            name = initials[1].replace(".", "").upper()
            authors.append({
                "lastname": lastname,
                "name": name,
                "patronymic": None,
                "affiliation": "Unknown",
                "ORCID": None,
            })

    # Сохранение данных
    journal = Journal(title=journal_title)
    session.add(journal)
    await session.flush()

    issue = JournalIssue(journal_id=journal.id, year=year, WoS=False,
                         Quartile_WoS=0, Scopus=False, Quartile_Scopus=0,
                         WhiteList=False, Quartile_WL=0, RINC_core=False)
    session.add(issue)
    await session.flush()

    author_objs = []
    for a in authors:
        author = Author(**a)
        session.add(author)
        await session.flush()
        author_objs.append(author)

    publication = Publication(
        title=title,
        doi=doi,
        abstract=abstract,
        keywords=",".join(keywords),
        year=year,
        volume=volume,
        number=number,
        pages=pages,
        journal_id=journal.id,
        issue_id=issue.id,
        authors=author_objs
    )

    session.add(publication)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Публикация уже существует")

    return {"detail": "Публикация успешно добавлена"}