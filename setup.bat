@echo off
chcp 65001

IF EXIST app.db (
    del app.db
    echo SQLite adatbázis törölve.
)

IF NOT EXIST venv (
    python -m venv venv
    echo ----------------------------------------
    echo Virtuális környezet létrehozva.
) ELSE (
    echo ----------------------------------------
    echo Virtuális környezet már létezik.
)

call venv\Scripts\activate.bat
echo ----------------------------------------
echo Virtuális környezet aktiválva.
echo ----------------------------------------

if exist requirements.txt (
    pip install -r backend/requirements.txt
    echo ----------------------------------------
    echo Minden csomag telepítve a requirements.txt alapján
) ELSE (
    echo ----------------------------------------
    echo Nincs requirements.txt a projekt gyökerében!
)

echo ----------------------------------------
echo A virtuális környezet aktív és csomagok telepítve

echo ----------------------------------------
echo Backend URL: http://127.0.0.1:8000
echo Swagger UI: http://127.0.0.1:8000/docs
REM echo Frontend Streamlit:
echo.

echo Backend indítása Uvicorn-nal...
uvicorn backend.main:app --reload

pause

pause
