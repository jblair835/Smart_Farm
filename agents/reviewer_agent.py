# agents/reviewer_agent.py

class ReviewerAgent:
    """
    Ivy reviews decisions for contradictions or missing logic.
    """

    def run(self, decisions):
        issues = []

        # Check contradictions
        if decisions["pesticide"]["should_spray"] and decisions["pesticide"]["timing"] is None:
            issues.append("Pesticide spraying approved but no timing provided.")

        if decisions["fertilizer"]["should_apply"] and decisions["fertilizer"]["timing"] is None:
            issues.append("Fertilizer application approved but no timing provided.")

        # Check risk alignment
        if decisions["pesticide"]["should_spray"] and "wind" in decisions["pesticide"]["reason"].lower():
            issues.append("Pesticide spraying approved despite wind risk.")

        return {"issues": issues}

    def speak(self, issues):
        if not issues:
            return "Inspector Ivy reporting — everything checks out."
        return "Inspector Ivy reporting — issues detected:\n" + "\n".join(f"• {i}" for i in issues)
