from flask import Flask, jsonify, request
from flask_cors import CORS

import os
import pandas as pd
import networkx as nx


# ============================================================
# CRIMEGRAPH AI - BACKEND API
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


# ============================================================
# DATA LOADING
# ============================================================

def load_csv(filename):

    filepath = os.path.join(
        DATA_DIR,
        filename
    )

    if not os.path.exists(filepath):

        print(
            f"WARNING: {filename} not found"
        )

        return pd.DataFrame()

    try:

        return pd.read_csv(filepath)

    except Exception as e:

        print(
            f"ERROR loading {filename}: {e}"
        )

        return pd.DataFrame()


persons = load_csv("persons.csv")
calls = load_csv("calls.csv")
transactions = load_csv("transactions.csv")
cases = load_csv("cases.csv")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_records(df):

    if df is None or df.empty:

        return []

    return df.fillna("").to_dict(
        orient="records"
    )


def get_person_calls(person_id):

    if calls.empty:

        return pd.DataFrame()

    person_id = str(person_id)

    return calls[
        (
            calls["Caller"]
            .astype(str)
            == person_id
        )
        |
        (
            calls["Receiver"]
            .astype(str)
            == person_id
        )
    ]


def get_person_transactions(person_id):

    if transactions.empty:

        return pd.DataFrame()

    person_id = str(person_id)

    return transactions[
        (
            transactions["Sender"]
            .astype(str)
            == person_id
        )
        |
        (
            transactions["Receiver"]
            .astype(str)
            == person_id
        )
    ]


def get_person_cases(person_id):

    if cases.empty:

        return pd.DataFrame()

    person_id = str(person_id)

    return cases[
        cases["Person_ID"]
        .astype(str)
        == person_id
    ]


# ============================================================
# BUILD NETWORK
# ============================================================

def build_graph():

    G = nx.Graph()

    # --------------------------------------------------------
    # PERSON NODES
    # --------------------------------------------------------

    if not persons.empty:

        for _, row in persons.iterrows():

            person_id = str(
                row["Person_ID"]
            )

            name = row.get(
                "Name",
                person_id
            )

            G.add_node(
                person_id,
                name=str(name),
                type="PERSON"
            )


    # --------------------------------------------------------
    # CALL EDGES
    # --------------------------------------------------------

    if not calls.empty:

        for _, row in calls.iterrows():

            caller = str(
                row["Caller"]
            )

            receiver = str(
                row["Receiver"]
            )

            if (
                caller in G
                and receiver in G
            ):

                if G.has_edge(
                    caller,
                    receiver
                ):

                    G[caller][receiver][
                        "weight"
                    ] += 1

                else:

                    G.add_edge(
                        caller,
                        receiver,
                        relationship="CALL",
                        weight=1
                    )


    # --------------------------------------------------------
    # TRANSACTION EDGES
    # --------------------------------------------------------

    if not transactions.empty:

        for _, row in transactions.iterrows():

            sender = str(
                row["Sender"]
            )

            receiver = str(
                row["Receiver"]
            )

            if (
                sender in G
                and receiver in G
            ):

                amount = row.get(
                    "Amount",
                    0
                )

                try:

                    amount = float(amount)

                except:

                    amount = 0


                if G.has_edge(
                    sender,
                    receiver
                ):

                    G[sender][receiver][
                        "transaction_count"
                    ] = (
                        G[sender][receiver]
                        .get(
                            "transaction_count",
                            0
                        )
                        + 1
                    )

                    G[sender][receiver][
                        "transaction_amount"
                    ] = (
                        G[sender][receiver]
                        .get(
                            "transaction_amount",
                            0
                        )
                        + amount
                    )

                else:

                    G.add_edge(
                        sender,
                        receiver,
                        relationship="TRANSACTION",
                        weight=1,
                        transaction_count=1,
                        transaction_amount=amount
                    )


    return G


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return jsonify({

        "system":
            "CrimeGraph AI",

        "status":
            "running",

        "version":
            "1.0",

        "message":
            "CrimeGraph AI Backend API is working"

    })


# ============================================================
# HEALTH
# ============================================================

