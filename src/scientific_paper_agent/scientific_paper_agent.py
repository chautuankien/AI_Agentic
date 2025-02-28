import asyncio
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.scientific_paper_agent.utils.state import AgentState
from src.scientific_paper_agent.utils.nodes import *
from src.scientific_paper_agent.utils.utils import print_stream


# Initialize state graph
workflow = StateGraph(AgentState)

# Add nodes to the graph
workflow.add_node("decision_making", decision_making_node)
workflow.add_node("planning", planning_node)
workflow.add_node("tools", tools_node)
workflow.add_node("agent", agent_node)
workflow.add_node("judge", judge_node)

# Set entry point of the graph
workflow.set_entry_point("decision_making")

# Add edges between nodes
workflow.add_conditional_edges(
    "decision_making",
    router,
    {
        "planning": "planning",
        "end": END,
    }
)
workflow.add_edge("planning", "agent")
workflow.add_edge("tools", "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": "judge",
    }
)
workflow.add_conditional_edges(
    "judge",
    final_answer_router,
    {
        "planning": "planning",
        "end": END,
    }
)

# Compile the graph
graph = workflow.compile()


"""
async def main() -> list:
    test_inputs: list[str] = [
        # "Download and summarize the findings of this paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11379842/pdf/11671_2024_Article_4070.pdf",
        "Can you find 3 papers on quantum machine learning?",
    ]

    # Run tests and store the results for later visualisation
    outputs: list = []
    for test_input in test_inputs:
        final_answer = await print_stream(graph, test_input)
        outputs.append(final_answer.content)
    return outputs

if __name__ == "__main__":
    outputs =asyncio.run(main())
    for output in outputs:
        print(output)
        print("\n---------------\n")
"""