from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from app.db import Base

# many-to-many между публикациями и авторами
publication_author = Table(
    "publication_author",
    Base.metadata,
    Column("publication_id", Integer, ForeignKey("publications.id")),
    Column("author_id", Integer, ForeignKey("authors.id")),
)

class Journal(Base):
    __tablename__ = "journals"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    ISSN = Column(String, nullable=True)
    eISSN = Column(String, nullable=True)
    publisher = Column(String, nullable=True)

class JournalIssue(Base):
    __tablename__ = "journal_issues"
    id = Column(Integer, primary_key=True)
    journal_id = Column(Integer, ForeignKey("journals.id"))
    journal = relationship("Journal")
    year = Column(Integer)
    WoS = Column(Boolean)
    Quartile_WoS = Column(Integer)
    Scopus = Column(Boolean)
    Quartile_Scopus = Column(Integer)
    WhiteList = Column(Boolean)
    Quartile_WL = Column(Integer)
    RINC_core = Column(Boolean)

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    lastname = Column(String)
    name = Column(String)
    patronymic = Column(String, nullable=True)
    affiliation = Column(String)
    ORCID = Column(String, nullable=True)

class Publication(Base):
    __tablename__ = "publications"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    doi = Column(String, unique=True, index=True)
    abstract = Column(Text)
    keywords = Column(String)
    year = Column(Integer)
    volume = Column(String, nullable=True)
    number = Column(String, nullable=True)
    pages = Column(String)

    journal_id = Column(Integer, ForeignKey("journals.id"))
    journal = relationship("Journal")

    issue_id = Column(Integer, ForeignKey("journal_issues.id"))
    issue = relationship("JournalIssue")

    authors = relationship("Author", secondary=publication_author, backref="publications")
