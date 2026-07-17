# agents/usda_agent.py

from agents.tools.usda_api import get_usda_data

class USDAAgent:
    """
    Smart USDA agent:
    - Auto-detects commodity categories
    - Searches multiple yield types
    - Returns best available dataset
    """

    POSSIBLE_CATEGORIES = [
        "TOMATOES, PROCESSING",
        "TOMATOES, FRESH MARKET",
        "TOMATOES, ALL",
        "CORN, GRAIN",
        "CORN, SILAGE",
        "WHEAT, WINTER",
        "WHEAT, SPRING"
    ]

    def run(self, question=None):
        crop = self.extract_crop(question)
        results = []

        for cat in self.POSSIBLE_CATEGORIES:
            if crop in cat:
                data = get_usda_data(cat)
                if data.get("results"):
                    results.append((cat, data))

        if not results:
            return {"usda": {"category": crop, "results": []}}

        # Pick the category with the most records
        best = max(results, key=lambda x: len(x[1]["results"]))
        return {"usda": {"category": best[0], "results": best[1]["results"]}}

    def extract_crop(self, question):
        if not question:
            return "TOMATOES"
        q = question.lower()
        crops = ["tomatoes", "corn", "wheat", "alfalfa", "grapes"]
        for c in crops:
            if c in q:
                return c.upper()
        return "TOMATOES"

    def speak(self, usda_data, question):
        if not usda_data["results"]:
            return "USDA Agent — no yield data available yet."

        cat = usda_data["category"]
        count = len(usda_data["results"])
        return f"USDA Agent — best match: {cat}, {count} records found."
