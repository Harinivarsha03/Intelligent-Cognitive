from app.agent import CognitiveAgent


def main():

    agent = CognitiveAgent()

    print("========================================")
    print(" Intelligent Cognitive Assistant System ")
    print("========================================")
    print("Type 'exit' to stop the assistant.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower().strip() == "exit":

            print("Assistant: Goodbye!")
            break

        if not user_input.strip():
            continue

        result = agent.process(user_input)

        print("\nDetected Intent:", result["intent"])
        print("Assistant:", result["response"])
        print()


if __name__ == "__main__":
    main()