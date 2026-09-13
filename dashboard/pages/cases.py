
import streamlit as st
import pandas as pd
import networkx as nx
import os

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CrimeGraph AI - Cases",
    page_icon="📁",
    layout="wide"
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

DATA_DIR = os.path.join(BASE_DIR, "data")


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    persons_path = os.path.join(DATA_DIR, "persons.csv")
    calls_path = os.path.join(DATA_DIR, "calls.csv")
    transactions_path = os.path.join(DATA_DIR, "transactions.csv")
    cases_path = os.path.join(DATA_DIR, "cases.csv")

    vehicles_path = os.path.join(DATA_DIR, "vehicles.csv")
    locations_path = os.path.join(DATA_DIR, "locations.csv")

    # Check required files
    required_files = {
        "persons.csv": persons_path,
        "calls.csv": calls_path,
        "transactions.csv": transactions_path,
        "cases.csv": cases_path
    }

    for filename, path in required_files.items():
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"{filename} not found at: {path}"
            )

        if os.path.getsize(path) == 0:
            raise ValueError(
                f"{filename} is empty: {path}"
            )

    # Load required datasets
    persons = pd.read_csv(persons_path)
    calls = pd.read_csv(calls_path)
    transactions = pd.read_csv(transactions_path)
    cases = pd.read_csv(cases_path)

    # Load optional datasets
    vehicles = (
        pd.read_csv(vehicles_path)
        if os.path.exists(vehicles_path)
        and os.path.getsize(vehicles_path) > 0
        else pd.DataFrame()
    )

    locations = (
        pd.read_csv(locations_path)
        if os.path.exists(locations_path)
        and os.path.getsize(locations_path) > 0
        else pd.DataFrame()
    )

    return (
        persons,
        calls,
        transactions,
        cases,
        vehicles,
        locations
    )


# ============================================================
# LOAD DATA SAFELY
# ============================================================

try:

    (
        persons,
        calls,
        transactions,
        cases,
        vehicles,
        locations
    ) = load_data()

except Exception as e:

    st.error("Unable to load case data.")
    st.code(str(e))
    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("📁 Case Investigation")

st.write(
    """
    Centralized investigation workspace for reviewing cases,
    associated persons, communications, financial activity,
    vehicles and locations.
    """
)

st.divider()


# ============================================================
# CASE STATISTICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Cases",
        len(cases)
    )

with col2:
    st.metric(
        "Persons",
        len(persons)
    )

with col3:
    st.metric(
        "Calls",
        len(calls)
    )

with col4:
    st.metric(
        "Transactions",
        len(transactions)
    )


st.divider()


# ============================================================
# CASE SELECTION
# ============================================================

if "Case_ID" not in cases.columns:

    st.error(
        "cases.csv is missing the Case_ID column."
    )

    st.write("Columns found:")
    st.write(list(cases.columns))

    st.stop()


case_ids = cases[
    "Case_ID"
].astype(str).tolist()


if len(case_ids) == 0:

    st.warning(
        "No cases available."
    )

    st.stop()


selected_case = st.selectbox(
    "Select Case",
    case_ids
)


case_data = cases[
    cases["Case_ID"].astype(str) == selected_case
]


# ============================================================
# CASE DETAILS
# ============================================================

st.header(
    f"📂 Case {selected_case}"
)

st.subheader(
    "Case Information"
)

st.dataframe(
    case_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# GET ASSOCIATED PERSON
# ============================================================

if "Person_ID" in case_data.columns and len(case_data) > 0:

    person_id = str(
        case_data.iloc[0]["Person_ID"]
    )

else:

    person_id = None


# ============================================================
# PERSON INFORMATION
# ============================================================

st.divider()

st.subheader(
    "👤 Primary Entity"
)


if person_id:

    person_data = persons[
        persons["Person_ID"].astype(str) == person_id
    ]

else:

    person_data = pd.DataFrame()


if len(person_data) > 0:

    st.dataframe(
        person_data,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No primary entity information available."
    )


# ============================================================
# COMMUNICATION
# ============================================================

st.divider()

st.subheader(
    "📞 Communication Records"
)


if person_id:

    person_calls = calls[
        (
            calls["Caller"].astype(str) == person_id
        )
        |
        (
            calls["Receiver"].astype(str) == person_id
        )
    ]

else:

    person_calls = pd.DataFrame()


if len(person_calls) > 0:

    st.write(
        f"{len(person_calls)} related communication records."
    )

    st.dataframe(
        person_calls,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No communication records found."
    )


# ============================================================
# TRANSACTIONS
# ============================================================

st.divider()

st.subheader(
    "💰 Financial Activity"
)


if person_id:

    person_transactions = transactions[
        (
            transactions["Sender"].astype(str) == person_id
        )
        |
        (
            transactions["Receiver"].astype(str) == person_id
        )
    ]

else:

    person_transactions = pd.DataFrame()


if len(person_transactions) > 0:

    amounts = pd.to_numeric(
        person_transactions["Amount"],
        errors="coerce"
    ).fillna(0)

    total_value = amounts.sum()
    average_value = amounts.mean()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Transactions",
            len(person_transactions)
        )

    with c2:

        st.metric(
            "Total Value",
            f"₹{total_value:,.0f}"
        )

    with c3:

        st.metric(
            "Average Value",
            f"₹{average_value:,.0f}"
        )

    st.dataframe(
        person_transactions,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No financial records found."
    )


