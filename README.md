# My Microservice Project

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
    - elindítja a FastAPI backend-et Uvicorn-nal
- `README.md` - ez a dokumentáció