@app.route("/api/health")
def health():

    return jsonify({

        "status":
            "healthy",

        "backend":
            "CrimeGraph AI",

        "persons":
            len(persons),

        "calls":
            len(calls),

        "transactions":
            len(transactions),

        "cases":
            len(cases)

    })


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/api/dashboard")
def dashboard():

    G = build_graph()

    return jsonify({

        "persons":
            len(persons),

        "calls":
            len(calls),

        "transactions":
            len(transactions),

        "cases":
            len(cases),

        "relationships":
            G.number_of_edges(),

        "network_entities":
            G.number_of_nodes(),

        "network_density":
            round(
                nx.density(G),
                4
            ) if G.number_of_nodes() > 1 else 0

    })


# ============================================================
# PERSONS
# ============================================================

@app.route("/api/persons")
def get_persons():

    return jsonify(
        safe_records(persons)
    )


# ============================================================
# CALLS
# ============================================================

@app.route("/api/calls")
def get_calls():

    return jsonify(
        safe_records(calls)
    )


# ============================================================
# TRANSACTIONS
# ============================================================

@app.route("/api/transactions")
def get_transactions():

    return jsonify(
        safe_records(transactions)
    )


# ============================================================
# CASES
# ============================================================

@app.route("/api/cases")
def get_cases():

    return jsonify(
        safe_records(cases)
    )


# ============================================================
# ENTITY SEARCH
# ============================================================

@app.route("/api/search")
def search():

    query = request.args.get(
        "q",
        ""
    ).strip().lower()

    if not query:

        return jsonify([])


    if persons.empty:

        return jsonify([])


    result = persons[
        persons.astype(str)
        .apply(
            lambda row:
            row.str.lower()
            .str.contains(
                query,
                na=False
            )
            .any(),
            axis=1
        )
    ]


    return jsonify(
        safe_records(result)
    )


# ============================================================
# PERSON DETAILS
# ============================================================

@app.route("/api/person/<person_id>")
def person_details(person_id):

    person_id = str(
        person_id
    )


    if persons.empty:

        return jsonify({
            "error":
                "Person database is empty"
        }), 404


    person = persons[
        persons["Person_ID"]
        .astype(str)
        == person_id
    ]


    if person.empty:

        return jsonify({
            "error":
                "Person not found"
        }), 404


    person_calls = (
        get_person_calls(
            person_id
        )
    )

    person_transactions = (
        get_person_transactions(
            person_id
        )
    )

    person_cases = (
        get_person_cases(
            person_id
        )
    )


    return jsonify({

        "person":
            safe_records(
                person
            )[0],

        "calls":
            safe_records(
                person_calls
            ),

        "transactions":
            safe_records(
                person_transactions
            ),

        "cases":
            safe_records(
                person_cases
            )

    })


# ============================================================
# NETWORK GRAPH
# ============================================================

@app.route("/api/network")
def network():

    G = build_graph()

    nodes = []

    edges = []


    # --------------------------------------------------------
    # NODES
    # --------------------------------------------------------

    for node, data in G.nodes(
        data=True
    ):

        nodes.append({

            "id":
                node,

            "label":
                data.get(
                    "name",
                    node
                ),

            "type":
                data.get(
                    "type",
                    "PERSON"
                ),

            "connections":
                G.degree(node)

        })


    # --------------------------------------------------------
    # EDGES
    # --------------------------------------------------------

    for source, target, data in G.edges(
        data=True
    ):

        edges.append({

            "source":
                source,

            "target":
                target,

            "relationship":
                data.get(
                    "relationship",
                    "UNKNOWN"
                ),

            "weight":
                data.get(
                    "weight",
                    1
                ),

            "transaction_amount":
                data.get(
                    "transaction_amount",
                    0
                )

        })


    return jsonify({

        "nodes":
            nodes,

        "edges":
            edges,

        "node_count":
            len(nodes),

        "edge_count":
            len(edges)

    })


# ============================================================
# NETWORK ANALYTICS
# ============================================================

