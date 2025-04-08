from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Elibrary Parser API",
    description="API для парсинга и обработки данных по DOI",
)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/parse")
async def parse_by_doi(doi: str = Query(..., description="DOI статьи")):
    return JSONResponse(content={
        "publication": {
            "title": f"Fake Article for DOI: {doi}",
            "authors": ["Ivanov I.I.", "Petrova A.B."],
            "doi": doi,
            "keywords": ["parsing", "api", "demo"],
            "abstract": "Это тестовая аннотация, сгенерированная для демонстрации.",
            "journal": "Demo Journal",
            "year": 2024,
            "volume": "5",
            "number": "2",
            "pages": "100-110"
        },
        "authors_info": [
            {
                "lastname": "Ivanov",
                "name": "Ivan",
                "patronymic": "Ivanovich",
                "affiliation": ["Demo University"],
                "ORCID": "0000-0000-0000-0001"
            },
            {
                "lastname": "Petrova",
                "name": "Anna",
                "patronymic": None,
                "affiliation": ["Demo Institute"],
                "ORCID": None
            }
        ],
        "journal_issue": {
            "journal": "Demo Journal",
            "year": 2024,
            "WoS": True,
            "Quartile_WoS": 2,
            "Scopus": True,
            "Quartile_Scopus": 1,
            "WhiteList": True,
            "Quartile_WL": 2,
            "RINC_core": True
        },
        "journal_info": {
            "title": "Demo Journal",
            "ISSN": "1111-2222",
            "eISSN": "3333-4444",
            "publisher": "Demo Publisher"
        }
    })
