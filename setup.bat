@echo off
chcp 65001

IF NOT EXIST venv (
    python -m venv venv
    echo Virtuális környezet létrehozva.
) ELSE (
    echo Virtuális környezet már létezik.
)

call venv\Scripts\activate.bat
echo Virtuális környezet aktiválva.

if exist requirements.txt (
    pip install -r requirements.txt
    echo Minden csomag telepítve a requirements.txt alapján
) ELSE (
    echo Nincs requirements.txt a projekt gyökerében!
)

echo ----------------------------------------
echo A virtuális környezet aktív és csomagok telepítve

echo ----------------------------------------
echo Backend indítása Uvicorn-nal...
uvicorn backend.main:app --reload

pause
