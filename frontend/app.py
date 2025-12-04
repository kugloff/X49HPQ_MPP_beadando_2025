import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date

BASE_URL = "https://x49hpq-mpp-beadando-2025.onrender.com"

st.set_page_config(page_title="TODO App", layout="centered")
st.title("TODO Lista alkalmazás")

choice = st.sidebar.selectbox("Menü", ["TODO lista", "Új TODO", "Statisztika"])

if choice == "TODO lista":
    st.subheader("TODO lista")

    try:
        response = requests.get(f"{BASE_URL}/items/")
        items = response.json()

        pending_items = [i for i in items if i["status"] != "done"]
        done_items = [i for i in items if i["status"] == "done"]

        st.markdown("### Folyamatban lévő feladatok")

        if not pending_items:
            st.info("Nincs folyamatban lévő feladat.")
        else:
            for item in pending_items:
                col1, col2 = st.columns([5, 2])

                due_date_obj = datetime.fromisoformat(item['due_date']).date() if item.get("due_date") else None
                due_str = f" (Határidő: {due_date_obj})" if due_date_obj else ""
                if due_date_obj and due_date_obj < date.today():
                    due_str += " ⚠️ Lejárt!"

                with col1:
                    st.markdown(f"**{item['name']}** - {item['description']}{due_str}")

                with col2:
                    c1, c2 = st.columns(2)

                    if c1.button("Kész", key=f"done_{item['id']}"):
                        requests.put(
                            f"{BASE_URL}/items/{item['id']}",
                            json={"status": "done"}
                        )
                        st.rerun()

                    if c2.button("Törlés", key=f"delete_{item['id']}"):
                        requests.delete(f"{BASE_URL}/items/{item['id']}")
                        st.rerun()

        st.markdown("---")
        st.markdown("### Kész feladatok")

        if not done_items:
            st.info("Még nincs kész feladat.")
        else:
            for item in done_items:
                due_str = f" (Határidő: {item['due_date'][:10]})" if item.get("due_date") else ""
                col1, col2 = st.columns([5, 2])

                with col1:
                    st.write(f"~~{item['name']} - {item['description']}{due_str}~~")

                with col2:
                    if st.button("Törlés", key=f"delete_done_{item['id']}"):
                        requests.delete(f"{BASE_URL}/items/{item['id']}")
                        st.rerun()

    except Exception as e:
        st.error(f"Hiba történt: {e}")

elif choice == "Új TODO":
    st.subheader("Új TODO hozzáadása")

    with st.form("todo_form", clear_on_submit=False):
        name = st.text_input("Név")
        description = st.text_area("Leírás")
        due_date = st.date_input("Határidő")
        submit = st.form_submit_button("Hozzáadás")

        if submit:
            name_val = name.strip()
            desc_val = description.strip()

            if not name_val or not desc_val:
                st.error("Minden mezőt ki kell tölteni!")
            else:
                payload = {
                    "name": name_val,
                    "description": desc_val,
                    "due_date": datetime.combine(due_date, datetime.min.time()).isoformat() if due_date else None
                }
                try:
                    resp = requests.post(f"{BASE_URL}/items/", json=payload)
                    if resp.status_code in (200, 201):
                        st.success("TODO sikeresen hozzáadva!")
                    elif resp.status_code == 400:
                        st.error(resp.json().get("detail", "Hiba történt a hozzáadáskor."))
                    else:
                        st.error("Nem sikerült hozzáadni.")
                except Exception as e:
                    st.error(f"Hiba történt: {e}")

elif choice == "Statisztika":
    st.subheader("TODO statisztika")

    try:
        response = requests.get(f"{BASE_URL}/items/")
        items = response.json()

        pending_items = [i for i in items if i["status"] != "done"]
        done_items = [i for i in items if i["status"] == "done"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Folyamatban lévő")
            st.markdown(f"**Összesen:** {len(pending_items)} db")
            for item in pending_items:
                st.write(f"- **{item['name']}**: {item['description']}")

        with col2:
            st.markdown("### Kész")
            st.markdown(f"**Összesen:** {len(done_items)} db")
            for item in done_items:
                st.write(f"- ~~{item['name']}~~")

        st.markdown("---")
        st.markdown("### Állapotdiagram")

        df = pd.DataFrame({
            "Állapot": ["Folyamatban", "Kész"],
            "Darab": [len(pending_items), len(done_items)]
        })

        st.bar_chart(df, x="Állapot", y="Darab")

    except Exception as e:
        st.error(f"Hiba történt: {e}")