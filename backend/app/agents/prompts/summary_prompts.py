def summarize_prompt(existing_summary: str) -> str:
    if existing_summary:
        return (
            f"Existing summary:\n{existing_summary}\n\n"
            "Update and extend the summary using the new conversation."
        )
    return "Summarize the following conversation concisely."
