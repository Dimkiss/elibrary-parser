import asyncio
from app.db import AsyncSessionLocal, engine
from app.models import Base, Author, Journal, JournalIssue, Publication

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        journal = Journal(title="Demo Journal", ISSN="1111-2222", eISSN="3333-4444", publisher="Demo Publisher")
        session.add(journal)
        await session.flush()

        issue = JournalIssue(
            journal_id=journal.id,
            year=2024,
            WoS=True,
            Quartile_WoS=2,
            Scopus=True,
            Quartile_Scopus=1,
            WhiteList=True,
            Quartile_WL=2,
            RINC_core=True,
        )
        session.add(issue)
        await session.flush()

        author1 = Author(lastname="Ivanov", name="Ivan", patronymic="Ivanovich", affiliation="Demo University", ORCID="0000-0000-0000-0001")
        author2 = Author(lastname="Petrova", name="Anna", patronymic=None, affiliation="Demo Institute", ORCID=None)
        session.add_all([author1, author2])
        await session.flush()

        publication = Publication(
            title="Fake Article for DOI: 10.0000/fake.doi",
            doi="10.0000/fake.doi",
            abstract="Это тестовая аннотация.",
            keywords="parsing,api,demo",
            year=2024,
            volume="5",
            number="2",
            pages="100-110",
            journal_id=journal.id,
            issue_id=issue.id,
            authors=[author1, author2]
        )
        session.add(publication)
        await session.commit()

asyncio.run(seed())
