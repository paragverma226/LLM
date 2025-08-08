from typing import Literal, List, Any
from typing_extensions import TypedDict, Annotated

from langchain_core.tools import tool
from langgraph.types import Command
from langgraph.graph.message import add_messages
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

from prompt_library.prompt import system_prompt
from utils.llms import LanguageModel
from toolkit.toolkits import (
    check_availability_by_doctor,
    check_availability_by_specialization,
    set_appointment,
    cancel_appointment,
    reschedule_appointment
)


# === State Definitions ===

class RoutingDecision(TypedDict):
    next: Literal["information_node", "booking_node", "FINISH"]
    reasoning: str

class AgentContext(TypedDict):
    messages: Annotated[List[Any], add_messages]
    id_number: int
    next: str
    query: str
    current_reasoning: str


# === Main Agent Class ===

class DoctorAppointmentAgent:
    """
    A multi-agent system to manage doctor availability queries and appointment bookings.
    """

    def __init__(self):
        self.llm = LanguageModel().get_model()

    def supervisor_node(self, context: AgentContext) -> Command[Literal["information_node", "booking_node", "__end__"]]:
        print("🧠 Entered supervisor_node with state:")
        print(context)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User's identification number is {context['id_number']}"},
        ] + context["messages"]

        user_query = context["messages"][0].content if len(context["messages"]) == 1 else ""

        print("📨 Compiled messages:")
        print(messages)

        print("❓ Query extracted:")
        print(user_query)

        decision = self.llm.with_structured_output(RoutingDecision).invoke(messages)

        next_step = decision["next"]
        if next_step == "FINISH":
            next_step = END

        print("🔀 Routing decision:")
        print(next_step)
        print("💬 Reasoning:", decision["reasoning"])

        update = {
            "next": next_step,
            "current_reasoning": decision["reasoning"]
        }

        if user_query:
            update["query"] = user_query
            update["messages"] = [HumanMessage(content=f"User's identification number is {context['id_number']}")]

        return Command(goto=next_step, update=update)

    def information_node(self, context: AgentContext) -> Command[Literal["supervisor"]]:
        print("📚 Entered information_node")

        info_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are an assistant that answers FAQs or doctor availability queries. "
             "Always consider the year to be 2024."),
            ("placeholder", "{messages}"),
        ])

        info_agent = create_react_agent(
            model=self.llm,
            tools=[check_availability_by_doctor, check_availability_by_specialization],
            prompt=info_prompt
        )

        result = info_agent.invoke(context)

        return Command(
            update={
                "messages": context["messages"] + [
                    AIMessage(content=result["messages"][-1].content, name="information_node")
                ]
            },
            goto="supervisor"
        )

    def booking_node(self, context: AgentContext) -> Command[Literal["supervisor"]]:
        print("📅 Entered booking_node")

        booking_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You manage appointments: setting, rescheduling, or canceling. "
             "Always consider the year to be 2024."),
            ("placeholder", "{messages}"),
        ])

        booking_agent = create_react_agent(
            model=self.llm,
            tools=[set_appointment, cancel_appointment, reschedule_appointment],
            prompt=booking_prompt
        )

        result = booking_agent.invoke(context)

        return Command(
            update={
                "messages": context["messages"] + [
                    AIMessage(content=result["messages"][-1].content, name="booking_node")
                ]
            },
            goto="supervisor"
        )

    def build_graph(self):
        """
        Constructs and compiles the multi-agent graph.
        """
        workflow = StateGraph(AgentContext)
        workflow.add_node("supervisor", self.supervisor_node)
        workflow.add_node("information_node", self.information_node)
        workflow.add_node("booking_node", self.booking_node)
        workflow.add_edge(START, "supervisor")
        self.app = workflow.compile()
        return self.app
