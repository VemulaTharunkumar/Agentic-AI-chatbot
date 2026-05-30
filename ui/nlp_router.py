<<<<<<< HEAD
# nlp_router.py
# Central NLP Intent Router for Agent Selection
# Rule-based + Extendable (ML / Embeddings ready)

import re

CODE_KEYWORDS = [
    "code", "program", "python", "java", "script", "algorithm",
    "compile", "function", "class", "logic"
]

RESEARCH_KEYWORDS = [
    "latest", "news", "research", "study", "source", "trend", "paper", "report"
]

REVIEW_KEYWORDS = [
    "review", "evaluate", "feedback", "rate", "critic", "analysis"
]

GREETING_PATTERNS = [
    # Simple greetings
    r"^hi$", r"^hello$", r"^hey$", r"^yo$", r"^sup$",
    r"^hii+$", r"^heyy+$",

    # Time-based greetings
    r"^good morning$", r"^good afternoon$", r"^good evening$", r"^good night$",

    # Polite greetings
    r"^hello there$", r"^hey there$", r"^hi there$",

    # How-are-you style
    r"^how are you$", r"^how r u$", r"^how are you doing$",
    r"^how's it going$", r"^how is it going$",
    r"^what's up$", r"^wassup$", r"^what up$",

    # Friendly / casual chat
    r"^nice to meet you$", r"^pleased to meet you$",
    r"^good to see you$", r"^long time no see$",

    # Bot-specific greetings
    r"^hey bot$", r"^hello bot$", r"^hi bot$",

    # Multiple words / casual typing
    r"^hi everyone$", r"^hello everyone$",
    r"^hey buddy$", r"^hey friend$"
]



def detect_intent(text: str) -> str:
    """
    Returns one of:
    GREETING, CODE, RESEARCH, REVIEW, GENERAL
    """
    text = text.lower().strip()

    if any(word in text for word in GREETING_PATTERNS):
        return "RESEARCH"

    # Code intent
    if any(word in text for word in CODE_KEYWORDS):
        return "CODE"

    # Research intent
    if any(word in text for word in RESEARCH_KEYWORDS):
        return "RESEARCH"

    # Review intent
    if any(word in text for word in REVIEW_KEYWORDS):
        return "REVIEW"

    return "GENERAL"


def select_agents(intent: str):
    """
    Decide which agents to run based on intent
    """

=======
import json
import re
import sys
import os

# Add project root to path so we can import agents
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.base_agent import BaseAgent

router_prompt = """
You are a semantic intent classifier. Analyze the full meaning and context of the user request.
Classify the request into exactly one of these intents:
- GREETING: Simple hellos, pleasantries, asking how the bot is doing.
- CODE: Writing code, programming, debugging scripts, implementing features, fixing exceptions.
- RESEARCH: Fact finding, comparing technologies, searching for news, gathering information.
- REVIEW: Reviewing architecture, giving feedback on designs or systems.
- GENERAL: General advice, planning, unrelated topics (e.g., wedding colors, travel, general planning).

Respond ONLY with a valid JSON object in this format, without any markdown formatting:
{"intent": "<INTENT_NAME>", "confidence": <float>}
"""

router_agent = BaseAgent(role_prompt=router_prompt)

def detect_intent(text: str):
    """
    Returns a tuple of (intent, confidence)
    intent is one of: GREETING, CODE, RESEARCH, REVIEW, GENERAL
    """
    response_text = router_agent.think(text).strip()
    
    # Clean up markdown if the LLM adds it
    response_text = re.sub(r'```json\s*', '', response_text)
    response_text = re.sub(r'```\s*', '', response_text)
    
    try:
        data = json.loads(response_text)
        intent = data.get("intent", "GENERAL").upper()
        confidence = float(data.get("confidence", 0.0))
    except (json.JSONDecodeError, ValueError):
        intent = "GENERAL"
        confidence = 0.0
        
    valid_intents = ["GREETING", "CODE", "RESEARCH", "REVIEW", "GENERAL"]
    if intent not in valid_intents:
        intent = "GENERAL"
        
    # If confidence is below threshold, route to GENERAL
    if confidence < 0.6:
        intent = "GENERAL"
        
    return intent, confidence

def select_agents(intent: str):
    """
    Decide which agents to run based on semantic intent
    """
>>>>>>> 9640e9d (Updated code)
    if intent == "GREETING":
        return ["research"]

    if intent == "CODE":
        return ["planner", "research", "coder", "critic"]

    if intent == "RESEARCH":
        return ["planner", "research", "critic"]

    if intent == "REVIEW":
        return ["planner", "critic"]

    # GENERAL
    return ["research"]
