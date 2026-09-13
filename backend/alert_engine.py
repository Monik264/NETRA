import pandas as pd

try:
    from .data_loader import load_all_data
    from .config import (
        HIGH_TRANSACTION_MULTIPLIER,
        REPEATED_CALL_THRESHOLD
    )
except ImportError:
    from data_loader import load_all_data
    from config import (
        HIGH_TRANSACTION_MULTIPLIER,
        REPEATED_CALL_THRESHOLD
    )


# ============================================================
# ALERT ENGINE
# ============================================================

class AlertEngine:

    def __init__(self):

        (
            self.persons,
            self.calls,
            self.transactions,
            self.cases
        ) = load_all_data()


    # ========================================================
    # REPEATED CALLS
    # ========================================================

    def repeated_calls(self):

        counts = (
            self.calls
            .groupby(
                ["Caller", "Receiver"]
            )
            .size()
            .reset_index(
                name="Call_Count"
            )
        )

        alerts = counts[
            counts["Call_Count"]
            >= REPEATED_CALL_THRESHOLD
        ].copy()

        alerts["Alert_Type"] = (
            "Repeated Communication"
        )

        alerts["Severity"] = (
            alerts["Call_Count"]
            .apply(
                lambda x:
                "HIGH"
                if x >= 5
                else "MEDIUM"
            )
        )

        return alerts


    # ========================================================
    # LARGE TRANSACTIONS
    # ========================================================

    def large_transactions(self):

        if self.transactions.empty:

            return pd.DataFrame()

        average = (
            self.transactions[
                "Amount"
            ].mean()
        )

        threshold = (
            average
            * HIGH_TRANSACTION_MULTIPLIER
        )

        alerts = self.transactions[
            self.transactions[
                "Amount"
            ] > threshold
        ].copy()

        alerts["Alert_Type"] = (
            "Unusual Transaction"
        )

        alerts["Severity"] = (
            "HIGH"
        )

        alerts["Threshold"] = (
            threshold
        )

        return alerts


    # ========================================================
    # PERSON ALERTS
    # ========================================================

    def person_alerts(self, person_id):

        person_id = str(person_id)

        alerts = []

        repeated = self.repeated_calls()

        for _, row in repeated.iterrows():

            if (
                str(row["Caller"])
                == person_id
                or
                str(row["Receiver"])
                == person_id
            ):

                alerts.append({

                    "Alert_Type":
                        "Repeated Communication",

                    "Severity":
                        row["Severity"],

                    "Description":
                        (
                            f'{row["Call_Count"]} calls '
                            f'between {row["Caller"]} '
                            f'and {row["Receiver"]}'
                        )
                })


        large = self.large_transactions()

        for _, row in large.iterrows():

            if (
                str(row["Sender"])
                == person_id
                or
                str(row["Receiver"])
                == person_id
            ):

                alerts.append({

                    "Alert_Type":
                        "Unusual Transaction",

                    "Severity":
                        "HIGH",

                    "Description":
                        (
                            f'Transaction of '
                            f'₹{row["Amount"]}'
                        )
                })


        return alerts


    # ========================================================
    # ALL ALERTS
    # ========================================================

    def all_alerts(self):

        alerts = []

        repeated = self.repeated_calls()

        for _, row in repeated.iterrows():

            alerts.append({

                "Alert_Type":
                    "Repeated Communication",

                "Severity":
                    row["Severity"],

                "Source":
                    row["Caller"],

                "Target":
                    row["Receiver"],

                "Value":
                    int(row["Call_Count"])
            })


        large = self.large_transactions()

        for _, row in large.iterrows():

            alerts.append({

                "Alert_Type":
                    "Unusual Transaction",

                "Severity":
                    "HIGH",

                "Source":
                    row["Sender"],

                "Target":
                    row["Receiver"],

                "Value":
                    float(row["Amount"])
            })


        return alerts


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    engine = AlertEngine()

    print("=" * 60)
    print("ALERT ENGINE")
    print("=" * 60)

    print()

    alerts = engine.all_alerts()

    for alert in alerts:

        print(alert)