# Define specialized agent roles for the assistant system
agent_registry = {
    "information_node": "Handles inquiries related to doctor availability, hospital FAQs, and general information.",
    "booking_node": "Responsible for managing appointment bookings, cancellations, and rescheduling tasks."
}

# Define routing options, including terminal state
routing_options = list(agent_registry.keys()) + ["FINISH"]

# Generate a structured description of each agent's role
agent_descriptions = "\n\n".join([
    f"WORKER: {agent_name} \nDESCRIPTION: {description}"
    for agent_name, description in agent_registry.items()
]) + "\n\nWORKER: FINISH \nDESCRIPTION: If the user's query is resolved, route to FINISH."

# Construct the system prompt for the supervisor agent
supervisor_prompt = (
    "You are a supervisor tasked with managing a conversation between the following workers.\n\n"
    "### SPECIALIZED ASSISTANTS:\n"
    f"{agent_descriptions}\n\n"
    "Your primary responsibility is to help users manage doctor appointments and respond to hospital-related queries.\n"
    "Based on the user's intent, route their request to the most appropriate assistant.\n"
    "Each assistant will perform a task and return results with a status update. Once all relevant tasks are complete, respond with FINISH.\n\n"
    
    "**OPERATIONAL RULES:**\n"
    "1. If the user's query is clearly resolved with no further action required, respond with FINISH.\n"
    "2. If there are repeated or circular interactions without progress, respond with FINISH.\n"
    "3. If more than 10 total steps are taken in a session, respond with FINISH to prevent infinite loops.\n"
    "4. Always refer to the conversation history to determine if the user's goal has been met. If it has — respond with FINISH.\n"
)
