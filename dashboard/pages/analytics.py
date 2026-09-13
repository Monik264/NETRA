# ============================================================
# CRIMEGRAPH AI - ANALYTICS PAGE
# ============================================================

import streamlit as st
import pandas as pd
import networkx as nx
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CrimeGraph AI - Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# DATA PATH
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

@st.cache_data
def load_data():

    persons_path = os.path.join(
        DATA_DIR,
        "persons.csv"
    )

    calls_path = os.path.join(
        DATA_DIR,
        "calls.csv"
    )

    transactions_path = os.path.join(
        DATA_DIR,
        "transactions.csv"
    )

    cases_path = os.path.join(
        DATA_DIR,
        "cases.csv"
    )

    persons = pd.read_csv(persons_path)
    calls = pd.read_csv(calls_path)
    transactions = pd.read_csv(transactions_path)
    cases = pd.read_csv(cases_path)

    return (
        persons,
        calls,
        transactions,
        cases
    )


# ============================================================
# TRY LOADING DATA
# ============================================================

try:

    persons, calls, transactions, cases = load_data()

except Exception as e:

    st.error(
        "Unable to load data files."
    )

    st.code(
        str(e)
    )

    st.info(
        "Make sure the CSV files are inside the SIH_FINAL/data folder."
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("📊 Network Analytics")

st.markdown(
    """
    ### Criminal Network Intelligence

    This module analyses the relationship network and calculates
    multiple graph-based indicators to help investigators understand
    important entities and communication patterns.

    **Note:** These indicators are analytical aids and should not be
    treated as proof of criminal activity.
    """
)


st.divider()


# ============================================================
# CREATE NETWORK
# ============================================================

G = nx.Graph()


# ============================================================
# ADD PERSON NODES
# ============================================================

for _, row in persons.iterrows():

    person_id = str(row["Person_ID"])

    name = str(
        row.get(
            "Name",
            person_id
        )
    )

    G.add_node(
        person_id,
        name=name,
        entity_type="PERSON"
    )


# ============================================================
# ADD CALL RELATIONSHIPS
# ============================================================

for _, row in calls.iterrows():

    caller = str(row["Caller"])
    receiver = str(row["Receiver"])

    if (
        caller in G.nodes
        and
        receiver in G.nodes
    ):

        if G.has_edge(
            caller,
            receiver
        ):

            G[caller][receiver]["weight"] += 1
            G[caller][receiver]["communications"] += 1

        else:

            G.add_edge(
                caller,
                receiver,
                weight=1,
                communications=1
            )


# ============================================================
# ADD TRANSACTION RELATIONSHIPS
# ============================================================

for _, row in transactions.iterrows():

    sender = str(row["Sender"])
    receiver = str(row["Receiver"])

    if (
        sender in G.nodes
        and
        receiver in G.nodes
    ):

        amount = 0

        try:
            amount = float(row["Amount"])
        except:
            amount = 0

        if G.has_edge(
            sender,
            receiver
        ):

            G[sender][receiver]["weight"] += 1

            G[sender][receiver][
                "transaction_amount"
            ] = (
                G[sender][receiver]
                .get("transaction_amount", 0)
                + amount
            )

        else:

            G.add_edge(
                sender,
                receiver,
                weight=1,
                transaction_amount=amount
            )


# ============================================================
# BASIC NETWORK INFORMATION
# ============================================================

number_of_nodes = G.number_of_nodes()

number_of_edges = G.number_of_edges()

density = nx.density(G)

components = nx.number_connected_components(G)


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👤 Entities",
        number_of_nodes
    )


with col2:

    st.metric(
        "🔗 Relationships",
        number_of_edges
    )


with col3:

    st.metric(
        "🌐 Network Density",
        round(
            density,
            3
        )
    )


with col4:

    st.metric(
        "🧩 Network Groups",
        components
    )


st.divider()


# ============================================================
# CENTRALITY CALCULATIONS
# ============================================================

st.subheader(
    "🎯 Entity Importance Analysis"
)


# Degree centrality

degree_centrality = nx.degree_centrality(
    G
)


# Betweenness centrality

betweenness_centrality = nx.betweenness_centrality(
    G
)


# Closeness centrality

if number_of_nodes > 1:

    closeness_centrality = nx.closeness_centrality(
        G
    )

