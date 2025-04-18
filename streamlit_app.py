import streamlit as st

home_page = st.Page("home.py", title="Home", icon=":material/home:")
document_page = st.Page("./pages/document.py", title="Document", icon=":material/menu_book:")

pg = st.navigation([home_page, document_page])
# st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()