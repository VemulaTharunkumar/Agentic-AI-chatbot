from agents.base_agent import BaseAgent

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
<<<<<<< HEAD
            "Provide short factual research summary. NO code."
=======
            "Provide short factual research summaries in natural language ONLY. "
            "You are strictly forbidden from writing any source code, scripts, or programming language syntax."
>>>>>>> 9640e9d (Updated code)
        )

    def run(self, topic):
        return self.think(topic)
