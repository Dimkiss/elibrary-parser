# eLibrary Parser

Проект для поиска и добавления научных публикаций по DOI с использованием данных из eLibrary. Пользователь может ввести DOI, получить полную информацию о публикации и сохранить её в локальную базу данных. Также доступен просмотр всех добавленных статей с поддержкой поиска и пагинации.

## Стек технологий

### Backend:
- Python
- FastAPI
- SQLAlchemy
- httpx
- BeautifulSoup4
- SQLite

### Frontend:
- React + TypeScript + Vite

## Как запустить проект

### 1. Клонировать репозиторий
```
git clone https://github.com/Dimkiss/elibrary-parser.git
cd elibrary-parser
```
##  Backend
### Установка зависимостей
```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
### Запуск сервера
```
uvicorn app.main:app --reload
```
* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Получение публикаций: `GET /publications`
* Добавление по DOI: `POST /parse-by-doi-online?doi=...`

## Frontend
### Установка и запуск
```
cd frontend
npm install
npm run dev
```
* Приложение откроется на: [http://localhost:5173](http://localhost:5173)

## Возможности

* Добавление публикаций по DOI из eLibrary
* Автоматическое парсинг и сохранение в БД
* Интерфейс для поиска, просмотра и навигации по статьям
