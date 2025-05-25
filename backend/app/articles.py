from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db import AsyncSessionLocal
from app.models import Publication, Author, Journal, JournalIssue
from sqlalchemy.exc import IntegrityError
import re
from app.parser import fetch_article_info_from_doi
from fastapi.responses import JSONResponse
from sqlalchemy import or_

router = APIRouter()

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

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

@router.get("/publications")
async def list_publications(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    query: str = Query("", description="Поиск по DOI, названию, автору, журналу"),
    session: AsyncSession = Depends(get_session)
):
    offset = (page - 1) * per_page

    stmt = (
        select(Publication)
        .options(selectinload(Publication.authors), selectinload(Publication.journal))
        .offset(offset)
        .limit(per_page)
    )

    if query:
        stmt = stmt.where(
            or_(
                Publication.doi.ilike(f"%{query}%"),
                Publication.title.ilike(f"%{query}%"),
                Publication.journal.has(Journal.title.ilike(f"%{query}%")),
                Publication.authors.any(Author.lastname.ilike(f"%{query}%")),
            )
        )

    result = await session.execute(stmt)
    publications = result.scalars().all()

    return JSONResponse([
        {
            "title": pub.title,
            "doi": pub.doi,
            "authors": [f"{a.lastname} {a.name[0]}." for a in pub.authors],
            "journal": pub.journal.title if pub.journal else None,
            "year": pub.year,
        }
        for pub in publications
    ])
