import streamlit as st
import requests


# ============================================================
# CRIMEGRAPH AI - INTELLIGENCE PAGE
# ============================================================

BACKEND_URL = "http://127.0.0.1:5000"


# ============================================================
# BACKEND REQUEST FUNCTION
# ============================================================

def get_backend_data(endpoint):

    try:

        response = requests.get(
            f"{BACKEND_URL}{endpoint}",
            timeout=10
        )

        response.raise_for_status()

        return response.json(), None

    except requests.exceptions.ConnectionError:

        return None, "Backend is not running."

    except requests.exceptions.Timeout:

        return None, "Backend request timed out."

    except requests.exceptions.HTTPError as error:

        return None, f"Backend HTTP error: {error}"

    except requests.exceptions.RequestException as error:

        return None, f"Request failed: {error}"

    except Exception as error:

        return None, f"Unexpected error: {error}"


# ============================================================
# DISPLAY VALUE
# ============================================================

def format_key(key):

    return (
        str(key)
        .replace("_", " ")
        .replace("-", " ")
        .title()
    )


# ============================================================
# EXTRACT NUMERIC METRICS
# ============================================================

def extract_numeric_metrics(data, prefix=""):

    metrics = []

    if isinstance(data, dict):

        for key, value in data.items():

            metric_name = (
                f"{prefix}_{key}"
                if prefix
                else key
            )

            # Direct numeric value
            if isinstance(value, (int, float)) and not isinstance(value, bool):

                metrics.append(
                    (metric_name, value)
                )

            # Nested dictionary
            elif isinstance(value, dict):

                metrics.extend(
                    extract_numeric_metrics(
                        value,
                        metric_name
                    )
                )

    return metrics


# ============================================================
# INTELLIGENCE PAGE
# ============================================================