@app.route("/api/analytics")
def analytics():

    G = build_graph()


    if G.number_of_nodes() == 0:

        return jsonify({

            "summary": {},

            "entities": []

        })


    # --------------------------------------------------------
    # CENTRALITIES
    # --------------------------------------------------------

    degree = nx.degree_centrality(G)

    betweenness = (
        nx.betweenness_centrality(G)
    )

    closeness = (
        nx.closeness_centrality(G)
    )

    clustering = (
        nx.clustering(G)
    )


    # --------------------------------------------------------
    # PAGERANK
    # --------------------------------------------------------

    try:

        pagerank = nx.pagerank(
            G
        )

    except Exception:

        pagerank = {

            node:
                0

            for node in G.nodes()

        }


    # --------------------------------------------------------
    # ENTITY ANALYTICS
    # --------------------------------------------------------

    results = []


    for node in G.nodes():

        name = G.nodes[node].get(
            "name",
            node
        )


        results.append({

            "Person_ID":
                node,

            "Person":
                name,

            "Connections":
                G.degree(node),

            "Degree_Centrality":
                round(
                    degree.get(
                        node,
                        0
                    ),
                    4
                ),

            "Betweenness_Centrality":
                round(
                    betweenness.get(
                        node,
                        0
                    ),
                    4
                ),

            "Closeness_Centrality":
                round(
                    closeness.get(
                        node,
                        0
                    ),
                    4
                ),

            "PageRank":
                round(
                    pagerank.get(
                        node,
                        0
                    ),
                    4
                ),

            "Clustering":
                round(
                    clustering.get(
                        node,
                        0
                    ),
                    4
                )

        })


    results.sort(
        key=lambda x:
            x["PageRank"],
        reverse=True
    )


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    components = list(
        nx.connected_components(G)
    )


    summary = {

        "entities":
            G.number_of_nodes(),

        "relationships":
            G.number_of_edges(),

        "density":
            round(
                nx.density(G),
                4
            ),

        "connected_components":
            len(components),

        "isolated_entities":
            len(
                list(
                    nx.isolates(G)
                )
            )

    }


    return jsonify({

        "summary":
            summary,

        "entities":
            results

    })


# ============================================================
# RISK ANALYSIS
# ============================================================

@app.route("/api/risk/<person_id>")
def risk(person_id):

    person_id = str(
        person_id
    )


    G = build_graph()


    if person_id not in G:

        return jsonify({

            "error":
                "Person not found"

        }), 404


    score = 0

    reasons = []


    # --------------------------------------------------------
    # COMMUNICATION ACTIVITY
    # --------------------------------------------------------

    person_calls = (
        get_person_calls(
            person_id
        )
    )

    call_count = len(
        person_calls
    )


    if call_count >= 5:

        score += 25

        reasons.append(
            "High communication activity"
        )

    elif call_count >= 2:

        score += 15

        reasons.append(
            "Moderate communication activity"
        )


    # --------------------------------------------------------
    # NETWORK CONNECTIONS
    # --------------------------------------------------------

    connections = G.degree(
        person_id
    )


    if connections >= 6:

        score += 25

        reasons.append(
            "High number of network connections"
        )

    elif connections >= 3:

        score += 15

        reasons.append(
            "Multiple network connections"
        )


    # --------------------------------------------------------
    # TRANSACTION ACTIVITY
    # --------------------------------------------------------

    person_transactions = (
        get_person_transactions(
            person_id
        )
    )


    transaction_total = 0


    if (
        not person_transactions.empty
        and
        "Amount" in
        person_transactions.columns
    ):

        transaction_total = float(
            person_transactions[
                "Amount"
            ].sum()
        )


    if transaction_total >= 75000:

        score += 30

        reasons.append(
            "High transaction value"
        )

    elif transaction_total >= 50000:

        score += 25

        reasons.append(
            "Elevated transaction value"
        )

    elif transaction_total >= 20000:

        score += 15

        reasons.append(
            "Moderate transaction activity"
        )


    # --------------------------------------------------------
    # CASE PRIORITY
    # --------------------------------------------------------

    person_cases = (
        get_person_cases(
            person_id
        )
    )


    high_priority = 0


    if (
        not person_cases.empty
        and
        "Priority" in
        person_cases.columns
    ):

        high_priority = len(
            person_cases[
                person_cases[
                    "Priority"
                ]
                .astype(str)
                .str.lower()
                .isin(
                    [
                        "high",
                        "critical"
                    ]
                )
            ]
        )


    if high_priority > 0:

        score += 15

        reasons.append(
            "Associated with high-priority case(s)"
        )


    # --------------------------------------------------------
    # CAP SCORE
    # --------------------------------------------------------

    score = min(
        score,
        100
    )


    # --------------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------------

    if score >= 70:

        level = "HIGH"

    elif score >= 40:

        level = "MEDIUM"

    else:

        level = "LOW"


    return jsonify({

        "Person_ID":
            person_id,

        "Score":
            score,

        "Level":
            level,

        "Reasons":
            reasons,

        "Metrics": {

            "Connections":
                connections,

            "Calls":
                call_count,

            "Transaction_Total":
                transaction_total,

            "High_Priority_Cases":
                high_priority

        }

    })


