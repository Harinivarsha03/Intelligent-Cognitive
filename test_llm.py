from ollama import chat


response = chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Explain Python in one simple sentence."
        }
    ]
)

print(response["message"]["content"])