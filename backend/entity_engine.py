import pandas as pd

try:
    from .data_loader import load_all_data
except ImportError:
    from data_loader import load_all_data


# ============================================================
# ENTITY ENGINE
# ============================================================

class EntityEngine:

    def __init__(self):

        (
            self.persons,
            self.calls,
            self.transactions,
            self.cases
        ) = load_all_data()


    # ========================================================
    # GET ENTITY
    # ========================================================

    def get_entity(self, person_id):

        person_id = str(person_id)

        result = self.persons[
            self.persons["Person_ID"].astype(str)
            == person_id
        ]

        if result.empty:

            return None

        return result.iloc[0].to_dict()


    # ========================================================
    # ALL ENTITIES
    # ========================================================

    def get_all_entities(self):

        return self.persons.to_dict(
            orient="records"
        )


    # ========================================================
    # ENTITY PROFILE
    # ========================================================

    def get_profile(self, person_id):

        person_id = str(person_id)

        person = self.get_entity(
            person_id
        )

        if person is None:

            return None

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

        cases = self.cases[
            self.cases["Person_ID"].astype(str)
            == person_id
        ]

        return {

            "person": person,

            "call_count":
                len(calls),

            "transaction_count":
                len(transactions),

            "case_count":
                len(cases),

            "total_transaction_value":
                float(
                    transactions["Amount"].sum()
                ),

            "cases":
                cases.to_dict(
                    orient="records"
                )
        }


    # ========================================================
    # RELATED ENTITIES
    # ========================================================

    def related_entities(self, person_id):

        person_id = str(person_id)

        related = set()

        outgoing = self.calls[
            self.calls["Caller"].astype(str)
            == person_id
        ]["Receiver"].astype(str)

        incoming = self.calls[
            self.calls["Receiver"].astype(str)
            == person_id
        ]["Caller"].astype(str)

        related.update(outgoing)
        related.update(incoming)

        outgoing = self.transactions[
            self.transactions["Sender"].astype(str)
            == person_id
        ]["Receiver"].astype(str)

        incoming = self.transactions[
            self.transactions["Receiver"].astype(str)
            == person_id
        ]["Sender"].astype(str)

        related.update(outgoing)
        related.update(incoming)

        related.discard(
            person_id
        )

        return list(
            related
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    engine = EntityEngine()

    print(
        engine.get_profile("P001")
    )