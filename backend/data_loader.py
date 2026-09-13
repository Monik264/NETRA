import pandas as pd

try:
    from .config import (
        PERSONS_FILE,
        CALLS_FILE,
        TRANSACTIONS_FILE,
        CASES_FILE
    )
except ImportError:
    from config import (
        PERSONS_FILE,
        CALLS_FILE,
        TRANSACTIONS_FILE,
        CASES_FILE
    )


# ============================================================
# DATA LOADER
# ============================================================

class DataLoader:

    def __init__(self):

        self.persons = None
        self.calls = None
        self.transactions = None
        self.cases = None

        self.load_all()


    # ========================================================
    # LOAD ALL DATA
    # ========================================================

    def load_all(self):

        self.persons = pd.read_csv(
            PERSONS_FILE
        )

        self.calls = pd.read_csv(
            CALLS_FILE
        )

        self.transactions = pd.read_csv(
            TRANSACTIONS_FILE
        )

        self.cases = pd.read_csv(
            CASES_FILE
        )

        return self


    # ========================================================
    # GETTERS
    # ========================================================

    def get_persons(self):

        return self.persons.copy()


    def get_calls(self):

        return self.calls.copy()


    def get_transactions(self):

        return self.transactions.copy()


    def get_cases(self):

        return self.cases.copy()


    # ========================================================
    # SUMMARY
    # ========================================================

    def summary(self):

        return {
            "persons": len(self.persons),
            "calls": len(self.calls),
            "transactions": len(self.transactions),
            "cases": len(self.cases)
        }


# ============================================================
# SHARED LOADER
# ============================================================

_loader = None


def get_loader():

    global _loader

    if _loader is None:
        _loader = DataLoader()

    return _loader


def load_all_data():

    loader = get_loader()

    return (
        loader.get_persons(),
        loader.get_calls(),
        loader.get_transactions(),
        loader.get_cases()
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    try:

        loader = DataLoader()

        print("=" * 60)
        print("CRIMEGRAPH AI DATA LOADER")
        print("=" * 60)

        print()

        summary = loader.summary()

        print("Persons      :", summary["persons"])
        print("Calls        :", summary["calls"])
        print("Transactions :", summary["transactions"])
        print("Cases        :", summary["cases"])

        print()
        print("DATA LOADED SUCCESSFULLY")

    except Exception as e:

        print("ERROR:")
        print(e)