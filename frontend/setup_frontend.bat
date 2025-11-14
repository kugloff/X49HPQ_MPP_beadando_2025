@echo off
chcp 65001

echo ----------------------------------------
echo Streamlit frontend indítása...
echo ----------------------------------------

call ..\venv\Scripts\activate.bat
echo Virtuális környezet aktiválva.

streamlit run app.py

pause