# ============================================================
# CRIMEGRAPH AI
# ALERTS & ANOMALY DETECTION
# ============================================================

import streamlit as st
import pandas as pd
import networkx as nx
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CrimeGraph AI - Alerts",
    page_icon="🚨",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    persons = pd.read_csv(
        os.path.join(
            DATA_DIR,
            "persons.csv"
        )
    )

    calls = pd.read_csv(
        os.path.join(
            DATA_DIR,
            "calls.csv"
        )
    )

    transactions = pd.read_csv(
        os.path.join(
            DATA_DIR,
            "transactions.csv"
        )
    )

    cases = pd.read_csv(
        os.path.join(
            DATA_DIR,
            "cases.csv"
        )
    )

    return (
        persons,
        calls,
        transactions,
        cases
    )


# ============================================================
# LOAD DATA SAFELY
# ============================================================

try:

    persons, calls, transactions, cases = load_data()

except Exception as e:

    st.error(
        "Unable to load data."
    )

    st.code(
        str(e)
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title(
    "🚨 Alerts & Anomaly Detection"
)

st.markdown(
    """
    ### Automated Investigation Alerts

    This module examines communication, financial and network
    patterns and highlights records that may deserve additional
    human review.

    **Important:** An alert is only an indicator. It does not
    establish criminal activity or guilt.
    """
)

st.divider()


# ============================================================
# CREATE NETWORK
# ============================================================

G = nx.Graph()


# ============================================================
# ADD PERSONS
# ============================================================

for _, row in persons.iterrows():

    person_id = str(
        row["Person_ID"]
    )

    name = str(
        row.get(
            "Name",
            person_id
        )
    )

    G.add_node(
        person_id,
        name=name
    )


# ============================================================
# ADD CALL CONNECTIONS
# ============================================================

for _, row in calls.iterrows():

    caller = str(
        row["Caller"]
    )

    receiver = str(
        row["Receiver"]
    )

    if (
        caller in G.nodes
        and
        receiver in G.nodes
    ):

        if G.has_edge(
            caller,
            receiver
        ):

            G[caller][receiver][
                "calls"
            ] += 1

        else:

            G.add_edge(
                caller,
                receiver,
                calls=1,
                transactions=0,
                amount=0
            )


# ============================================================
# ADD TRANSACTION CONNECTIONS
# ============================================================

for _, row in transactions.iterrows():

    sender = str(
        row["Sender"]
    )

    receiver = str(
        row["Receiver"]
    )

    try:

        amount = float(
            row["Amount"]
        )

    except:

        amount = 0


    if (
        sender in G.nodes
        and
        receiver in G.nodes
    ):

        if G.has_edge(
            sender,
            receiver
        ):

            G[sender][receiver][
                "transactions"
            ] += 1

            G[sender][receiver][
                "amount"
            ] += amount

        else:

            G.add_edge(
                sender,
                receiver,
                calls=0,
                transactions=1,
                amount=amount
            )


# ============================================================
# ALERT COUNTERS
# ============================================================

repeated_call_alerts = 0

financial_alerts = 0

high_connection_alerts = 0

rapid_transaction_alerts = 0

total_alerts = 0


# ============================================================
# ALERT 1
# REPEATED COMMUNICATION
# ============================================================

st.subheader(
    "📞 1. Repeated Communication"
)

st.write(
    """
    Detects person-to-person communication links that occur
    repeatedly.
    """
)


if len(calls) > 0:

    call_counts = (
        calls
        .groupby(
            [
                "Caller",
                "Receiver"
            ]
        )
        .size()
        .reset_index(
            name="Call Count"
        )
        .sort_values(
            by="Call Count",
            ascending=False
        )
    )

    repeated_calls = call_counts[
        call_counts["Call Count"] >= 3
    ]


    repeated_call_alerts = len(
        repeated_calls
    )


    if repeated_call_alerts > 0:

        st.warning(
            f"{repeated_call_alerts} repeated communication "
            "pattern(s) detected."
        )

        st.dataframe(
            repeated_calls,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No repeated communication pattern detected."
        )

else:

    st.info(
        "No call data available."
    )


st.divider()


# ============================================================
# ALERT 2
# HIGH VALUE TRANSACTIONS
# ============================================================

st.subheader(
    "💰 2. High-Value Transactions"
)

st.write(
    """
    Flags transactions significantly higher than the average
    transaction value in the dataset.
    """
)


if len(transactions) > 0:

    transaction_amounts = pd.to_numeric(
        transactions["Amount"],
        errors="coerce"
    ).fillna(0)


    average_amount = (
        transaction_amounts.mean()
    )

    threshold = (
        average_amount * 2
    )


    high_value_transactions = transactions[
        transaction_amounts >= threshold
    ].copy()


    financial_alerts = len(
        high_value_transactions
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Average Transaction",
            f"₹{average_amount:,.2f}"
        )


    with col2:

        st.metric(
            "Alert Threshold",
            f"₹{threshold:,.2f}"
        )


    if financial_alerts > 0:

        st.warning(
            f"{financial_alerts} high-value transaction(s) detected."
        )

        st.dataframe(
            high_value_transactions,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No high-value transaction detected."
        )

else:

    st.info(
        "No transaction data available."
    )


st.divider()


# ============================================================
# ALERT 3
# HIGHLY CONNECTED ENTITIES
# ============================================================

st.subheader(
    "🕸️ 3. Highly Connected Entities"
)

st.write(
    """
    Identifies entities with unusually high numbers of
    direct network connections.
    """
)


if G.number_of_nodes() > 0:

    degrees = dict(
        G.degree()
    )


    degree_df = pd.DataFrame(
        [
            {
                "Person ID": node,

                "Name": G.nodes[node].get(
                    "name",
                    node
                ),

                "Connections": degree
            }

            for node, degree
            in degrees.items()
        ]
    )


    if len(degree_df) > 0:

        average_degree = (
            degree_df["Connections"]
            .mean()
        )

        degree_threshold = max(
            3,
            average_degree * 2
        )


        highly_connected = degree_df[
            degree_df["Connections"]
            >= degree_threshold
        ].sort_values(
            by="Connections",
            ascending=False
        )


        high_connection_alerts = len(
            highly_connected
        )


        if high_connection_alerts > 0:

            st.warning(
                f"{high_connection_alerts} highly connected "
                "entity/entities detected."
            )

            st.dataframe(
                highly_connected,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "No unusually highly connected entities detected."
            )


st.divider()


# ============================================================
# ALERT 4
# MULTIPLE TRANSACTIONS BETWEEN SAME ENTITIES
# ============================================================

st.subheader(
    "🔄 4. Repeated Financial Relationships"
)

st.write(
    """
    Detects repeated money transfers between the same sender
    and receiver.
    """
)


if len(transactions) > 0:

    transaction_relationships = (
        transactions
        .groupby(
            [
                "Sender",
                "Receiver"
            ]
        )
        .agg(
            Transaction_Count=(
                "Amount",
                "count"
            ),

            Total_Amount=(
                "Amount",
                "sum"
            ),

            Average_Amount=(
                "Amount",
                "mean"
            )
        )
        .reset_index()
    )


    repeated_transactions = (
        transaction_relationships[
            transaction_relationships[
                "Transaction_Count"
            ] >= 3
        ]
        .sort_values(
            by="Transaction_Count",
            ascending=False
        )
    )


    rapid_transaction_alerts = len(
        repeated_transactions
    )


    if rapid_transaction_alerts > 0:

        st.warning(
            f"{rapid_transaction_alerts} repeated financial "
            "relationship(s) detected."
        )

        st.dataframe(
            repeated_transactions,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No repeated financial relationships detected."
        )


st.divider()


# ============================================================
# ALERT 5
# COMMUNICATION + TRANSACTION CONNECTION
# ============================================================

st.subheader(
    "📞💰 5. Communication + Financial Relationship"
)

st.write(
    """
    Finds pairs of entities that both communicate with each
    other and have financial interactions.
    """)


communication_pairs = set()


for _, row in calls.iterrows():

    a = str(
        row["Caller"]
    )

    b = str(
        row["Receiver"]
    )

    communication_pairs.add(
        tuple(
            sorted(
                [a, b]
            )
        )
    )


transaction_pairs = set()


for _, row in transactions.iterrows():

    a = str(
        row["Sender"]
    )

    b = str(
        row["Receiver"]
    )

    transaction_pairs.add(
        tuple(
            sorted(
                [a, b]
            )
        )
    )


overlapping_pairs = (
    communication_pairs
    &
    transaction_pairs
)


combined_relationships = []


for pair in overlapping_pairs:

    a, b = pair

    call_count = len(
        calls[
            (
                (
                    calls["Caller"].astype(str)
                    == a
                )
                &
                (
                    calls["Receiver"].astype(str)
                    == b
                )
            )
            |
            (
                (
                    calls["Caller"].astype(str)
                    == b
                )
                &
                (
                    calls["Receiver"].astype(str)
                    == a
                )
            )
        ]
    )


    pair_transactions = transactions[
        (
            (
                transactions["Sender"].astype(str)
                == a
            )
            &
            (
                transactions["Receiver"].astype(str)
                == b
            )
        )
        |
        (
            (
                transactions["Sender"].astype(str)
                == b
            )
            &
            (
                transactions["Receiver"].astype(str)
                == a
            )
        )
    ]


    total_amount = pd.to_numeric(
        pair_transactions["Amount"],
        errors="coerce"
    ).fillna(0).sum()


    combined_relationships.append(
        {
            "Entity A": a,

            "Entity B": b,

            "Calls": call_count,

            "Transactions": len(
                pair_transactions
            ),

            "Total Transaction Value":
                total_amount
        }
    )


combined_df = pd.DataFrame(
    combined_relationships
)


if len(combined_df) > 0:

    combined_df = combined_df.sort_values(
        by="Total Transaction Value",
        ascending=False
    )

    st.warning(
        f"{len(combined_df)} entity pair(s) show both "
        "communication and financial relationships."
    )

    st.dataframe(
        combined_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No overlapping communication and transaction "
        "relationships detected."
    )


st.divider()


# ============================================================
# OVERALL ALERT SUMMARY
# ============================================================

total_alerts = (
    repeated_call_alerts
    +
    financial_alerts
    +
    high_connection_alerts
    +
    rapid_transaction_alerts
)


st.subheader(
    "📋 Alert Summary"
)


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "🚨 Total",
        total_alerts
    )


