import streamlit as st

st.set_page_config(
    page_title="CrimeGraph AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ CrimeGraph AI")
st.write("AI-powered criminal network analysis")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Entity Search",
        "Network",
        "Analytics",
        "Alerts",
        "Cases",
        "Intelligence"
    ]
)

if page == "Dashboard":
    from pages.dashboard import show
    show()

elif page == "Entity Search":
    from pages.search import show
    show()

elif page == "Network":
    from pages.network import show
    show()

elif page == "Analytics":
    from pages.analytics import show
    show()

elif page == "Alerts":
    from pages.alerts import show
    show()

elif page == "Cases":
    from pages.cases import show
    show()

elif page == "Intelligence":
    from pages.intelligence import show
    show()