import networkx as nx
import pandas as pd

try:
    from .data_loader import load_all_data
except ImportError:
    from data_loader import load_all_data


# ============================================================
# CRIME NETWORK GRAPH
# ============================================================

class CrimeGraph:

    def __init__(self):

        (
            self.persons,
            self.calls,
            self.transactions,
            self.cases
        ) = load_all_data()

        self.graph = nx.MultiDiGraph()

        self.build_graph()


    # ========================================================
    # BUILD GRAPH
    # ========================================================

    def build_graph(self):

        # ----------------------------------------------------
        # PERSON NODES
        # ----------------------------------------------------

        for _, row in self.persons.iterrows():

            person_id = str(
                row["Person_ID"]
            )

            self.graph.add_node(

                person_id,

                entity_type="PERSON",

                name=str(row["Name"]),

                phone=str(row["Phone"]),

                location=str(row["Location"]),

                vehicle=str(row["Vehicle"])
            )


        # ----------------------------------------------------
        # CALL EDGES
        # ----------------------------------------------------

        for _, row in self.calls.iterrows():

            caller = str(row["Caller"])
            receiver = str(row["Receiver"])

            if (
                caller in self.graph
                and receiver in self.graph
            ):

                self.graph.add_edge(

                    caller,
                    receiver,

                    relationship="CALL",

                    record_id=str(
                        row["Call_ID"]
                    ),

                    date=str(
                        row["Date"]
                    ),

                    time=str(
                        row["Time"]
                    ),

                    duration=float(
                        row["Duration_Seconds"]
                    )
                )


        # ----------------------------------------------------
        # TRANSACTION EDGES
        # ----------------------------------------------------

        for _, row in self.transactions.iterrows():

            sender = str(row["Sender"])
            receiver = str(row["Receiver"])

            if (
                sender in self.graph
                and receiver in self.graph
            ):

                self.graph.add_edge(

                    sender,
                    receiver,

                    relationship="TRANSACTION",

                    record_id=str(
                        row["Transaction_ID"]
                    ),

                    amount=float(
                        row["Amount"]
                    ),

                    date=str(
                        row["Date"]
                    ),

                    transaction_type=str(
                        row["Type"]
                    )
                )


    # ========================================================
    # SUMMARY
    # ========================================================

    def summary(self):

        return {

            "entities":
                self.graph.number_of_nodes(),

            "relationships":
                self.graph.number_of_edges(),

            "call_records":
                len(self.calls),

            "transactions":
                len(self.transactions),

            "cases":
                len(self.cases)
        }


    # ========================================================
    # PERSON
    # ========================================================

    def get_person(self, person_id):

        person_id = str(person_id)

        if person_id not in self.graph:

            return None

        data = dict(
            self.graph.nodes[person_id]
        )

        data["Person_ID"] = person_id

        return data


    # ========================================================
    # CONNECTIONS
    # ========================================================

    def get_connections(self, person_id):

        person_id = str(person_id)

        if person_id not in self.graph:

            return []

        results = []

        for source, target, data in self.graph.edges(
            person_id,
            data=True
        ):

            results.append({

                "source": source,

                "target": target,

                "relationship":
                    data.get("relationship"),

                "record_id":
                    data.get("record_id")
            })


        for source, target, data in self.graph.in_edges(
            person_id,
            data=True
        ):

            results.append({

                "source": source,

                "target": target,

                "relationship":
                    data.get("relationship"),

                "record_id":
                    data.get("record_id")
            })


        return results


    # ========================================================
    # PERSON CALLS
    # ========================================================

    def get_person_calls(self, person_id):

        person_id = str(person_id)

        return self.calls[
            (self.calls["Caller"].astype(str) == person_id)
            |
            (self.calls["Receiver"].astype(str) == person_id)
        ].copy()


    # ========================================================
    # PERSON TRANSACTIONS
    # ========================================================

    def get_person_transactions(
        self,
        person_id
    ):

        person_id = str(person_id)

        return self.transactions[
            (self.transactions["Sender"].astype(str) == person_id)
            |
            (self.transactions["Receiver"].astype(str) == person_id)
        ].copy()


    # ========================================================
    # DEGREE CENTRALITY
    # ========================================================

    def degree_centrality(self):

        return nx.degree_centrality(
            self.graph
        )


    # ========================================================
    # BETWEENNESS
    # ========================================================

    def betweenness_centrality(self):

        return nx.betweenness_centrality(
            self.graph
        )


    # ========================================================
    # PAGERANK
    # ========================================================

    def page_rank(self):

        return nx.pagerank(
            self.graph
        )


    # ========================================================
    # ANALYTICS
    # ========================================================

    def get_network_analytics(self):

        degree = self.degree_centrality()

        betweenness = self.betweenness_centrality()

        pagerank = self.page_rank()

        results = []

        for person_id in self.graph.nodes:

            data = self.graph.nodes[
                person_id
            ]

            results.append({

                "Person_ID": person_id,

                "Name":
                    data.get("name"),

                "Connections":
                    self.graph.degree(
                        person_id
                    ),

                "Degree_Centrality":
                    round(
                        degree.get(
                            person_id,
                            0
                        ),
                        4
                    ),

                "Betweenness_Centrality":
                    round(
                        betweenness.get(
                            person_id,
                            0
                        ),
                        4
                    ),

                "PageRank":
                    round(
                        pagerank.get(
                            person_id,
                            0
                        ),
                        4
                    )
            })


        return pd.DataFrame(
            results
        ).sort_values(
            by="Degree_Centrality",
            ascending=False
        )


    # ========================================================
    # SHORTEST PATH
    # ========================================================

    def shortest_path(
        self,
        source,
        target
    ):

        source = str(source)
        target = str(target)

        if (
            source not in self.graph
            or target not in self.graph
        ):

            return []

        try:

            return nx.shortest_path(
                self.graph,
                source,
                target
            )

        except nx.NetworkXNoPath:

            return []


    # ========================================================
    # COMMON CONNECTIONS
    # ========================================================

    def common_connections(
        self,
        person1,
        person2
    ):

        person1 = str(person1)
        person2 = str(person2)

        if (
            person1 not in self.graph
            or person2 not in self.graph
        ):

            return []

        c1 = set(
            self.graph.neighbors(
                person1
            )
        )

        c2 = set(
            self.graph.neighbors(
                person2
            )
        )

        return list(
            c1.intersection(c2)
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    graph = CrimeGraph()

    print("=" * 60)
    print("CRIMEGRAPH AI GRAPH ENGINE")
    print("=" * 60)

    print()

    print(
        graph.summary()
    )

    print()

    print(
        graph.get_network_analytics()
        .head(10)
        .to_string(index=False)
    )