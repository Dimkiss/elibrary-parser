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

from app.services.parser import fetch_article_info_from_doi

@router.post("/parse-by-doi-online")
async def parse_by_doi_online(doi: str = Query(...), session: AsyncSession = Depends(get_session)):
    data = await fetch_article_info_from_doi(doi)
    if not data:
        raise HTTPException(status_code=404, detail="Статья не найдена на eLibrary")

    journal = Journal(title=data["journal"])
    session.add(journal)
    await session.flush()

    issue = JournalIssue(
        journal_id=journal.id,
        year=data["year"],
        WoS=False,
        Quartile_WoS=0,
        Scopus=False,
        Quartile_Scopus=0,
        WhiteList=False,
        Quartile_WL=0,
        RINC_core=False
    )
    session.add(issue)
    await session.flush()

    author_objs = []
    for full in data["authors"]:
        parts = full.split()
        lastname = parts[0].title()
        name = parts[1][0] if len(parts) > 1 else "X"
        author = Author(lastname=lastname, name=name, patronymic=None, affiliation="Unknown", ORCID=None)
        session.add(author)
        await session.flush()
        author_objs.append(author)

    publication = Publication(
        title=data["title"],
        doi=data["doi"],
        abstract="",
        keywords="",
        year=data["year"],
        volume=None,
        number=data["number"],
        pages=data["pages"],
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

@router.get("/parse-lite")
async def parse_lite_by_doi(
    doi: str = Query(..., description="DOI статьи"),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Publication)
        .options(
            selectinload(Publication.authors),
            selectinload(Publication.journal)
        )
        .where(Publication.doi == doi)
    )
    publication = result.scalars().first()

    if not publication:
        raise HTTPException(status_code=404, detail="DOI не найден")

    return {
        "title": publication.title,
        "authors": [
            f"{a.lastname} {a.name[0]}." for a in publication.authors if a.name
        ],
        "doi": publication.doi,
        "keywords": publication.keywords.split(",") if publication.keywords else [],
        "abstract": publication.abstract,
        "year": publication.year,
        "volume": publication.volume,
        "number": publication.number,
        "pages": publication.pages,
    }

