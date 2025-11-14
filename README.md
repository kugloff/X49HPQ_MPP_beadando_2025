# My Microservice Project - TODO-list

## Rövid bemutatás

Ez a projekt egy mikroszerviz-szerű Python alkalmazás, amely demonstrálja a **procedurális, funkcionális és objektumorientált programozás** alkalmazását.  
A rendszer tartalmaz FastAPI alapú backend-et, Streamlit frontend-et, SQLAlchemy ORM alapú adatbázist, valamint automatizált feladatvégzést.

## Architektúra

- **Backend (FastAPI)**
- **Frontend (Streamlit)**
- **Database (SQLite)**
- **Automatizáció**

## Mappastruktúra

- `backend/` - API, modellek, szolgáltatások, adatbázis
- `frontend/` - Streamlit app és komponensek
- `venv/` - virtuális környezet
- `requirements.txt` - szükséges csomagok (fastapi, uvicorn, streamlit, sqlalchemy, pydantic)
- `setup.bat`
    - virtuális környezet létrehozása és csomagok telepítése `requirements.txt` alapján
    - tájékoztat, hogy milyen URL-en érhető el a backend (FastAPI)
    - elindítja a FastAPI backend-et Uvicorn-nal
- `README.md` - ez a dokumentáció

## API végpontok

- A backend FastAPI-vel készült, és az alábbi CRUD végpontokat tartalmazza a TODO itemekhez:

    - `GET /items/` - minden item listázása
    - `POST /items/` - új item létrehozása
    - `GET /items/{id}` - egy item lekérése ID alapján
    - `PUT /items/{id}` - egy item frissítése
    - `DELETE /items/{id}` - egy item törlése