with col2:

    st.metric(
        "📞 Communication",
        repeated_call_alerts
    )


with col3:

    st.metric(
        "💰 Financial",
        financial_alerts
    )


with col4:

    st.metric(
        "🕸️ Network",
        high_connection_alerts
    )


with col5:

    st.metric(
        "🔄 Repeated Transfers",
        rapid_transaction_alerts
    )


st.divider()


# ============================================================
# ALERT SEVERITY
# ============================================================

st.subheader(
    "⚠️ Alert Severity"
)


if total_alerts == 0:

    st.success(
        "No automated alerts were generated."
    )

elif total_alerts <= 3:

    st.info(
        "Low number of indicators detected. "
        "Review individual records."
    )

elif total_alerts <= 10:

    st.warning(
        "Multiple indicators detected. "
        "Prioritized human review is recommended."
    )

else:

    st.error(
        "A large number of indicators were detected. "
        "Detailed investigation and verification are recommended."
    )


# ============================================================
# INVESTIGATOR FILTER
# ============================================================

st.divider()

st.subheader(
    "🔎 Investigate Entity"
)


person_ids = persons[
    "Person_ID"
].astype(str).tolist()


if len(person_ids) > 0:

    selected_person = st.selectbox(
        "Select an entity",
        person_ids
    )


    selected_person_data = persons[
        persons["Person_ID"].astype(str)
        ==
        selected_person
    ]


    st.write(
        "### Entity Information"
    )


    st.dataframe(
        selected_person_data,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # PERSON CALLS
    # --------------------------------------------------------

    person_calls = calls[
        (
            calls["Caller"].astype(str)
            ==
            selected_person
        )
        |
        (
            calls["Receiver"].astype(str)
            ==
            selected_person
        )
    ]


    st.write(
        "### 📞 Communication Records"
    )


    if len(person_calls) > 0:

        st.dataframe(
            person_calls,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No communication records found."
        )


    # --------------------------------------------------------
    # PERSON TRANSACTIONS
    # --------------------------------------------------------

    person_transactions = transactions[
        (
            transactions["Sender"].astype(str)
            ==
            selected_person
        )
        |
        (
            transactions["Receiver"].astype(str)
            ==
            selected_person
        )
    ]


    st.write(
        "### 💰 Financial Records"
    )


    if len(person_transactions) > 0:

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
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CrimeGraph AI | SIH 26189 Prototype"
)

st.caption(
    "Automated alerts are investigative indicators only. "
    "Human verification is required."
)