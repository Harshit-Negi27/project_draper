from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents import (
    research_logic,
    twitter_writer,
    linkedin_writer,
    facebook_writer,
    instagram_writer
)

def build_graph():
    # Initialize Graph
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("researcher", research_logic)
    workflow.add_node("twitter", twitter_writer)
    workflow.add_node("linkedin", linkedin_writer)
    workflow.add_node("facebook", facebook_writer)
    workflow.add_node("instagram", instagram_writer)

    # Define Edges
    # 1. Start -> Researcher
    workflow.set_entry_point("researcher")
    
    # 2. Researcher -> All Writers (Parallel Fan-out)
    workflow.add_edge("researcher", "twitter")
    workflow.add_edge("researcher", "linkedin")
    workflow.add_edge("researcher", "facebook")
    workflow.add_edge("researcher", "instagram")
    
    # 3. Writers -> End
    workflow.add_edge("twitter", END)
    workflow.add_edge("linkedin", END)
    workflow.add_edge("facebook", END)
    workflow.add_edge("instagram", END)

    # Compile
    return workflow.compile()