import pandas as pd

try:
    from .data_loader import load_all_data
except ImportError:
    from data_loader import load_all_data


# ============================================================
# CASE ENGINE
# ============================================================

class CaseEngine:

    def __init__(self):

        (
            self.persons,
            self.calls,
            self.transactions,
            self.cases
        ) = load_all_data()


    # ========================================================
    # ALL CASES
    # ========================================================

    def get_all_cases(self):

        return self.cases.to_dict(
            orient="records"
        )


    # ========================================================
    # GET CASE
    # ========================================================

    def get_case(self, case_id):

        result = self.cases[
            self.cases["Case_ID"].astype(str)
            == str(case_id)
        ]

        if result.empty:

            return None

        return result.iloc[0].to_dict()


    # ========================================================
    # CASE PERSON
    # ========================================================

    def get_case_person(self, case_id):

        case = self.get_case(
            case_id
        )

        if case is None:

            return None

        person_id = str(
            case["Person_ID"]
        )

        result = self.persons[
            self.persons["Person_ID"].astype(str)
            == person_id
        ]

        if result.empty:

            return None

        return result.iloc[0].to_dict()


    # ========================================================
    # CASE INVESTIGATION DATA
    # ========================================================

    def get_case_details(self, case_id):

        case = self.get_case(
            case_id
        )

        if case is None:

            return None

        person_id = str(
            case["Person_ID"]
        )

        person = self.get_case_person(
            case_id
        )

        calls = self.calls[
            (self.calls["Caller"].astype(str) == person_id)
            |
            (self.calls["Receiver"].astype(str) == person_id)
        ]

        transactions = self.transactions[
            (self.transactions["Sender"].astype(str) == person_id)
            |
            (self.transactions["Receiver"].astype(str) == person_id)
        ]

        return {

            "case": case,

            "person": person,

            "calls":
                calls.to_dict(
                    orient="records"
                ),

            "transactions":
                transactions.to_dict(
                    orient="records"
                )
        }


    # ========================================================
    # CASE STATISTICS
    # ========================================================

    def statistics(self):

        return {

            "total":
                len(self.cases),

            "open":
                int(
                    (
                        self.cases["Status"]
                        == "Open"
                    ).sum()
                ),

            "under_review":
                int(
                    (
                        self.cases["Status"]
                        == "Under Review"
                    ).sum()
                ),

            "closed":
                int(
                    (
                        self.cases["Status"]
                        == "Closed"
                    ).sum()
                ),

            "high_priority":
                int(
                    (
                        self.cases["Priority"]
                        == "High"
                    ).sum()
                )
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    engine = CaseEngine()

    print(
        engine.statistics()
    )

    print()

    print(
        engine.get_case_details(
            "CASE001"
        )
    )