try:
    from .entity_engine import EntityEngine
    from .alert_engine import AlertEngine
    from .case_engine import CaseEngine
    from .risk_engine import RiskEngine
    from .graph_engine import CrimeGraph
except ImportError:
    from entity_engine import EntityEngine
    from alert_engine import AlertEngine
    from case_engine import CaseEngine
    from risk_engine import RiskEngine
    from graph_engine import CrimeGraph


# ============================================================
# INVESTIGATION ENGINE
# ============================================================

class InvestigationEngine:

    def __init__(self):

        self.entities = EntityEngine()

        self.alerts = AlertEngine()

        self.cases = CaseEngine()

        self.risk = RiskEngine()

        self.graph = CrimeGraph()


    # ========================================================
    # COMPLETE PERSON INVESTIGATION
    # ========================================================

    def investigate_person(
        self,
        person_id
    ):

        person_id = str(
            person_id
        )

        profile = (
            self.entities
            .get_profile(
                person_id
            )
        )

        if profile is None:

            return None


        connections = (
            self.graph
            .get_connections(
                person_id
            )
        )


        alerts = (
            self.alerts
            .person_alerts(
                person_id
            )
        )


        risk = (
            self.risk
            .calculate_score(
                person_id
            )
        )


        cases = [
            case
            for case in self.cases.get_all_cases()
            if str(case["Person_ID"])
            == person_id
        ]


        return {

            "entity":
                profile,

            "connections":
                connections,

            "alerts":
                alerts,

            "risk":
                risk,

            "cases":
                cases
        }


    # ========================================================
    # PATH BETWEEN TWO PEOPLE
    # ========================================================

    def investigate_connection(
        self,
        person1,
        person2
    ):

        path = (
            self.graph
            .shortest_path(
                person1,
                person2
            )
        )

        common = (
            self.graph
            .common_connections(
                person1,
                person2
            )
        )

        return {

            "source":
                str(person1),

            "target":
                str(person2),

            "shortest_path":
                path,

            "common_connections":
                common
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    engine = InvestigationEngine()

    result = (
        engine
        .investigate_person(
            "P001"
        )
    )

    print(result)