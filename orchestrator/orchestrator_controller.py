from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.coder_agent import CoderAgent
from agents.critic_agent import CriticAgent
<<<<<<< HEAD
import re
=======
from agents.base_agent import BaseAgent
import re
import json
>>>>>>> 9640e9d (Updated code)

class Orchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.research = ResearchAgent()
        self.coder = CoderAgent()
        self.critic = CriticAgent()
<<<<<<< HEAD

    # Only generate code if user EXPLICITLY asks
    def is_code_task(self, goal):
        keywords = ["code", "program", "logic", "script", "implementation"]
        return any(word in goal.lower() for word in keywords)

    # HARD REMOVE EVERYTHING THAT LOOKS LIKE CODE
    def remove_code_completely(self, text):
        # Remove fenced code blocks
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

        # Remove inline code
        text = re.sub(r"`.*?`", "", text)

        # Remove Python / Java patterns
        code_patterns = [
            r"(?m)^.*def .*",
            r"(?m)^.*class .*",
            r"(?m)^.*import .*",
            r"(?m)^.*public .*",
            r"(?m)^.*static .*",
            r"(?m)^.*if __name__.*",
            r"(?m)^.*print\(.*",
            r"(?m)^.*;.*",
            r"\{.*?\}",
        ]

        for pattern in code_patterns:
            text = re.sub(pattern, "", text)

        # Remove extra empty lines
        text = "\n".join(line for line in text.splitlines() if line.strip())

        return text.strip()
=======
        
        # Initialize a router agent to classify intent
        router_prompt = (
            "You are an intent classification engine. Analyze the user's request semantically "
            "and classify it into exactly one of the following categories: "
            "'coding', 'explanation', 'research', 'planning', 'debugging'.\n\n"
            "Respond ONLY with a valid JSON object in the following format, without markdown blocks:\n"
            '{"intent": "<category>", "confidence": <float between 0 and 1>}\n\n'
            "Categories meaning:\n"
            "- 'coding': EXPLICITLY software development, programming, implementation, algorithm design, API creation, or script generation.\n"
            "- 'explanation': Explaining concepts, general Q&A, recommendations, ideas.\n"
            "- 'research': Information gathering, comparing technologies, fact-finding.\n"
            "- 'planning': Step-by-step guidance, project architecture, startup steps, business advice, career guidance, wedding suggestions, travel suggestions.\n"
            "- 'debugging': Fixing errors, reviewing code, solving exceptions, code review.\n\n"
            "CRITICAL: Non-coding queries (wedding suggestions, travel ideas, recommendations, general Q&A) MUST NOT be classified as 'coding'. "
            "Code should ONLY be generated when the user's intent is explicitly software development."
        )
        self.router = BaseAgent(role_prompt=router_prompt)

    def detect_intent_and_confidence(self, goal):
        """
        Uses an LLM-based classifier to determine the user's intent and confidence score.
        Returns a tuple: (intent (str), confidence (float))
        """
        response_text = self.router.think(goal).strip()
        
        # In case the LLM wraps it in markdown, remove it
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        
        try:
            data = json.loads(response_text)
            intent = data.get("intent", "research").lower()
            confidence = float(data.get("confidence", 0.0))
        except (json.JSONDecodeError, ValueError):
            # Fallback if LLM fails to return valid JSON
            intent = "research"
            confidence = 0.0
            
        valid_intents = ["coding", "explanation", "research", "planning", "debugging"]
        if intent not in valid_intents:
            intent = "research"
            
        return intent, confidence

    def contains_code(self, text):
        """
        Detects if a string contains source code patterns.
        """
        code_patterns = [
            r"```[a-zA-Z]*\n[\s\S]*?```",  # Markdown code blocks
            r"(?m)^\s*def \w+\(.*\):",     # Python function
            r"(?m)^\s*class \w+.*:",       # Python/Java/JS class
            r"(?m)^\s*import [a-zA-Z0-9_\.]+", # Import statements
            r"(?m)^\s*public class ",      # Java class
            r"(?m)^\s*public static ",     # Java static method
            r"(?m)^\s*if __name__\s*==\s*['\"]__main__['\"]:", # Python main
            r"(?m)^\s*function \w+\(.*\)\s*\{", # JS function
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, text):
                return True
        return False
>>>>>>> 9640e9d (Updated code)

    def run(self, goal):
        print("\n🎯 USER TASK:", goal)

<<<<<<< HEAD
        research = self.research.run(goal)

        # CODE MODE (ONLY IF USER ASKED)
        if self.is_code_task(goal):
            result = self.coder.think(goal)

        # TEXT MODE — FORCE STEP ANSWER
        else:
            result = self.planner.think(
                f"Give ONLY steps and explanation. NEVER include code. Task: {goal}"
            )
            result = self.remove_code_completely(result)

        critique = self.critic.think(result)

        # Removed self.memory.save as memory is undefined in Orchestrator

=======
        intent, confidence = self.detect_intent_and_confidence(goal)
        print(f"🧭 DETECTED INTENT: {intent} (Confidence: {confidence})")

        research = self.research.run(goal)

        # Route task based on confidence and detected intent
        if confidence < 0.6:
            print("⚠️ Low confidence detected. Defaulting to PlannerAgent.")
            result = self.planner.think(
                f"Answer the user's task in natural language. DO NOT provide code. Task: {goal}"
            )
            
        elif intent in ["coding", "debugging"]:
            result = self.coder.think(goal)
            
        elif intent in ["planning", "explanation"]:
            result = self.planner.think(
                f"Answer the user's task in natural language. Provide recommendations and explanations. DO NOT provide code. Task: {goal}"
            )
            
        else:
            # Fallback for research intent
            result = self.planner.think(
                f"Synthesize an answer based ONLY on this research, do not include code. Task: {goal}\nResearch: {research}"
            )

        # Safety layer: verify no code in non-coding intents
        if intent not in ["coding", "debugging"] and self.contains_code(result):
            print("⚠️ Code detected in non-coding response. Regenerating as natural language...")
            result = self.planner.think(
                f"Rewrite the following text strictly as natural language. Remove any source code, functions, classes, or code blocks. Keep the core recommendations and ideas intact.\n\nText:\n{result}"
            )

        critique = self.critic.think(result)

>>>>>>> 9640e9d (Updated code)
        print("\n🌐 RESEARCH:\n", research)
        print("\n✅ FINAL ANSWER:\n", result)
        print("\n🧪 FEEDBACK:\n", critique)

        return result
