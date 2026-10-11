from fastapi import APIRouter

from knowitall.agent import analysis_graph
from knowitall.domain import AnalysisAnswer, AnalysisIntent, AnalysisRequest, BusinessScope

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisAnswer)
async def create_analysis(request: AnalysisRequest) -> AnalysisAnswer:
    result = await analysis_graph.ainvoke(
        {
            "request_id": str(request.request_id),
            "question": request.question,
            "requested_business_line_ids": request.business_line_ids,
        }
    )
    return AnalysisAnswer(
        request_id=request.request_id,
        intent=AnalysisIntent(result["intent"]),
        effective_scope=BusinessScope.model_validate(result["effective_scope"]),
        conclusion=result["conclusion"],
        evidence_ids=result.get("evidence_ids", []),
        uncertainty=result.get("uncertainty", []),
    )
