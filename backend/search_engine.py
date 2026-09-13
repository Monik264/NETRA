import pandas as pd

try:
    from .data_loader import load_all_data
except ImportError:
    from data_loader import load_all_data


# ============================================================
# SEARCH ENGINE
# ============================================================

class SearchEngine:

    def __init__(self):

        (
            self.persons,
            self.calls,
            self.transactions,
            self.cases
        ) = load_all_data()


    # ========================================================
    # GENERAL PERSON SEARCH
    # ========================================================

    def search_persons(self, query):

        query = str(
            query
        ).strip().lower()

        if not query:

            return []

        mask = (
            self.persons
            .astype(str)
            .apply(
                lambda column:
                column.str.lower()
                .str.contains(
                    query,
                    na=False
                )
            )
            .any(axis=1)
        )

        results = self.persons[
            mask
        ]

        return results.to_dict(
            orient="records"
        )


    # ========================================================
    # SEARCH BY PERSON ID
    # ========================================================

    def search_person_id(
        self,
        person_id
    ):

        result = self.persons[
            self.persons[
                "Person_ID"
            ].astype(str)
            == str(person_id)
        ]

        return result.to_dict(
            orient="records"
        )


    # ========================================================
    # SEARCH BY PHONE
    # ========================================================

    def search_phone(
        self,
        phone
    ):

        result = self.persons[
            self.persons[
                "Phone"
            ].astype(str)
            == str(phone)
        ]

        return result.to_dict(
            orient="records"
        )


    # ========================================================
    # SEARCH CASES
    # ========================================================

    def search_cases(self, query):

        query = str(
            query
        ).strip().lower()

        if not query:

            return []

        mask = (
            self.cases
            .astype(str)
            .apply(
                lambda column:
                column.str.lower()
                .str.contains(
                    query,
                    na=False
                )
            )
            .any(axis=1)
        )

        return self.cases[
            mask
        ].to_dict(
            orient="records"
        )


    # ========================================================
    # GLOBAL SEARCH
    # ========================================================

    def global_search(self, query):

        return {

            "persons":
                self.search_persons(
                    query
                ),

            "cases":
                self.search_cases(
                    query
                )
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    engine = SearchEngine()

    print(
        engine.global_search(
            "P001"
        )
    )