else:

    closeness_centrality = {
        node: 0
        for node in G.nodes
    }


# PageRank

if number_of_nodes > 0:

    pagerank = nx.pagerank(
        G
    )

else:

    pagerank = {}


# ============================================================
# BUILD ANALYTICS TABLE
# ============================================================

analytics_data = []


for node in G.nodes:

    name = G.nodes[node].get(
        "name",
        node
    )

    connections = G.degree(
        node
    )

    analytics_data.append(
        {
            "Person ID": node,

            "Name": name,

            "Connections": connections,

            "Degree Centrality": round(
                degree_centrality.get(
                    node,
                    0
                ),
                4
            ),

            "Betweenness Centrality": round(
                betweenness_centrality.get(
                    node,
                    0
                ),
                4
            ),

            "Closeness Centrality": round(
                closeness_centrality.get(
                    node,
                    0
                ),
                4
            ),

            "PageRank": round(
                pagerank.get(
                    node,
                    0
                ),
                4
            )
        }
    )


analytics_df = pd.DataFrame(
    analytics_data
)


# ============================================================
# SORT BY IMPORTANCE
# ============================================================

analytics_df = analytics_df.sort_values(
    by="Degree Centrality",
    ascending=False
)


# ============================================================
# DISPLAY TABLE
# ============================================================

