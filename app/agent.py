from ollama import chat
from app.tools import calculator, get_weather
from app.memory import ConversationMemory


class CognitiveAgent:

    def __init__(self):
        self.name = "Intelligent Cognitive Assistant"
        self.model = "llama3.2"
        self.memory = ConversationMemory()

    # -----------------------------------
    # AI SYSTEM PROMPT
    # -----------------------------------

    SYSTEM_PROMPT = """
You are an Intelligent Cognitive Assistant powered by Llama 3.2.

You are a general-purpose AI assistant.

You can help the user with:

- General knowledge
- Programming
- Python
- SQL
- Data science
- Machine learning
- Artificial intelligence
- Mathematics
- Science
- Technology
- Education
- Interview preparation
- Career guidance
- Writing
- Rewriting
- Summarization
- Brainstorming
- Problem solving
- Step-by-step explanations
- Project ideas
- Study plans
- Everyday questions
- Conversation

IMPORTANT BEHAVIOR:

1. Answer the user's actual question directly.

2. Do not say that you can only answer a limited number of topics.

3. If the user asks for an explanation, explain it clearly.

4. If the user asks "how to", give step-by-step instructions.

5. If the user asks for code, provide useful working code and explain it.

6. If the user is learning something, explain it in beginner-friendly language.

7. If the question is complex, break it into smaller parts.

8. Use previous conversation context when it is relevant.

9. Do not invent live information.

10. Be helpful, clear and natural.

11. Keep simple answers concise, but provide more detail when the user asks for detailed information.

12. You are the main conversational intelligence of the application.
"""

    # -----------------------------------
    # INTENT DETECTION
    # -----------------------------------

    def detect_intent(self, user_input):

        text = user_input.lower().strip()

        # -----------------------------------
        # WEATHER
        # -----------------------------------

        weather_keywords = [
            "weather",
            "temperature",
            "rain",
            "rainfall",
            "humidity",
            "wind",
            "forecast",
            "climate",
            "hot today",
            "cold today"
        ]

        if any(word in text for word in weather_keywords):
            return "WEATHER_REQUEST"

        # -----------------------------------
        # CONTEXT WEATHER
        # -----------------------------------

        context_weather_phrases = [
            "what about",
            "how about",
            "is it hot",
            "is it cold",
            "will it rain",
            "how is it"
        ]

        if any(phrase in text for phrase in context_weather_phrases):

            history = self.memory.get_history()

            for message in reversed(history):

                if message["role"] == "user":

                    previous_text = message["content"].lower()

                    if any(
                        word in previous_text
                        for word in weather_keywords
                    ):
                        return "WEATHER_REQUEST"

        # -----------------------------------
        # CALCULATION
        # -----------------------------------

        calculation_keywords = [
            "calculate",
            "what is",
            "how much is",
            "plus",
            "minus",
            "multiply",
            "divided by",
            "divide",
            "sum of",
            "add",
            "subtract",
            "percentage of",
            "percent of"
        ]

        # Only treat obvious mathematical expressions as calculations.
        math_symbols = ["+", "-", "*", "/", "%"]

        has_math_symbol = any(
            symbol in text
            for symbol in math_symbols
        )

        has_calculation_word = any(
            word in text
            for word in calculation_keywords
        )

        # Don't route every "what is..." question to calculator.
        if has_math_symbol or (
            has_calculation_word
            and any(char.isdigit() for char in text)
        ):
            return "CALCULATION"

        # -----------------------------------
        # GREETING
        # -----------------------------------

        greeting_keywords = [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "thank you",
            "thanks",
            "okk",
            "okay"
        ]

        if any(
            text == word or text.startswith(word + " ")
            for word in greeting_keywords
        ):
            return "GREETING"

        # -----------------------------------
        # IDENTITY
        # -----------------------------------

        identity_keywords = [
            "who are you",
            "what are you",
            "your name",
            "tell me about yourself"
        ]

        if any(word in text for word in identity_keywords):
            return "IDENTITY"

        # -----------------------------------
        # GENERAL QUESTION
        # -----------------------------------

        # Everything else goes directly to Llama.
        return "GENERAL_QUESTION"

    # -----------------------------------
    # LLM WITH MEMORY
    # -----------------------------------

    def ask_llm(self, user_input):

        history = self.memory.get_history()

        messages = [
            {
                "role": "system",
                "content": self.SYSTEM_PROMPT
            }
        ]

        # Add previous conversation
        messages.extend(history)

        # Add current user message
        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        response = chat(
            model=self.model,
            messages=messages
        )

        return response["message"]["content"]

    # -----------------------------------
    # CALCULATOR
    # -----------------------------------

    def handle_calculation(self, user_input):

        expression_prompt = f"""
Extract only the mathematical expression from this request.

User:
{user_input}

Rules:

- Return ONLY the mathematical expression.
- Do not explain.
- Do not include words.

Examples:

User: Calculate 25 * 4

Return:
25 * 4

User: What is 100 + 50?

Return:
100 + 50

User: Calculate 500 / 10

Return:
500 / 10
"""

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": expression_prompt
                }
            ]
        )

        expression = response["message"]["content"].strip()

        result = calculator(expression)

        return f"The answer is {result}."

    # -----------------------------------
    # WEATHER
    # -----------------------------------

    def handle_weather(self, user_input):

        history = self.memory.get_history()

        city_prompt = f"""
Extract the city name from the user's weather request.

User:
{user_input}

Previous conversation:
{history}

Rules:

1. Return ONLY the city name.
2. If the user says "what about Chennai", return Chennai.
3. If the user asks about a city directly, return that city.
4. Do not return explanations.
"""

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": city_prompt
                }
            ]
        )

        city = response["message"]["content"].strip()

        weather = get_weather(city)

        if isinstance(weather, dict):

            return (
                f"Current weather in {weather['city']}: "
                f"{weather['temperature']}°C, "
                f"humidity {weather['humidity']}%, "
                f"wind speed {weather['wind_speed']} km/h."
            )

        return weather

    # -----------------------------------
    # MAIN AGENT
    # -----------------------------------

    def process(self, user_input):

        intent = self.detect_intent(user_input)

        # -----------------------------------
        # WEATHER
        # -----------------------------------

        if intent == "WEATHER_REQUEST":

            response = self.handle_weather(user_input)

        # -----------------------------------
        # CALCULATION
        # -----------------------------------

        elif intent == "CALCULATION":

            response = self.handle_calculation(user_input)

        # -----------------------------------
        # IDENTITY
        # -----------------------------------

        elif intent == "IDENTITY":

            response = self.ask_llm(user_input)

        # -----------------------------------
        # GREETING
        # -----------------------------------

        elif intent == "GREETING":

            response = self.ask_llm(user_input)

        # -----------------------------------
        # EVERYTHING ELSE
        # -----------------------------------

        else:

            response = self.ask_llm(user_input)

        # -----------------------------------
        # SAVE USER MESSAGE
        # -----------------------------------

        self.memory.add_message(
            "user",
            user_input
        )

        # -----------------------------------
        # SAVE ASSISTANT RESPONSE
        # -----------------------------------

        self.memory.add_message(
            "assistant",
            response
        )

        # -----------------------------------
        # RETURN RESULT
        # -----------------------------------

        return {
            "intent": intent,
            "response": response
        }