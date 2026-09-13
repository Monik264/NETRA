import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"


def show():

    st.title("🏠 CrimeGraph AI Dashboard")

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/dashboard",
            timeout=5
        )

        response.raise_for_status()
        data = response.json()

    except Exception:
        st.error("Backend is not running.")
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👤 Persons", data["persons"])

    with col2:
        st.metric("📞 Calls", data["calls"])

    with col3:
        st.metric("💰 Transactions", data["transactions"])

    with col4:
        st.metric("📁 Cases", data["cases"])

import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"


st.title("🏠 CrimeGraph AI Dashboard")

try:
    response = requests.get(
        f"{BACKEND_URL}/api/dashboard",
        timeout=5
    )

    response.raise_for_status()
    data = response.json()

except Exception as e:
    st.error("Backend is not running.")
    st.code(str(e))
    st.stop()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👤 Persons", data.get("persons", 0))

with col2:
    st.metric("📞 Calls", data.get("calls", 0))

with col3:
    st.metric("💰 Transactions", data.get("transactions", 0))

with col4:
    st.metric("📁 Cases", data.get("cases", 0))

