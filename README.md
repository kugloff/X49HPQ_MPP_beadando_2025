# My Microservice Project - TODO-list

## Rövid bemutatás

Ez a projekt egy mikroszerviz-szerű Python alkalmazás, amely demonstrálja a **procedurális, funkcionális és objektumorientált programozás** alkalmazását.  
A rendszer tartalmaz FastAPI alapú backend-et, Streamlit frontend-et, SQLAlchemy ORM alapú adatbázist, valamint automatizált feladatvégzést.

Streamlit app backend nélkül: https://x49hpqmppbeadando2025.streamlit.app

## Használat:

- Backend indítása:
    - A projekt gyökerében futtasd a `setup.bat` fájlt
        - virtuális környezet létrehozása és csomagok telepítése `requirements.txt` alapján
        - tájékoztat, hogy milyen URL-en érhető el a backend (FastAPI)
        - elindítja a FastAPI backend-et Uvicorn-nal
- Frontend indítása:
    - A frontend mappában található `setup_frontend.bat` fájlt futtasd
        - frontend indítása Streamlit-el
        - a FastAPI backend CRUD végpontjait használja

## Architektúra

- **Backend (FastAPI)**
- **Frontend (Streamlit)**
- **Database (SQLite)**
- **Automatizáció**

## Mappastruktúra

- `backend/` - API, modellek, szolgáltatások, adatbázis
- `frontend/` - Streamlit app és komponensek
- `frontend/setup_frontend.bat` - frontend indítása
- `venv/` - virtuális környezet
- `requirements.txt` - szükséges csomagok (fastapi, uvicorn, streamlit, sqlalchemy, pydantic)
- `setup.bat` - backend indítása
- `README.md` - ez a dokumentáció

## API végpontok

- A backend FastAPI-vel készült, és az alábbi CRUD végpontokat tartalmazza a TODO elemekhez:

    - `GET /items/` - minden TODO listázása
    - `POST /items/` - új TODO létrehozása
    - `GET /items/{id}` - egy TODO lekérése ID alapján
    - `PUT /items/{id}` - egy TODO frissítése
    - `DELETE /items/{id}` - egy TODO törlése