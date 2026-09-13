
import streamlit as st
import requests

# ============================================================
# CONFIG
# ============================================================

BACKEND_URL = "http://127.0.0.1:5000"


# ============================================================
# PAGE
# ============================================================

st.title("🔎 Entity Search")

st.write(
    "Search for a person by Person ID, name, or other information."
)

# ============================================================
# SEARCH BOX
# ============================================================

search = st.text_input(
    "Search Person ID or Name",
    placeholder="Example: P001 or John"
)

# ============================================================
# SEARCH
# ============================================================

if search.strip():

    try:

        response = requests.get(
            f"{BACKEND_URL}/api/search",
            params={"q": search.strip()},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.ConnectionError:

        st.error("❌ Backend is not running.")

        st.info(
            "Start the backend with:"
        )

        st.code(
            r"python backend\api.py"
        )

        st.stop()

    except requests.exceptions.Timeout:

        st.error(
            "❌ Backend request timed out."
        )

        st.stop()

    except requests.exceptions.RequestException as e:

        st.error(
            "❌ Search request failed."
        )

        st.code(str(e))

        st.stop()

    except Exception as e:

        st.error(
            "❌ Unexpected error."
        )

        st.code(str(e))

        st.stop()

    # ========================================================
    # RESULTS
    # ========================================================

    if data:

        st.success(
            f"Found {len(data)} result(s)."
        )

        st.dataframe(
            data,
            width="stretch",
            hide_index=True
        )

    else:

        st.warning(
            f"No entity found for '{search}'."
        )

else:

    st.info(
        "Enter a Person ID or name to search."
    )



