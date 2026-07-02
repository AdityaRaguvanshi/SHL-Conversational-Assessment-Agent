
def is_out_of_scope(text):
    banned = [
        "legal advice",
        "ignore previous instructions",
        "politics",
        "salary negotiation"
    ]

    text = text.lower()

    return any(word in text for word in banned)
