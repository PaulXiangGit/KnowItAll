from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from knowitall.domain.analysis import AnalysisIntent, AnalysisState, ScopeSource


def resolve_scope(state: AnalysisState) -> AnalysisState:
    requested = state.get("requested_business_line_ids", [])
    if requested:
        return {
            "effective_scope": {
                "business_line_ids": requested,
                "source": ScopeSource.USER_EXPLICIT.value,
                "confidence": 1.0,
                "requires_confirmation": False,
            }
        }

    return {
        "effective_scope": {
            "business_line_ids": [],
            "source": ScopeSource.UNRESOLVED.value,
            "confidence": 0.0,
            "requires_confirmation": True,
        },
        "uncertainty": ["尚未确定业务线，当前未注入任何历史业务记忆。"],
    }


def classify_intent(state: AnalysisState) -> AnalysisState:
    question = state["question"]
    if any(keyword in question for keyword in ("影响", "依赖", "调用")):
        intent = AnalysisIntent.CHANGE_IMPACT
    elif any(keyword in question for keyword in ("缺少", "评审", "完整")):
        intent = AnalysisIntent.REQUIREMENT_REVIEW
    else:
        intent = AnalysisIntent.KNOWLEDGE_SEARCH
    return {"intent": intent.value}


def compose_placeholder_answer(state: AnalysisState) -> AnalysisState:
    intent = state["intent"]
    return {
        "conclusion": f"已识别分析意图 {intent}；知识检索工具将在后续任务中接入。",
        "evidence_ids": [],
    }


def build_analysis_graph() -> CompiledStateGraph[AnalysisState, None, AnalysisState, AnalysisState]:
    builder = StateGraph(AnalysisState)
    builder.add_node("resolve_scope", resolve_scope)
    builder.add_node("classify_intent", classify_intent)
    builder.add_node("compose_answer", compose_placeholder_answer)
    builder.add_edge(START, "resolve_scope")
    builder.add_edge("resolve_scope", "classify_intent")
    builder.add_edge("classify_intent", "compose_answer")
    builder.add_edge("compose_answer", END)
    return builder.compile()


analysis_graph = build_analysis_graph()