st.dataframe(
    analytics_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# TOP CONNECTED ENTITIES
# ============================================================

st.subheader(
    "🔥 Most Connected Entities"
)


top_connections = analytics_df.sort_values(
    by="Connections",
    ascending=False
).head(10)


st.dataframe(
    top_connections[
        [
            "Person ID",
            "Name",
            "Connections"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# TOP BETWEENNESS ENTITIES
# ============================================================

st.subheader(
    "🌉 Network Bridge Entities"
)


st.write(
    """
    High betweenness centrality means an entity frequently lies
    on paths connecting different parts of the network.
    """
)


top_betweenness = analytics_df.sort_values(
    by="Betweenness Centrality",
    ascending=False
).head(10)


st.dataframe(
    top_betweenness[
        [
            "Person ID",
            "Name",
            "Connections",
            "Betweenness Centrality"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# TOP PAGERANK
# ============================================================

st.subheader(
    "⭐ High Influence Entities"
)


st.write(
    """
    PageRank estimates the relative structural importance of
    entities based on their relationships with other entities.
    """
)


top_pagerank = analytics_df.sort_values(
    by="PageRank",
    ascending=False
).head(10)


st.dataframe(
    top_pagerank[
        [
            "Person ID",
            "Name",
            "PageRank"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# COMMUNICATION ANALYSIS
# ============================================================

st.subheader(
    "📞 Communication Analytics"
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
            name="Number of Calls"
        )
        .sort_values(
            by="Number of Calls",
            ascending=False
        )
    )

    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Total Calls",
            len(calls)
        )


    with col2:

        st.metric(
            "Unique Communication Links",
            len(call_counts)
        )


    st.write(
        "### Most Frequent Communication Links"
    )

    st.dataframe(
        call_counts.head(15),
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No call records available."
    )


st.divider()


# ============================================================
# FINANCIAL ANALYSIS
# ============================================================

st.subheader(
    "💰 Transaction Analytics"
)


if len(transactions) > 0:

    total_transaction_value = (
        pd.to_numeric(
            transactions["Amount"],
            errors="coerce"
        )
        .fillna(0)
        .sum()
    )


    average_transaction = (
        pd.to_numeric(
            transactions["Amount"],
            errors="coerce"
        )
        .fillna(0)
        .mean()
    )


    largest_transaction = (
        pd.to_numeric(
            transactions["Amount"],
            errors="coerce"
        )
        .fillna(0)
        .max()
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "💵 Total Transaction Value",
            f"₹{total_transaction_value:,.2f}"
        )


    with col2:

        st.metric(
            "📈 Average Transaction",
            f"₹{average_transaction:,.2f}"
        )


    with col3:

        st.metric(
            "🚨 Largest Transaction",
            f"₹{largest_transaction:,.2f}"
        )


    transaction_summary = (
        transactions
        .groupby(
            [
                "Sender",
                "Receiver"
            ]
        )["Amount"]
        .agg(
            [
                "count",
                "sum"
            ]
        )
        .reset_index()
    )


    transaction_summary = (
        transaction_summary
        .rename(
            columns={
                "count": "Transaction Count",
                "sum": "Total Amount"
            }
        )
        .sort_values(
            by="Total Amount",
            ascending=False
        )
    )


    st.write(
        "### Highest Transaction Relationships"
    )


    st.dataframe(
        transaction_summary.head(15),
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No transaction records available."
    )


st.divider()


# ============================================================
# NETWORK COMPONENT ANALYSIS
# ============================================================

st.subheader(
    "🧩 Connected Network Groups"
)


connected_components = list(
    nx.connected_components(G)
)


component_data = []


for index, component in enumerate(
    connected_components,
    start=1
):

    component_data.append(
        {
            "Network Group": f"Group {index}",

            "Number of Entities": len(
                component
            ),

            "Entities": ", ".join(
                sorted(component)
            )
        }
    )


component_df = pd.DataFrame(
    component_data
)


st.dataframe(
    component_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# INVESTIGATIVE PRIORITY SCORE
# ============================================================

st.subheader(
    "🚨 Investigative Priority Indicators"
)


st.write(
    """
    This is a prototype ranking mechanism combining multiple
    network indicators. It is intended only to prioritize data
    for human review and does not determine guilt or criminality.
    """
)


priority_df = analytics_df.copy()


# Normalize values

def normalize(series):

    maximum = series.max()

    minimum = series.min()

    if maximum == minimum:

        return pd.Series(
            [0] * len(series),
            index=series.index
        )

    return (
        (series - minimum)
        /
        (maximum - minimum)
    )


priority_df[
    "Degree Score"
] = normalize(
    priority_df[
        "Degree Centrality"
    ]
)


priority_df[
    "Betweenness Score"
] = normalize(
    priority_df[
        "Betweenness Centrality"
    ]
)


priority_df[
    "PageRank Score"
] = normalize(
    priority_df[
        "PageRank"
    ]
)


# Combined score

priority_df[
    "Priority Score"
] = (
    priority_df["Degree Score"] * 0.35
    +
    priority_df["Betweenness Score"] * 0.35
    +
    priority_df["PageRank Score"] * 0.30
)


priority_df[
    "Priority Score"
] = priority_df[
    "Priority Score"
].round(4)


priority_df = priority_df.sort_values(
    by="Priority Score",
    ascending=False
)


# ============================================================
# DISPLAY PRIORITY TABLE
# ============================================================

st.dataframe(
    priority_df[
        [
            "Person ID",
            "Name",
            "Connections",
            "Degree Centrality",
            "Betweenness Centrality",
            "PageRank",
            "Priority Score"
        ]
    ].head(20),
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# SELECT ENTITY
# ============================================================

st.subheader(
    "🔎 Inspect Individual Entity"
)


entity_options = analytics_df[
    "Person ID"
].tolist()


if len(entity_options) > 0:

    selected_entity = st.selectbox(
        "Select an entity",
        entity_options
    )


    selected_row = analytics_df[
        analytics_df["Person ID"]
        ==
        selected_entity
    ].iloc[0]


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Connections",
            int(
                selected_row[
                    "Connections"
                ]
            )
        )


    with col2:

        st.metric(
            "Degree",
            selected_row[
                "Degree Centrality"
            ]
        )


    with col3:

        st.metric(
            "Betweenness",
            selected_row[
                "Betweenness Centrality"
            ]
        )


    with col4:

        st.metric(
            "PageRank",
            selected_row[
                "PageRank"
            ]
        )


    # --------------------------------------------------------
    # NEIGHBORS
    # --------------------------------------------------------

    st.write(
        "### Direct Network Connections"
    )


    neighbors = list(
        G.neighbors(
            selected_entity
        )
    )


    neighbor_data = []


    for neighbor in neighbors:

        neighbor_name = G.nodes[
            neighbor
        ].get(
            "name",
            neighbor
        )


        neighbor_data.append(
            {
                "Person ID": neighbor,
                "Name": neighbor_name
            }
        )


    if len(neighbor_data) > 0:

        st.dataframe(
            pd.DataFrame(
                neighbor_data
            ),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No direct network connections found."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CrimeGraph AI | SIH 26189 Prototype"
)

st.caption(
    "Analytics are decision-support indicators. "
    "Human verification is required."
)