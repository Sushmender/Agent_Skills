"""
Display utilities for Google ADK events.

Handles formatting of agent messages, tool calls, and subagent activity
for a readable terminal experience.
"""


def truncate(text: str, max_length: int = 120) -> str:
    """Truncate a string to max_length, appending '...' if needed."""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def display_event(event) -> None:
    """
    Display a single ADK runner event in a readable format.

    Handles:
    - Function/tool calls (shown with 🔧)
    - Intermediate agent text (shown with 💭)
    - Final responses (shown as bold Agent output)
    """
    author = getattr(event, "author", "unknown")

    # Color-code by author: main orchestrator vs subagents
    if author == "orchestrator":
        label = "\033[36m[Main]\033[0m"
    else:
        label = f"\033[35m[{author}]\033[0m"

    # Show tool/function calls
    if hasattr(event, "get_function_calls"):
        for fc in event.get_function_calls():
            args_str = truncate(str(fc.args))
            print(f"{label} 🔧 \033[1m{fc.name}\033[0m")
            print(f"   Input: {args_str}")

    # Show final response text (the agent's answer to the user)
    if event.is_final_response():
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print(f"\033[1mAgent\033[0m: {part.text}\n")
        return

    # Show intermediate text (agent reasoning / subagent output mid-flight)
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and part.text.strip():
                preview = truncate(part.text.strip(), 200)
                print(f"{label} 💭 {preview}")
