from fastapi import FastAPI
from pydantic import BaseModel
from agent import DoctorAppointmentAgent
from langchain_core.messages import HumanMessage
import os

# Remove environment variable that may cause SSL issues
os.environ.pop("SSL_CERT_FILE", None)

# Initialize FastAPI app
app = FastAPI(title="Doctor Appointment Agentic API")

# Pydantic model to structure incoming request
class UserInput(BaseModel):
    id_number: int
    query: str

# Initialize the agent
appointment_agent = DoctorAppointmentAgent()

@app.post("/execute")
def run_agent(user_input: UserInput):
    # Build the workflow
    agent_workflow = appointment_agent.workflow()

    # Prepare the initial state for the agent
    initial_state = {
        "messages": [HumanMessage(content=user_input.query)],
        "id_number": user_input.id_number,
        "next": "",
        "query": "",
        "current_reasoning": "",
    }

    # Execute the workflow
    result = agent_workflow.invoke(initial_state, config={"recursion_limit": 20})
    
    return {"messages": result["messages"]}
