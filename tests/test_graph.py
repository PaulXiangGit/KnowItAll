import pytest

from knowitall.agent import analysis_graph
from knowitall.domain import AnalysisIntent, ScopeSource


@pytest.mark.asyncio
async def test_graph_uses_explicit_business_scope() -> None:
    result = await analysis_graph.ainvoke(
        {
            "request_id": "request-1",
            "question": "修改订单字段会影响哪些页面？",
            "requested_business_line_ids": ["commerce-order"],
        }
    )

    assert result["intent"] == AnalysisIntent.CHANGE_IMPACT.value
    assert result["effective_scope"]["source"] == ScopeSource.USER_EXPLICIT.value
    assert result["effective_scope"]["business_line_ids"] == ["commerce-order"]


@pytest.mark.asyncio
async def test_graph_does_not_use_memory_without_a_scope() -> None:
    result = await analysis_graph.ainvoke(
        {
            "request_id": "request-2",
            "question": "查找相似需求",
            "requested_business_line_ids": [],
        }
    )

    assert result["effective_scope"]["requires_confirmation"] is True
    assert result["effective_scope"]["business_line_ids"] == []
    assert result["uncertainty"]
