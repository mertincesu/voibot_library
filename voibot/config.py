# Default OpenAI API model to use
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"

# Default temperature for OpenAI API responses
DEFAULT_TEMPERATURE = 0.9

# Default max tokens for responses
DEFAULT_MAX_TOKENS = 150

# Default role for the assistant (this can be overridden by user)
DEFAULT_ROLE = "Voi AI Assistant, for answering questions related to Voi AI and its products."

# Default categories/classes for classification
DEFAULT_CLASSES = {
    "Company-related": "Questions about Voi AI and its products (VoiBot, etc.).",
    "Assistant-related": "Questions about the assistant, such as 'What do you know?' or 'Who are you?'",
    "Greeting": "Friendly greetings like 'Hey' or 'How are you?'",
    "Other Topic": "Questions that are unrelated to the assistant or company.",
    "Not Understandable Word/Phrase": "Gibberish or nonsensical input."
}

# Default automatic replies for each category
DEFAULT_AUTOMATIC_REPLIES = {
    "Company-related": "I can provide information related to Voi AI and its products. Let me know if you need any specifics.",
    "Assistant-related": "I am VoiBot, a virtual assistant here to help you with any questions about Voi AI and its offerings.",
    "Greeting": "Hello, I'm here to help. How can I assist you today?",
    "Other Topic": "I'm not sure I can help with that topic. Please ask something related to Voi AI.",
    "Not Understandable Word/Phrase": "I'm sorry, I didn't quite understand that. Could you try asking again?"
}

# Default segment assignments for each category (used for knowledge retrieval)
DEFAULT_SEGMENT_ASSIGNMENTS = {
    "Company-related": "unified",
    "Assistant-related": "unified",
    "Greeting": "unified",
    "Other Topic": "unified",
    "Not Understandable Word/Phrase": "unified"
}