def show():

    st.title("🧠 Intelligence")

    st.write(
        "AI-assisted investigation support using "
        "network analytics and entity risk indicators."
    )

    st.caption(
        "All analytical results require human verification."
    )

    st.divider()


    # ========================================================
    # BACKEND CONNECTION
    # ========================================================

    st.subheader("🔌 Intelligence Engine")

    data, error = get_backend_data(
        "/api/analytics"
    )


    if error:

        st.error(
            f"❌ {error}"
        )

        st.info(
            "Start the backend in a separate terminal:"
        )

        st.code(
            "python backend/api.py",
            language="powershell"
        )

        return


    st.success(
        "🟢 Intelligence Engine Connected"
    )


    # ========================================================
    # ANALYTICS OVERVIEW
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Network Intelligence Overview"
    )


    # --------------------------------------------------------
    # Make sure backend returned a dictionary
    # --------------------------------------------------------

    if not isinstance(data, dict):

        st.warning(
            "Backend returned an unexpected response."
        )

        st.json(data)

        return


    # ========================================================
    # NUMERIC METRICS
    # ========================================================

    numeric_items = extract_numeric_metrics(data)


    if len(numeric_items) == 0:

        st.info(
            "No numeric analytics are currently available."
        )

    else:

        # ----------------------------------------------------
        # Display four metrics per row
        # ----------------------------------------------------

        for start in range(
            0,
            len(numeric_items),
            4
        ):

            row = numeric_items[
                start:start + 4
            ]

            columns = st.columns(
                len(row)
            )

            for column, item in zip(
                columns,
                row
            ):

                key, value = item

                with column:

                    # Format floating point numbers
                    if isinstance(value, float):

                        if abs(value) < 1:

                            display_value = f"{value:.3f}"

                        else:

                            display_value = f"{value:.2f}"

                    else:

                        display_value = value


                    st.metric(
                        format_key(key),
                        display_value
                    )


    # ========================================================
    # DETAILED ANALYTICS
    # ========================================================

    st.divider()

    st.subheader(
        "🔎 Detailed Intelligence"
    )


    for key, value in data.items():

        display_name = format_key(key)


        # ----------------------------------------------------
        # Dictionary
        # ----------------------------------------------------

        if isinstance(value, dict):

            with st.expander(
                display_name
            ):

                st.json(value)


        # ----------------------------------------------------
        # List
        # ----------------------------------------------------

        elif isinstance(value, list):

            with st.expander(
                display_name
            ):

                if len(value) == 0:

                    st.info(
                        "No records available."
                    )

                elif all(
                    isinstance(item, dict)
                    for item in value
                ):

                    st.dataframe(
                        value,
                        width="stretch"
                    )

                else:

                    for item in value:

                        st.write(
                            f"• {item}"
                        )


        # ----------------------------------------------------
        # String
        # ----------------------------------------------------

        elif isinstance(value, str):

            with st.expander(
                display_name
            ):

                st.write(value)


    # ========================================================
    # ENTITY RISK ANALYSIS
    # ========================================================

    st.divider()

    st.subheader(
        "⚠️ Entity Risk Analysis"
    )

    st.write(
        "Enter a Person ID to retrieve its analytical "
        "risk assessment from the backend."
    )


    person_id = st.text_input(
        "Person ID",
        placeholder="Example: P001"
    )


    if person_id:

        person_id = person_id.strip().upper()

        st.write(
            f"Searching for **{person_id}**..."
        )


        risk_data, risk_error = get_backend_data(
            f"/api/risk/{person_id}"
        )


        if risk_error:

            st.error(
                f"❌ {risk_error}"
            )


        elif risk_data is None:

            st.error(
                "❌ No risk information received."
            )


        else:

            st.success(
                f"Risk analysis received for {person_id}"
            )


            # =================================================
            # RISK DATA
            # =================================================

            if isinstance(
                risk_data,
                dict
            ):

                # -------------------------------------------------
                # Find score
                # -------------------------------------------------

                score = risk_data.get(
                    "Score",
                    risk_data.get(
                        "score",
                        None
                    )
                )


                # -------------------------------------------------
                # Find risk level
                # -------------------------------------------------

                level = risk_data.get(
                    "Level",
                    risk_data.get(
                        "level",
                        "UNKNOWN"
                    )
                )


                # -------------------------------------------------
                # Find reasons
                # -------------------------------------------------

                reasons = risk_data.get(
                    "Reasons",
                    risk_data.get(
                        "reasons",
                        []
                    )
                )


                # -------------------------------------------------
                # Risk cards
                # -------------------------------------------------

                col1, col2, col3 = st.columns(3)


                with col1:

                    if score is not None:

                        st.metric(
                            "Risk Score",
                            score
                        )

                    else:

                        st.metric(
                            "Risk Score",
                            "N/A"
                        )


                with col2:

                    st.metric(
                        "Risk Level",
                        str(level)
                    )


                with col3:

                    if isinstance(
                        reasons,
                        list
                    ):

                        st.metric(
                            "Risk Factors",
                            len(reasons)
                        )

                    else:

                        st.metric(
                            "Risk Factors",
                            "N/A"
                        )


                # =================================================
                # RISK LEVEL MESSAGE
                # =================================================

                level_text = str(
                    level
                ).upper()


                if level_text == "HIGH":

                    st.error(
                        "🔴 HIGH RISK INDICATOR"
                    )


                elif level_text == "MEDIUM":

                    st.warning(
                        "🟠 MEDIUM RISK INDICATOR"
                    )


                elif level_text == "LOW":

                    st.success(
                        "🟢 LOW RISK INDICATOR"
                    )


                else:

                    st.info(
                        "ℹ️ Risk level returned by backend."
                    )


                # =================================================
                # RISK REASONS
                # =================================================

                st.write(
                    "### 🧠 Risk Factors"
                )


                if (
                    isinstance(
                        reasons,
                        list
                    )
                    and len(reasons) > 0
                ):

                    for reason in reasons:

                        st.warning(
                            f"• {reason}"
                        )

                else:

                    st.info(
                        "No specific risk factors returned."
                    )


                # =================================================
                # COMPLETE RESPONSE
                # =================================================

                with st.expander(
                    "View complete backend response"
                ):

                    st.json(
                        risk_data
                    )


            else:

                st.write(
                    risk_data
                )


    # ========================================================
    # INVESTIGATION GUIDANCE
    # ========================================================

    st.divider()

    st.subheader(
        "🧭 Investigation Support"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.info(
            "Network analytics can help identify "
            "highly connected entities and potential "
            "bridging positions within a network."
        )


    with col2:

        st.info(
            "Risk scores are analytical indicators, "
            "not conclusions of criminal activity."
        )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.divider()

    st.caption(
        "⚠️ CrimeGraph AI is an investigation-support "
        "prototype. Analytical indicators should be "
        "independently verified by authorized personnel "
        "before any decision is made."
    )


# ============================================================
# PAGE ENTRY
# ============================================================

if __name__ == "__main__":

    show()

