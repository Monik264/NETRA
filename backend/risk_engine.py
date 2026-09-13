import pandas as pd

try:
    from .data_loader import load_all_data
    from .graph_engine import CrimeGraph
except ImportError:
    from data_loader import load_all_data
    from graph_engine import CrimeGraph


# ============================================================
# RISK / PRIORITY ENGINE
# ============================================================

class RiskEngine:

    def __init__(self):

        (
            self.persons,
            self.calls,
            self.transactions,
            self.cases
        ) = load_all_data()

        self.graph_engine = CrimeGraph()


    # ========================================================
    # PERSON SCORE
    # ========================================================

    def calculate_score(self, person_id):

        person_id = str(person_id)

        score = 0

        reasons = []


        # ----------------------------------------------------
        # CONNECTION SCORE
        # ----------------------------------------------------

        connections = 0

        if person_id in self.graph_engine.graph:

            connections = (
                self.graph_engine.graph.degree(
                    person_id
                )
            )

        if connections >= 8:

            score += 25

            reasons.append(
                "High number of network connections"
            )

        elif connections >= 5:

            score += 15

            reasons.append(
                "Moderate number of network connections"
            )


        # ----------------------------------------------------
        # CALL SCORE
        # ----------------------------------------------------

        person_calls = self.calls[
            (self.calls["Caller"].astype(str) == person_id)
            |
            (self.calls["Receiver"].astype(str) == person_id)
        ]

        call_count = len(
            person_calls
        )

        if call_count >= 8:

            score += 20

            reasons.append(
                "High communication activity"
            )

        elif call_count >= 5:

            score += 10

            reasons.append(
                "Moderate communication activity"
            )


        # ----------------------------------------------------
        # TRANSACTION SCORE
        # ----------------------------------------------------

        person_transactions = self.transactions[
            (self.transactions["Sender"].astype(str) == person_id)
            |
            (self.transactions["Receiver"].astype(str) == person_id)
        ]

        total_value = float(
            person_transactions[
                "Amount"
            ].sum()
        )

        if total_value >= 100000:

            score += 30

            reasons.append(
                "High total transaction value"
            )

        elif total_value >= 50000:

            score += 20

            reasons.append(
                "Elevated transaction value"
            )


        # ----------------------------------------------------
        # CASE SCORE
        # ----------------------------------------------------

        person_cases = self.cases[
            self.cases["Person_ID"].astype(str)
            == person_id
        ]

        high_cases = (
            person_cases["Priority"]
            == "High"
        ).sum()

        score += min(
            int(high_cases) * 10,
            20
        )

        if high_cases > 0:

            reasons.append(
                "Associated with high-priority case(s)"
            )


        # ----------------------------------------------------
        # CAP SCORE
        # ----------------------------------------------------

        score = min(
            score,
            100
        )


        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        if score >= 70:

            level = "HIGH"

        elif score >= 40:

            level = "MEDIUM"

        else:

            level = "LOW"


        return {

            "Person_ID":
                person_id,

            "Score":
                score,

            "Level":
                level,

            "Reasons":
                reasons
        }


    # ========================================================
    # ALL SCORES
    # ========================================================

    def all_scores(self):

        results = []

        for person_id in self.persons[
            "Person_ID"
        ]:

            results.append(
                self.calculate_score(
                    person_id
                )
            )

        return pd.DataFrame(
            results
        ).sort_values(
            "Score",
            ascending=False
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    engine = RiskEngine()

    print(
        engine.all_scores()
        .head(10)
        .to_string(index=False)
    )