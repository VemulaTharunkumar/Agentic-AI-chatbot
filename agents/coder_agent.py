from agents.base_agent import BaseAgent

class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__(
<<<<<<< HEAD
            "Write ONLY executable code. NO explanation text."
=======
            "You are an expert software engineer.\n"
            "Write the code necessary to solve the user's task using markdown code blocks.\n"
            "FORMATTING RULES:\n"
            "1. Explain your logic briefly before the code.\n"
            "2. Explain how to run or use it after the code.\n"
            "3. Use code blocks (```) ONLY for the code itself.\n"
            "4. Highlight critical words using Markdown (**bold**).\n"
            "5. Use headings and bullet points to avoid walls of text."
>>>>>>> 9640e9d (Updated code)
        )
