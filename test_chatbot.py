from voibot.chatbot import VoiAssistant

# Set up the parameters for the assistant
pdf_urls = {
    "voi_knowledge": ["https://firebasestorage.googleapis.com/v0/b/voiage-67f40.appspot.com/o/pdfs%2Fdemo%2FVoiAssistantKnowledge.pdf?alt=media"],
    "ab_inbev": ["https://www.ab-inbev.com/assets/pressreleases/2023/FY%20Financial%20Report%202022.pdf"],
    "samsung": ["https://images.samsung.com/is/content/samsung/assets/global/our-values/resource/Samsung-Electronics-Supplier-Code-of-Conduct-Guide_ver3.1.pdf"]
}

role = "You are an AI virtual assistant capable of answering questions about Voi AI, AB InBev's financial report, and Samsung's supplier code of conduct."

intents = {
    "Voi-related": "Questions about Voi AI, its features, or capabilities",
    "AB InBev-related": "Questions about AB InBev's financial report for 2022",
    "Samsung-related": "Questions about Samsung's supplier code of conduct",
    "Greeting": "Greetings like 'Hello' or 'How are you?'",
    "Other Topic": "Non-related topics",
    "Clarification": "Asking the assistant to clarify a previously given answer",
    "Follow-up Inquiry": "Follow-up question based on a previous response",
}

replies = {
    "Voi-related": "RAG",
    "AB InBev-related": "RAG",
    "Samsung-related": "RAG",
    "Greeting": "Hello! I'm an AI assistant that can help you with information about Voi AI, AB InBev's financial report, and Samsung's supplier code of conduct. How can I assist you today?",
    "Other Topic": "I'm sorry, but I'm specialized in Voi AI, AB InBev's financials, and Samsung's supplier code. I may not be able to help with that topic.",
    "Clarification": "I apologize if I wasn't clear. Let me try to clarify: {most_recent_response}",
    "Follow-up Inquiry": "Certainly, I'd be happy to provide more information. Based on what we discussed earlier: {most_recent_response}",
}

segment_assignments = {
    "Voi-related": "voi_knowledge",
    "AB InBev-related": "ab_inbev",
    "Samsung-related": "samsung",
    "Greeting": "no_segment",
    "Other Topic": "no_segment",
    "Clarification": "no_segment",
    "Follow-up Inquiry": "no_segment",
}

dont_know_response = "I'm sorry, but I don't have enough information to answer that question accurately. Could you please rephrase or ask about a different aspect of Voi AI, AB InBev's financials, or Samsung's supplier code?"

# Initialize the assistant
assistant = VoiAssistant(
    openai_key=openai_key,
    pdf_urls=pdf_urls,
    role=role,
    intents=intents,
    replies=replies,
    segment_assignments=segment_assignments,
    dont_know_response=dont_know_response
)

loading = True

assistant.initialize_assistant()

loading = False
print("\rInitialization complete!       ")

print("\nEntering interactive mode. Type 'exit' to end the conversation.")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        print("Conversation ended.")
        break
    response = assistant.get_response(user_input)
    print(f"Assistant: {response}")
