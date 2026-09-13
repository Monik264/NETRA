# ============================================================
# CRIMEGRAPH AI - ANALYTICS PAGE
# ============================================================

import os
import streamlit as st
import pandas as pd
import networkx as nx


# ============================================================
# SHOW ANALYTICS PAGE
# ============================================================

def show():

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

        persons = pd.read_csv(
            os.path.join(DATA_DIR, "persons.csv")
        )

        calls = pd.read_csv(
            os.path.join(DATA_DIR, "calls.csv")
        )

        transactions = pd.read_csv(
            os.path.join(DATA_DIR, "transactions.csv")
        )

        cases = pd.read_csv(
            os.path.join(DATA_DIR, "cases.csv")
        )

        return persons, calls, transactions, cases


    # ============================================================
    # LOAD DATA SAFELY
    # ============================================================

    try:

        persons, calls, transactions, cases = load_data()

    except Exception as e:

        st.error("Unable to load data files.")

        st.code(str(e))

        st.info(
            "Make sure persons.csv, calls.csv, transactions.csv "
            "and cases.csv are inside SIH_FINAL/data."
        )

        return


    # ============================================================
    # HEADER
    # ============================================================

    st.title("📊 Network Analytics")

    st.markdown(
        """
        ### Criminal Network Intelligence

        This module analyses relationships between entities and
        calculates graph-based indicators to identify important
        structural patterns within the network.

        **Note:** These indicators are analytical aids and should not
        be treated as proof of criminal activity.
        """
    )

    st.divider()


    # ============================================================
    # CREATE GRAPH
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

        if caller in G and receiver in G:

            if G.has_edge(caller, receiver):

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

        if sender in G and receiver in G:

            try:
                amount = float(row["Amount"])
            except:
                amount = 0.0

            if G.has_edge(sender, receiver):

                G[sender][receiver]["weight"] += 1

                G[sender][receiver]["transaction_amount"] = (
                    G[sender][receiver].get(
                        "transaction_amount",
                        0
                    ) + amount
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
            round(density, 3)
        )

    with col4:

        st.metric(
            "🧩 Network Groups",
            components
        )


    st.divider()


    # ============================================================
    # CENTRALITY ANALYSIS
    # ============================================================

    st.subheader(
        "🎯 Entity Importance Analysis"
    )


    if number_of_nodes > 0:

        degree_centrality = nx.degree_centrality(G)

        betweenness_centrality = nx.betweenness_centrality(G)

        pagerank = nx.pagerank(G)

    else:

        degree_centrality = {}

        betweenness_centrality = {}

        pagerank = {}


    if number_of_nodes > 1:

        closeness_centrality = nx.closeness_centrality(G)

    else:

        closeness_centrality = {
            node: 0
            for node in G.nodes
        }


    # ============================================================
    # BUILD ANALYTICS TABLE
    # ============================================================

    analytics_data = []


    for node in G.nodes:

        analytics_data.append(
            {
                "Person ID": node,

                "Name": G.nodes[node].get(
                    "name",
                    node
                ),

                "Connections": G.degree(node),

                "Degree Centrality": round(
                    degree_centrality.get(node, 0),
                    4
                ),

                "Betweenness Centrality": round(
                    betweenness_centrality.get(node, 0),
                    4
                ),

                "Closeness Centrality": round(
                    closeness_centrality.get(node, 0),
                    4
                ),

                "PageRank": round(
                    pagerank.get(node, 0),
                    4
                )
            }
        )


    analytics_df = pd.DataFrame(
        analytics_data
    )


    if len(analytics_df) > 0:

        analytics_df = analytics_df.sort_values(
            by="Degree Centrality",
            ascending=False
        )


    # ============================================================
    # FULL ANALYTICS TABLE
    # ============================================================

    st.dataframe(
        analytics_df,
        width="stretch",
        hide_index=True
    )


    st.divider()


    # ============================================================
    # MOST CONNECTED
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
        width="stretch",
        hide_index=True
    )


    st.divider()


    # ============================================================
    # BETWEENNESS
    # ============================================================

    st.subheader(
        "🌉 Network Bridge Entities"
    )

    st.write(
        """
        High betweenness centrality indicates that an entity
        frequently lies on paths connecting different parts
        of the network.
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
        width="stretch",
        hide_index=True
    )


    st.divider()


    # ============================================================
    # PAGERANK
    # ============================================================

    st.subheader(
        "⭐ High Influence Entities"
    )

    st.write(
        """
        PageRank estimates structural importance based on
        relationships with other entities.
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
        width="stretch",
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
                ["Caller", "Receiver"]
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
            width="stretch",
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

        amounts = (
            pd.to_numeric(
                transactions["Amount"],
                errors="coerce"
            )
            .fillna(0)
        )


        total_transaction_value = amounts.sum()

        average_transaction = amounts.mean()

        largest_transaction = amounts.max()


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
            .assign(
                Amount=pd.to_numeric(
                    transactions["Amount"],
                    errors="coerce"
                ).fillna(0)
            )
            .groupby(
                ["Sender", "Receiver"]
            )["Amount"]
            .agg(
                ["count", "sum"]
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
            width="stretch",
            hide_index=True
        )


    else:

        st.info(
            "No transaction records available."
        )


    st.divider()


    # ============================================================
    # CONNECTED COMPONENTS
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

                "Number of Entities": len(component),

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
        width="stretch",
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
        This prototype combines multiple network indicators to
        prioritize data for human review. It does not determine
        guilt or criminality.
        """
    )


    priority_df = analytics_df.copy()


    # ============================================================
    # NORMALIZATION
    # ============================================================

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


    priority_df["Degree Score"] = normalize(
        priority_df["Degree Centrality"]
    )


    priority_df["Betweenness Score"] = normalize(
        priority_df["Betweenness Centrality"]
    )


    priority_df["PageRank Score"] = normalize(
        priority_df["PageRank"]
    )


    # ============================================================
    # PRIORITY SCORE
    # ============================================================

    priority_df["Priority Score"] = (
        priority_df["Degree Score"] * 0.35
        +
        priority_df["Betweenness Score"] * 0.35
        +
        priority_df["PageRank Score"] * 0.30
    )


    priority_df["Priority Score"] = (
        priority_df["Priority Score"].round(4)
    )


    priority_df = priority_df.sort_values(
        by="Priority Score",
        ascending=False
    )


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
        width="stretch",
        hide_index=True
    )


    st.divider()


    # ============================================================
    # INDIVIDUAL ENTITY INSPECTION
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
            analytics_df["Person ID"] == selected_entity
        ].iloc[0]


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Connections",
                int(
                    selected_row["Connections"]
                )
            )


        with col2:

            st.metric(
                "Degree",
                selected_row["Degree Centrality"]
            )


        with col3:

            st.metric(
                "Betweenness",
                selected_row["Betweenness Centrality"]
            )


        with col4:

            st.metric(
                "PageRank",
                selected_row["PageRank"]
            )


        # ========================================================
        # DIRECT CONNECTIONS
        # ========================================================

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

            neighbor_data.append(
                {
                    "Person ID": neighbor,

                    "Name": G.nodes[neighbor].get(
                        "name",
                        neighbor
                    )
                }
            )


        if len(neighbor_data) > 0:

            st.dataframe(
                pd.DataFrame(
                    neighbor_data
                ),
                width="stretch",
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


# Run the Analytics page
show()