# ============================================================
# VEHICLES
# ============================================================

st.divider()

st.subheader(
    "🚗 Associated Vehicles"
)


person_vehicles = pd.DataFrame()


if len(vehicles) > 0 and person_id:

    possible_person_columns = [
        "Person_ID",
        "person_id",
        "Owner_ID",
        "Owner"
    ]

    vehicle_person_column = None

    for column in possible_person_columns:

        if column in vehicles.columns:

            vehicle_person_column = column
            break

    if vehicle_person_column:

        person_vehicles = vehicles[
            vehicles[
                vehicle_person_column
            ].astype(str) == person_id
        ]


if len(person_vehicles) > 0:

    st.dataframe(
        person_vehicles,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No vehicles linked to this entity."
    )


# ============================================================
# LOCATIONS
# ============================================================

st.divider()

st.subheader(
    "📍 Associated Locations"
)


person_locations = pd.DataFrame()


if len(locations) > 0 and person_id:

    possible_person_columns = [
        "Person_ID",
        "person_id",
        "Person",
        "Entity_ID"
    ]

    location_person_column = None

    for column in possible_person_columns:

        if column in locations.columns:

            location_person_column = column
            break

    if location_person_column:

        person_locations = locations[
            locations[
                location_person_column
            ].astype(str) == person_id
        ]


if len(person_locations) > 0:

    st.dataframe(
        person_locations,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No locations linked to this entity."
    )


# ============================================================
# NETWORK CONNECTIONS
# ============================================================

st.divider()

st.subheader(
    "🕸️ Network Connections"
)


G = nx.Graph()


# Add persons
for _, row in persons.iterrows():

    pid = str(row["Person_ID"])

    G.add_node(pid)


# Add call relationships
for _, row in calls.iterrows():

    a = str(row["Caller"])
    b = str(row["Receiver"])

    if a in G.nodes and b in G.nodes:

        G.add_edge(a, b)


# Add transaction relationships
for _, row in transactions.iterrows():

    a = str(row["Sender"])
    b = str(row["Receiver"])

    if a in G.nodes and b in G.nodes:

        G.add_edge(a, b)


if person_id and person_id in G.nodes:

    neighbors = list(
        G.neighbors(person_id)
    )

    if neighbors:

        connection_data = []

        for neighbor in neighbors:

            name_match = persons[
                persons["Person_ID"].astype(str) == neighbor
            ]

            if len(name_match) > 0:

                name = name_match.iloc[0]["Name"]

            else:

                name = neighbor

            connection_data.append(
                {
                    "Person_ID": neighbor,
                    "Name": name,
                    "Connection_Count": G.degree(neighbor)
                }
            )

        connections_df = pd.DataFrame(
            connection_data
        )

        st.dataframe(
            connections_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No network connections found."
        )

else:

    st.info(
        "No network connections found."
    )


# ============================================================
# INVESTIGATION SUMMARY
# ============================================================

st.divider()

st.header(
    "🧠 Investigation Summary"
)


summary_points = []


if len(person_calls) > 0:

    summary_points.append(
        f"📞 {len(person_calls)} communication records "
        "are associated with this entity."
    )


if len(person_transactions) > 0:

    summary_points.append(
        f"💰 {len(person_transactions)} financial records "
        "are associated with this entity."
    )


if person_id and person_id in G.nodes:

    summary_points.append(
        f"🕸️ The entity has "
        f"{G.degree(person_id)} direct network connection(s)."
    )


if len(person_vehicles) > 0:

    summary_points.append(
        f"🚗 {len(person_vehicles)} vehicle record(s) "
        "are associated with this entity."
    )


if len(person_locations) > 0:

    summary_points.append(
        f"📍 {len(person_locations)} location record(s) "
        "are associated with this entity."
    )


if summary_points:

    for point in summary_points:

        st.write(
            "• " + point
        )

else:

    st.info(
        "Insufficient linked information for an automated summary."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CrimeGraph AI | SIH 26189"
)

st.caption(
    "Investigation support only — human verification required."
)