# ============================================================
# ALERTS
# ============================================================

@app.route("/api/alerts")
def alerts():

    alert_list = []


    # --------------------------------------------------------
    # REPEATED COMMUNICATION
    # --------------------------------------------------------

    if not calls.empty:

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
                name="Number_of_Calls"
            )
        )


        repeated = call_counts[
            call_counts[
                "Number_of_Calls"
            ] >= 2
        ]


        for _, row in repeated.iterrows():

            alert_list.append({

                "Alert_Type":
                    "Repeated Communication",

                "Severity":
                    "MEDIUM",

                "Description":
                    (
                        f"{int(row['Number_of_Calls'])} "
                        f"calls between "
                        f"{row['Caller']} and "
                        f"{row['Receiver']}"
                    ),

                "Caller":
                    str(
                        row["Caller"]
                    ),

                "Receiver":
                    str(
                        row["Receiver"]
                    ),

                "Count":
                    int(
                        row["Number_of_Calls"]
                    )

            })


    # --------------------------------------------------------
    # UNUSUAL TRANSACTIONS
    # --------------------------------------------------------

    if (
        not transactions.empty
        and
        "Amount" in transactions.columns
    ):

        average = float(
            transactions[
                "Amount"
            ].mean()
        )


        unusual = transactions[
            transactions[
                "Amount"
            ]
            > average * 2
        ]


        for _, row in unusual.iterrows():

            amount = float(
                row["Amount"]
            )


            alert_list.append({

                "Alert_Type":
                    "Unusual Transaction",

                "Severity":
                    "HIGH",

                "Description":
                    f"Transaction of ₹{amount:,.0f}",

                "Sender":
                    str(
                        row["Sender"]
                    ),

                "Receiver":
                    str(
                        row["Receiver"]
                    ),

                "Amount":
                    amount

            })


    # --------------------------------------------------------
    # HIGH PRIORITY CASES
    # --------------------------------------------------------

    if (
        not cases.empty
        and
        "Priority" in cases.columns
    ):

        high_cases = cases[
            cases[
                "Priority"
            ]
            .astype(str)
            .str.lower()
            .isin(
                [
                    "high",
                    "critical"
                ]
            )
        ]


        for _, row in high_cases.iterrows():

            alert_list.append({

                "Alert_Type":
                    "High Priority Case",

                "Severity":
                    "HIGH",

                "Description":
                    (
                        f"Case "
                        f"{row['Case_ID']} "
                        f"has "
                        f"{row['Priority']} "
                        f"priority"
                    ),

                "Case_ID":
                    str(
                        row["Case_ID"]
                    ),

                "Person_ID":
                    str(
                        row["Person_ID"]
                    )

            })


    return jsonify(
        alert_list
    )


# ============================================================
# CASE DETAILS
# ============================================================

@app.route("/api/case/<case_id>")
def case_details(case_id):

    case_id = str(
        case_id
    )


    if cases.empty:

        return jsonify({

            "error":
                "No cases available"

        }), 404


    case = cases[
        cases["Case_ID"]
        .astype(str)
        == case_id
    ]


    if case.empty:

        return jsonify({

            "error":
                "Case not found"

        }), 404


    case_record = safe_records(
        case
    )[0]


    person_id = str(
        case_record.get(
            "Person_ID",
            ""
        )
    )


    person = pd.DataFrame()


    if not persons.empty:

        person = persons[
            persons[
                "Person_ID"
            ]
            .astype(str)
            == person_id
        ]


    person_calls = (
        get_person_calls(
            person_id
        )
    )

    person_transactions = (
        get_person_transactions(
            person_id
        )
    )


    return jsonify({

        "case":
            case_record,

        "person":
            safe_records(
                person
            ),

        "calls":
            safe_records(
                person_calls
            ),

        "transactions":
            safe_records(
                person_transactions
            )

    })


