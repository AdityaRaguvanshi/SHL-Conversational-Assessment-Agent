def detect_intent(messages):
    latest = messages[-1]["content"].lower()

    comparison_words = [
        "difference",
        "compare",
        "vs",
        "versus"
    ]

    refinement_words = [
        "add",
        "include",
        "also",
        "instead",
        "actually"
    ]

    # comparison intent
    if any(word in latest for word in comparison_words):
        return "comparison"

    # refinement intent
    if any(word in latest for word in refinement_words):
        return "refinement"

    # clarification only if TOO vague
    vague_inputs = [
        "assessment",
        "test",
        "hiring",
        "need assessment"
    ]

    if latest.strip() in vague_inputs:
        return "clarify"

    # otherwise recommend
    return "recommend"


def clarification_question():
    return (
        "Could you share the role, seniority level, "
        "and whether you want technical, cognitive, "
        "or personality assessments?"
    )