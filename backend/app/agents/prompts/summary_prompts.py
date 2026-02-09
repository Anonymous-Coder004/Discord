def summarize_prompt(existing_summary: str) -> str:
    if existing_summary:
        return (
            f"Existing summary:\n{existing_summary}\n\n"
            "Update this summary using the new messages.\n"
            "- Preserve important user-specific facts (names, preferences, decisions).\n"
            "- Do not remove previously important context unless it is contradicted.\n"
            "- Keep it concise and information-dense.\n"
        )
    return (
        "Summarize the conversation.\n"
        "- Preserve important user-specific facts.\n"
        "- Keep it concise and information-dense.\n"
    )
