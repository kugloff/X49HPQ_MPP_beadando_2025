import streamlit as st
import requests

# Backend URL
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="TODO App",
    layout="centered"
)

st.title("TODO Lista alkalmazás")

# Menü
menu = ["Összes TODO", "Új TODO létrehozása", "Statisztika"]
choice = st.sidebar.selectbox("Menü", menu)

# Lista megjelenítése
if choice == "Összes TODO":
    st.subheader("Összes TODO")
    try:
        response = requests.get(f"{BASE_URL}/items/")
        if response.status_code == 200:
            items = response.json()
            for item in items:
                st.write(f"- **{item['name']}** ({item['status']}): {item['description']}")
        else:
            st.error("Nem sikerült lekérni az adatokat a backendről.")
    except Exception as e:
        st.error(f"Hiba történt: {e}")

# Új todo létrehozása
elif choice == "Új TODO létrehozása":
    st.subheader("Új TODO létrehozása")
    name = st.text_input("Név")
    description = st.text_area("Leírás")
    if st.button("Hozzáadás"):
        if name and description:
            try:
                response = requests.post(f"{BASE_URL}/items/", json={"name": name, "description": description})
                if response.status_code == 200 or response.status_code == 201:
                    st.success("TODO sikeresen hozzáadva!")
                else:
                    st.error("Nem sikerült hozzáadni a TODO-t.")
            except Exception as e:
                st.error(f"Hiba történt: {e}")
        else:
            st.warning("Kérlek töltsd ki a mezőket.")

# Statisztika / Vizualizáció
elif choice == "Statisztika":
    st.subheader("TODO vizualizációja")
    try:
        response = requests.get(f"{BASE_URL}/items/")
        if response.status_code == 200:
            items = response.json()
            status_count = {"pending": 0, "done": 0}
            for item in items:
                status = item.get("status", "pending")
                if status not in status_count:
                    status_count[status] = 0
                status_count[status] += 1
            
            st.bar_chart(status_count)
        else:
            st.error("Nem sikerült lekérni az adatokat a backendről.")
    except Exception as e:
        st.error(f"Hiba történt: {e}")