import os
import sys
import pandas as pd
import networkx as nx


# =========================================================
# PATH SETUP
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


# =========================================================
# LOAD DATA
# =========================================================

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

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


# =========================================================
# ANALYTICS ENGINE
# =========================================================

class AnalyticsEngine:

    def __init__(
        self,
        persons,
        calls,
        transactions,
        cases
    ):

        self.persons = persons
        self.calls = calls
        self.transactions = transactions
        self.cases = cases

        self.graph = nx.Graph()

        self.build_graph()


    # =====================================================
    # BUILD GRAPH
    # =====================================================

    def build_graph(self):

        # Add people

        for _, row in self.persons.iterrows():

            person_id = str(
                row["Person_ID"]
            )

            self.graph.add_node(
                person_id,
                name=row.get(
                    "Name",
                    person_id
                )
            )


        # Add call relationships

        for _, row in self.calls.iterrows():

            caller = str(
                row["Caller"]
            )

            receiver = str(
                row["Receiver"]
            )

            if (
                caller in self.graph
                and receiver in self.graph
            ):

                self.graph.add_edge(
                    caller,
                    receiver,
                    relationship="CALL"
                )


        # Add transaction relationships

        for _, row in self.transactions.iterrows():

            sender = str(
                row["Sender"]
            )

            receiver = str(
                row["Receiver"]
            )

            if (
                sender in self.graph
                and receiver in self.graph
            ):

                self.graph.add_edge(
                    sender,
                    receiver,
                    relationship="TRANSACTION"
                )


    # =====================================================
    # DEGREE CENTRALITY
    # =====================================================

    def degree_centrality(self):

        return nx.degree_centrality(
            self.graph
        )


    # =====================================================
    # BETWEENNESS CENTRALITY
    # =====================================================

    def betweenness_centrality(self):

        return nx.betweenness_centrality(
            self.graph
        )


    # =====================================================
    # CLOSENESS CENTRALITY
    # =====================================================

    def closeness_centrality(self):

        return nx.closeness_centrality(
            self.graph
        )


    # =====================================================
    # PAGERANK
    # =====================================================

    def page_rank(self):

        return nx.pagerank(
            self.graph
        )


    # =====================================================
    # CLUSTERING COEFFICIENT
    # =====================================================

    def clustering_coefficient(self):

        return nx.clustering(
            self.graph
        )


    # =====================================================
    # NETWORK DENSITY
    # =====================================================

    def network_density(self):

        return nx.density(
            self.graph
        )


    # =====================================================
    # CONNECTED COMPONENTS
    # =====================================================

    def connected_components(self):

        components = list(
            nx.connected_components(
                self.graph
            )
        )

        return [
            list(component)
            for component in components
        ]


    # =====================================================
    # PERSON RISK SCORE
    # =====================================================

    def calculate_risk_scores(self):

        degree = self.degree_centrality()

        betweenness = (
            self.betweenness_centrality()
        )

        pagerank = self.page_rank()

        closeness = (
            self.closeness_centrality()
        )


        scores = []


        for node in self.graph.nodes:

            # Normalize network metrics

            degree_score = (
                degree.get(node, 0)
            )

            between_score = (
                betweenness.get(node, 0)
            )

            page_score = (
                pagerank.get(node, 0)
            )

            close_score = (
                closeness.get(node, 0)
            )


            # Weighted score

            risk = (

                degree_score * 0.30

                +

                between_score * 0.30

                +

                page_score * 0.25

                +

                close_score * 0.15

            )


            # Convert to 0-100

            risk = round(
                risk * 100,
                2
            )


            name = self.graph.nodes[
                node
            ].get(
                "name",
                node
            )


            scores.append({

                "Person_ID":
                    node,

                "Person":
                    name,

                "Degree_Centrality":
                    round(
                        degree_score,
                        4
                    ),

                "Betweenness_Centrality":
                    round(
                        between_score,
                        4
                    ),

                "PageRank":
                    round(
                        page_score,
                        4
                    ),

                "Closeness_Centrality":
                    round(
                        close_score,
                        4
                    ),

                "Risk_Score":
                    risk

            })


        result = pd.DataFrame(
            scores
        )


        return result.sort_values(
            "Risk_Score",
            ascending=False
        )


    # =====================================================
    # TOP INFLUENTIAL ENTITIES
    # =====================================================

    def top_entities(
        self,
        limit=10
    ):

        result = (
            self.calculate_risk_scores()
        )

        return result.head(
            limit
        )


    # =====================================================
    # NETWORK SUMMARY
    # =====================================================

    def network_summary(self):

        return {

            "total_entities":
                self.graph.number_of_nodes(),

            "total_relationships":
                self.graph.number_of_edges(),

            "network_density":
                round(
                    self.network_density(),
                    4
                ),

            "connected_components":
                len(
                    self.connected_components()
                ),

            "isolated_entities":
                len(
                    list(
                        nx.isolates(
                            self.graph
                        )
                    )
                )

        }


# =========================================================
# TEST ENGINE
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("CRIMEGRAPH AI ANALYTICS ENGINE")
    print("=" * 60)

    engine = AnalyticsEngine(
        persons,
        calls,
        transactions,
        cases
    )

    print()
    print("NETWORK SUMMARY")
    print("-" * 60)

    summary = engine.network_summary()

    for key, value in summary.items():

        print(
            f"{key}: {value}"
        )


    print()
    print("TOP INFLUENTIAL ENTITIES")
    print("-" * 60)

    top = engine.top_entities(
        10
    )

    print(
        top[
            [
                "Person_ID",
                "Person",
                "Risk_Score"
            ]
        ].to_string(
            index=False
        )
    )

    print()
    print("ANALYTICS ENGINE READY")