# ============================================================
# CASE LIST WITH STATISTICS
# ============================================================

@app.route("/api/case-summary")
def case_summary():

    if cases.empty:

        return jsonify({

            "total": 0,

            "open": 0,

            "closed": 0,

            "high_priority": 0

        })


    total = len(
        cases
    )


    open_count = 0

    closed_count = 0

    high_priority = 0


    if "Status" in cases.columns:

        status = (
            cases["Status"]
            .astype(str)
            .str.lower()
        )

        open_count = int(
            (
                status == "open"
            ).sum()
        )

        closed_count = int(
            (
                status == "closed"
            ).sum()
        )


    if "Priority" in cases.columns:

        priority = (
            cases["Priority"]
            .astype(str)
            .str.lower()
        )

        high_priority = int(
            priority
            .isin(
                [
                    "high",
                    "critical"
                ]
            )
            .sum()
        )


    return jsonify({

        "total":
            total,

        "open":
            open_count,

        "closed":
            closed_count,

        "high_priority":
            high_priority

    })


# ============================================================
# TRANSACTION SUMMARY
# ============================================================

@app.route("/api/transaction-summary")
def transaction_summary():

    if transactions.empty:

        return jsonify({

            "count": 0,

            "total_amount": 0,

            "average_amount": 0,

            "maximum_amount": 0

        })


    if "Amount" not in transactions.columns:

        return jsonify({

            "count":
                len(transactions),

            "total_amount":
                0,

            "average_amount":
                0,

            "maximum_amount":
                0

        })


    amounts = pd.to_numeric(
        transactions["Amount"],
        errors="coerce"
    ).fillna(0)


    return jsonify({

        "count":
            len(transactions),

        "total_amount":
            float(
                amounts.sum()
            ),

        "average_amount":
            round(
                float(
                    amounts.mean()
                ),
                2
            ),

        "maximum_amount":
            float(
                amounts.max()
            )

    })


# ============================================================
# COMMUNICATION SUMMARY
# ============================================================

@app.route("/api/call-summary")
def call_summary():

    if calls.empty:

        return jsonify({

            "total_calls":
                0,

            "unique_callers":
                0,

            "unique_receivers":
                0,

            "unique_pairs":
                0

        })


    unique_callers = (
        calls["Caller"]
        .nunique()
    )


    unique_receivers = (
        calls["Receiver"]
        .nunique()
    )


    unique_pairs = (
        calls[
            [
                "Caller",
                "Receiver"
            ]
        ]
        .drop_duplicates()
        .shape[0]
    )


    return jsonify({

        "total_calls":
            len(calls),

        "unique_callers":
            unique_callers,

        "unique_receivers":
            unique_receivers,

        "unique_pairs":
            unique_pairs

    })


# ============================================================
# TOP ENTITIES
# ============================================================

@app.route("/api/top-entities")
def top_entities():

    G = build_graph()


    if G.number_of_nodes() == 0:

        return jsonify([])


    degree = nx.degree_centrality(
        G
    )


    results = []


    for node in G.nodes():

        results.append({

            "Person_ID":
                node,

            "Person":
                G.nodes[node].get(
                    "name",
                    node
                ),

            "Connections":
                G.degree(node),

            "Centrality":
                round(
                    degree.get(
                        node,
                        0
                    ),
                    4
                )

        })


    results.sort(
        key=lambda x:
            x["Centrality"],
        reverse=True
    )


    return jsonify(
        results[:10]
    )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "CRIMEGRAPH AI BACKEND"
    )

    print("=" * 60)

    print()

    print(
        "Backend starting..."
    )

    print(
        "API: http://127.0.0.1:5000"
    )

    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )