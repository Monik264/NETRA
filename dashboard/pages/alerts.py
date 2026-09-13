import streamlit as st
import pandas as pd
from pathlib import Path
from itertools import combinations


# ============================================================
# DATA FOLDER
# ============================================================

def get_data_folder():

    current_file = Path(__file__).resolve()

    possible_paths = [
        current_file.parents[2] / "data",
        current_file.parents[1] / "data",
        Path.cwd() / "data",
        Path.cwd().parent / "data"
    ]

    for path in possible_paths:
        if path.exists() and path.is_dir():
            return path

    return None


# ============================================================
# SAFE CSV READER
# ============================================================

def read_csv(path):

    if not path.exists():
        return pd.DataFrame()

    try:
        if path.stat().st_size == 0:
            return pd.DataFrame()

        return pd.read_csv(
            path,
            dtype=str,
            encoding="utf-8-sig"
        ).fillna("")

    except Exception:
        return pd.DataFrame()


# ============================================================
# FIND COLUMN
# ============================================================

def find_column(df, names):

    if df.empty:
        return None

    normalized = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for name in names:

        key = name.strip().lower()

        if key in normalized:
            return normalized[key]

    return None


# ============================================================
# MAIN PAGE FUNCTION
# ============================================================

def show():

    # ========================================================
    # LOAD DATA
    # ========================================================

    data_folder = get_data_folder()

    if data_folder is None:

        st.error("❌ Data folder not found.")

        st.info(
            "Make sure the data folder exists inside SIH_FINAL."
        )

        return

    persons = read_csv(
        data_folder / "persons.csv"
    )

    calls = read_csv(
        data_folder / "calls.csv"
    )

    transactions = read_csv(
        data_folder / "transactions.csv"
    )

    cases = read_csv(
        data_folder / "cases.csv"
    )

    phones = read_csv(
        data_folder / "phones.csv"
    )

    vehicles = read_csv(
        data_folder / "vehicles.csv"
    )

    locations = read_csv(
        data_folder / "locations.csv"
    )

    # ========================================================
    # TITLE
    # ========================================================

    st.title("🚨 Alerts & Anomaly Detection")

    st.markdown(
        "### Automated Investigation Alerts"
    )

    st.write(
        "This module examines communication, financial and "
        "network patterns and highlights records that may "
        "deserve additional human review."
    )

    st.info(
        "Important: An alert is only an indicator. "
        "It does not establish criminal activity or guilt."
    )

    # ========================================================
    # DATA STATUS
    # ========================================================

    with st.expander("📂 Data Status"):

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Persons", len(persons))

        with c2:
            st.metric("Calls", len(calls))

        with c3:
            st.metric("Transactions", len(transactions))

        with c4:
            st.metric("Cases", len(cases))

    # ========================================================
    # TOTAL ALERTS
    # ========================================================

    total_alerts = 0

    # ========================================================
    # 1. REPEATED COMMUNICATION
    # ========================================================

    st.markdown("### 📞 1. Repeated Communication")

    st.caption(
        "Detects person-to-person communication links "
        "that occur repeatedly."
    )

    if calls.empty:

        st.warning("No call data available.")

    else:

        caller_col = find_column(
            calls,
            [
                "caller",
                "caller_id",
                "source",
                "from",
                "sender"
            ]
        )

        receiver_col = find_column(
            calls,
            [
                "receiver",
                "receiver_id",
                "target",
                "to",
                "recipient"
            ]
        )

        if caller_col and receiver_col:

            repeated_calls = (
                calls
                .groupby(
                    [caller_col, receiver_col]
                )
                .size()
                .reset_index(
                    name="Number of Calls"
                )
            )

            repeated_calls = repeated_calls[
                repeated_calls["Number of Calls"] >= 2
            ]

            if not repeated_calls.empty:

                total_alerts += len(
                    repeated_calls
                )

                st.warning(
                    f"🚨 {len(repeated_calls)} repeated "
                    "communication relationship(s) detected."
                )

                st.dataframe(
                    repeated_calls.sort_values(
                        "Number of Calls",
                        ascending=False
                    ),
                    width="stretch",
                    hide_index=True
                )

            else:

                st.success(
                    "No repeated communication pattern detected."
                )

        else:

            st.error(
                "Caller/Receiver columns not found."
            )

    # ========================================================
    # 2. HIGH-VALUE TRANSACTIONS
    # ========================================================

    st.markdown(
        "### 💰 2. High-Value Transactions"
    )

    st.caption(
        "Flags transactions of ₹50,000 or more "
        "for additional review."
    )

    if transactions.empty:

        st.warning(
            "No transaction data available."
        )

    else:

        amount_col = find_column(
            transactions,
            [
                "amount",
                "transaction_amount",
                "value"
            ]
        )

        sender_col = find_column(
            transactions,
            [
                "sender",
                "sender_id",
                "source",
                "from"
            ]
        )

        receiver_col = find_column(
            transactions,
            [
                "receiver",
                "receiver_id",
                "target",
                "to"
            ]
        )

        transaction_id_col = find_column(
            transactions,
            [
                "transaction_id",
                "id"
            ]
        )

        if amount_col:

            transactions[amount_col] = pd.to_numeric(
                transactions[amount_col],
                errors="coerce"
            )

            transactions = transactions.dropna(
                subset=[amount_col]
            )

            threshold = 50000

            if not transactions.empty:

                average_transaction = (
                    transactions[amount_col].mean()
                )

                high_value = transactions[
                    transactions[amount_col] >= threshold
                ].copy()

                c1, c2, c3 = st.columns(3)

                with c1:

                    st.metric(
                        "Average Transaction",
                        f"₹{average_transaction:,.2f}"
                    )

                with c2:

                    st.metric(
                        "Alert Threshold",
                        f"₹{threshold:,.2f}"
                    )

                with c3:

                    st.metric(
                        "High-Value Alerts",
                        len(high_value)
                    )

                if not high_value.empty:

                    total_alerts += len(
                        high_value
                    )

                    st.warning(
                        f"🚨 {len(high_value)} high-value "
                        "transaction(s) detected."
                    )

                    display_columns = []

                    for col in [
                        transaction_id_col,
                        sender_col,
                        receiver_col,
                        amount_col,
                        "Date",
                        "date",
                        "Type",
                        "type"
                    ]:

                        if (
                            col
                            and col in high_value.columns
                            and col not in display_columns
                        ):

                            display_columns.append(col)

                    if display_columns:

                        st.dataframe(
                            high_value[
                                display_columns
                            ],
                            width="stretch",
                            hide_index=True
                        )

                    else:

                        st.dataframe(
                            high_value,
                            width="stretch",
                            hide_index=True
                        )

                else:

                    st.success(
                        "No high-value transaction detected."
                    )

            else:

                st.warning(
                    "No valid numeric transaction amounts found."
                )

        else:

            st.error(
                "Amount column not found."
            )

    # ========================================================
    # 3. HIGHLY CONNECTED ENTITIES
    # ========================================================

    st.markdown(
        "### 🕸️ 3. Highly Connected Entities"
    )

    st.caption(
        "Identifies people with unusually high numbers "
        "of direct network connections."
    )

    connection_counts = {}

    def add_person_connection(a, b):

        if not a or not b:
            return

        a = str(a).strip()
        b = str(b).strip()

        if not a or not b or a == b:
            return

        connection_counts.setdefault(
            a,
            set()
        )

        connection_counts.setdefault(
            b,
            set()
        )

        connection_counts[a].add(b)
        connection_counts[b].add(a)

    # ========================================================
    # CALL CONNECTIONS
    # ========================================================

    if not calls.empty:

        caller_col = find_column(
            calls,
            [
                "caller",
                "caller_id",
                "source",
                "from"
            ]
        )

        receiver_col = find_column(
            calls,
            [
                "receiver",
                "receiver_id",
                "target",
                "to"
            ]
        )

        if caller_col and receiver_col:

            for _, row in calls.iterrows():

                add_person_connection(
                    row[caller_col],
                    row[receiver_col]
                )

    # ========================================================
    # TRANSACTION CONNECTIONS
    # ========================================================

    if not transactions.empty:

        sender_col = find_column(
            transactions,
            [
                "sender",
                "sender_id",
                "source",
                "from"
            ]
        )

        receiver_col = find_column(
            transactions,
            [
                "receiver",
                "receiver_id",
                "target",
                "to"
            ]
        )

        if sender_col and receiver_col:

            for _, row in transactions.iterrows():

                add_person_connection(
                    row[sender_col],
                    row[receiver_col]
                )

    if connection_counts:

        connected_entities = []

        for person, connections in connection_counts.items():

            connected_entities.append(
                {
                    "Person": person,
                    "Direct Connections": len(
                        connections
                    )
                }
            )

        connected_df = pd.DataFrame(
            connected_entities
        )

        connected_df = connected_df.sort_values(
            "Direct Connections",
            ascending=False
        )

        top_connected = connected_df.head(5)

        if not top_connected.empty:

            total_alerts += len(
                top_connected
            )

            st.warning(
                "🔥 Most connected entities:"
            )

            st.dataframe(
                top_connected,
                width="stretch",
                hide_index=True
            )

    else:

        st.info(
            "No network connections available."
        )

    # ========================================================
    # 4. REPEATED FINANCIAL RELATIONSHIPS
    # ========================================================

    st.markdown(
        "### 🔄 4. Repeated Financial Relationships"
    )

    st.caption(
        "Detects repeated money transfers between "
        "the same sender and receiver."
    )

    if transactions.empty:

        st.warning(
            "No transaction data available."
        )

    else:

        sender_col = find_column(
            transactions,
            [
                "sender",
                "sender_id",
                "source",
                "from"
            ]
        )

        receiver_col = find_column(
            transactions,
            [
                "receiver",
                "receiver_id",
                "target",
                "to"
            ]
        )

        if sender_col and receiver_col:

            repeated_financial = (
                transactions
                .groupby(
                    [
                        sender_col,
                        receiver_col
                    ]
                )
                .size()
                .reset_index(
                    name="Transaction Count"
                )
            )

            repeated_financial = (
                repeated_financial[
                    repeated_financial[
                        "Transaction Count"
                    ] >= 2
                ]
            )

            if not repeated_financial.empty:

                total_alerts += len(
                    repeated_financial
                )

                st.warning(
                    f"🚨 {len(repeated_financial)} "
                    "repeated financial relationship(s) detected."
                )

                st.dataframe(
                    repeated_financial.sort_values(
                        "Transaction Count",
                        ascending=False
                    ),
                    width="stretch",
                    hide_index=True
                )

            else:

                st.success(
                    "No repeated financial relationships detected."
                )

        else:

            st.error(
                "Sender/Receiver columns not found."
            )

    # ========================================================
    # 5. COMMUNICATION + FINANCIAL
    # ========================================================

    st.markdown(
        "### 📞💰 5. Communication + Financial Relationship"
    )

    st.caption(
        "Finds pairs of entities that both communicate "
        "and have financial interactions."
    )

    communication_pairs = set()
    financial_pairs = set()

    # ========================================================
    # COMMUNICATION PAIRS
    # ========================================================

    if not calls.empty:

        caller_col = find_column(
            calls,
            [
                "caller",
                "caller_id",
                "source",
                "from"
            ]
        )

        receiver_col = find_column(
            calls,
            [
                "receiver",
                "receiver_id",
                "target",
                "to"
            ]
        )

        if caller_col and receiver_col:

            for _, row in calls.iterrows():

                a = str(
                    row[caller_col]
                ).strip()

                b = str(
                    row[receiver_col]
                ).strip()

                if a and b and a != b:

                    communication_pairs.add(
                        tuple(
                            sorted(
                                [a, b]
                            )
                        )
                    )

    # ========================================================
    # FINANCIAL PAIRS
    # ========================================================

    if not transactions.empty:

        sender_col = find_column(
            transactions,
            [
                "sender",
                "sender_id",
                "source",
                "from"
            ]
        )

        receiver_col = find_column(
            transactions,
            [
                "receiver",
                "receiver_id",
                "target",
                "to"
            ]
        )

        if sender_col and receiver_col:

            for _, row in transactions.iterrows():

                a = str(
                    row[sender_col]
                ).strip()

                b = str(
                    row[receiver_col]
                ).strip()

                if a and b and a != b:

                    financial_pairs.add(
                        tuple(
                            sorted(
                                [a, b]
                            )
                        )
                    )

    # ========================================================
    # COMBINED PAIRS
    # ========================================================

    combined_pairs = (
        communication_pairs
        & financial_pairs
    )

    if combined_pairs:

        total_alerts += len(
            combined_pairs
        )

        combined_data = []

        for a, b in sorted(
            combined_pairs
        ):

            combined_data.append(
                {
                    "Person 1": a,
                    "Person 2": b,
                    "Communication": "Yes",
                    "Financial Relationship": "Yes"
                }
            )

        combined_df = pd.DataFrame(
            combined_data
        )

        st.warning(
            f"🚨 {len(combined_df)} entity pair(s) "
            "show both communication and financial relationships."
        )

        st.dataframe(
            combined_df,
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            "No communication + financial relationships detected."
        )

    # ========================================================
    # 6. REPEATED NETWORK CONNECTIONS
    # ========================================================

    st.markdown(
        "### 🔗 6. Repeated Network Connections"
    )

    st.caption(
        "Detects people connected repeatedly through "
        "calls, transactions, phones, vehicles or locations."
    )

    network_connections = {}

    def record_network_connection(
        a,
        b,
        relationship
    ):

        if not a or not b:
            return

        a = str(a).strip()
        b = str(b).strip()

        if not a or not b or a == b:
            return

        pair = tuple(
            sorted(
                [a, b]
            )
        )

        if pair not in network_connections:

            network_connections[pair] = {
                "Person 1": pair[0],
                "Person 2": pair[1],
                "Calls": 0,
                "Transactions": 0,
                "Shared Phones": 0,
                "Shared Vehicles": 0,
                "Shared Locations": 0
            }

        network_connections[
            pair
        ][relationship] += 1

    # ========================================================
    # CALLS
    # ========================================================

    if not calls.empty:

        caller_col = find_column(
            calls,
            [
                "caller",
                "caller_id",
                "source",
                "from"
            ]
        )

        receiver_col = find_column(
            calls,
            [
                "receiver",
                "receiver_id",
                "target",
                "to"
            ]
        )

        if caller_col and receiver_col:

            for _, row in calls.iterrows():

                record_network_connection(
                    row[caller_col],
                    row[receiver_col],
                    "Calls"
                )

    # ========================================================
    # TRANSACTIONS
    # ========================================================

    if not transactions.empty:

        sender_col = find_column(
            transactions,
            [
                "sender",
                "sender_id",
                "source",
                "from"
            ]
        )

        receiver_col = find_column(
            transactions,
            [
                "receiver",
                "receiver_id",
                "target",
                "to"
            ]
        )

        if sender_col and receiver_col:

            for _, row in transactions.iterrows():

                record_network_connection(
                    row[sender_col],
                    row[receiver_col],
                    "Transactions"
                )

    # ========================================================
    # SHARED PHONES
    # ========================================================

    if not phones.empty:

        phone_person = find_column(
            phones,
            [
                "person_id",
                "owner_id"
            ]
        )

        phone_number = find_column(
            phones,
            [
                "phone_number",
                "phone",
                "number",
                "mobile"
            ]
        )

        if phone_person and phone_number:

            for _, group in phones.groupby(
                phone_number
            ):

                people = list(
                    dict.fromkeys(
                        str(x).strip()
                        for x in group[phone_person]
                        if str(x).strip()
                    )
                )

                for a, b in combinations(
                    people,
                    2
                ):

                    record_network_connection(
                        a,
                        b,
                        "Shared Phones"
                    )

    # ========================================================
    # SHARED VEHICLES
    # ========================================================

    if not vehicles.empty:

        vehicle_person = find_column(
            vehicles,
            [
                "owner_id",
                "person_id"
            ]
        )

        vehicle_id = find_column(
            vehicles,
            [
                "vehicle_id",
                "vehicle"
            ]
        )

        if vehicle_person and vehicle_id:

            for _, group in vehicles.groupby(
                vehicle_id
            ):

                people = list(
                    dict.fromkeys(
                        str(x).strip()
                        for x in group[vehicle_person]
                        if str(x).strip()
                    )
                )

                for a, b in combinations(
                    people,
                    2
                ):

                    record_network_connection(
                        a,
                        b,
                        "Shared Vehicles"
                    )

    # ========================================================
    # SHARED LOCATIONS
    # ========================================================

    if not locations.empty:

        location_person = find_column(
            locations,
            [
                "person_id",
                "owner_id",
                "resident_id"
            ]
        )

        location_id = find_column(
            locations,
            [
                "location_id",
                "location"
            ]
        )

        if location_person and location_id:

            for _, group in locations.groupby(
                location_id
            ):

                people = list(
                    dict.fromkeys(
                        str(x).strip()
                        for x in group[location_person]
                        if str(x).strip()
                    )
                )

                for a, b in combinations(
                    people,
                    2
                ):

                    record_network_connection(
                        a,
                        b,
                        "Shared Locations"
                    )

    # ========================================================
    # DISPLAY REPEATED NETWORK CONNECTIONS
    # ========================================================

    if network_connections:

        repeated_network = []

        for pair, data in network_connections.items():

            total_connections = (
                data["Calls"]
                + data["Transactions"]
                + data["Shared Phones"]
                + data["Shared Vehicles"]
                + data["Shared Locations"]
            )

            connection_types = sum(
                1
                for key in [
                    "Calls",
                    "Transactions",
                    "Shared Phones",
                    "Shared Vehicles",
                    "Shared Locations"
                ]
                if data[key] > 0
            )

            if (
                total_connections >= 2
                or connection_types >= 2
            ):

                result = data.copy()

                result["Total Connections"] = (
                    total_connections
                )

                result["Connection Types"] = (
                    connection_types
                )

                repeated_network.append(
                    result
                )

        if repeated_network:

            repeated_network_df = pd.DataFrame(
                repeated_network
            )

            repeated_network_df = (
                repeated_network_df.sort_values(
                    "Total Connections",
                    ascending=False
                )
            )

            total_alerts += len(
                repeated_network_df
            )

            st.warning(
                f"🚨 {len(repeated_network_df)} repeated "
                "network connection(s) detected."
            )

            st.dataframe(
                repeated_network_df,
                width="stretch",
                hide_index=True
            )

        else:

            st.success(
                "No repeated network connections detected."
            )

    else:

        st.info(
            "No network relationships available."
        )

    # ========================================================
    # ALERT SUMMARY
    # ========================================================

    st.markdown("---")

    st.markdown(
        "### 📊 Alert Summary"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Alert Indicators",
            total_alerts
        )

    with col2:

        st.metric(
            "Data Records",
            (
                len(persons)
                + len(calls)
                + len(transactions)
                + len(cases)
            )
        )

    st.caption(
        "These indicators are intended to support investigation "
        "and should be reviewed by authorized personnel."
    )


# ============================================================
# DIRECT STREAMLIT EXECUTION
# ============================================================

if __name__ == "__main__":
    show()