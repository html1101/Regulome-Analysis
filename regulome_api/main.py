from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from regulome_api.models import Investigation, InvestigationCreate, InvestigationSummary
from regulome_api.services.investigations import InvestigationNotFound, InvestigationService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.investigations = InvestigationService()
    yield


app = FastAPI(
    title="Regulome Detective API",
    version="0.1.0",
    description=(
        "Expression-first regulatory genomics investigation API. "
        "This starter resolves genes but does not yet infer causal mechanisms."
    ),
    lifespan=lifespan,
)


def get_service() -> InvestigationService:
    return app.state.investigations


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/api/v1/investigations",
    response_model=Investigation,
    status_code=status.HTTP_201_CREATED,
    summary="Create a gene + disease investigation",
)
async def create_investigation(request: InvestigationCreate) -> Investigation:
    return await get_service().create(request)


@app.get("/api/v1/investigations", response_model=list[InvestigationSummary])
async def list_investigations() -> list[InvestigationSummary]:
    return [
        InvestigationSummary(
            id=item.id,
            status=item.status,
            gene=item.gene,
            disease=item.disease,
            tissue=item.tissue,
            expression_direction=item.expression_direction,
            evidence_count=len(item.evidence),
            mechanism_count=len(item.mechanisms),
            warnings=item.warnings,
            errors=item.errors,
        )
        for item in get_service().list()
    ]


@app.get("/api/v1/investigations/{investigation_id}", response_model=Investigation)
async def get_investigation(investigation_id: str) -> Investigation:
    try:
        return get_service().get(investigation_id)
    except InvestigationNotFound:
        raise HTTPException(status_code=404, detail="Investigation not found") from None
