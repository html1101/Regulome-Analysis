from __future__ import annotations

from datetime import datetime, timezone

from regulome_api.adapters.ensembl import EnsemblAdapter, EnsemblError
from regulome_api.models import (
    Disease,
    Investigation,
    InvestigationCreate,
    JobStatus,
)


class InvestigationNotFound(KeyError):
    pass


class InvestigationService:
    """MVP orchestration. In-memory storage is development-only."""

    def __init__(self, ensembl: EnsemblAdapter | None = None):
        self.ensembl = ensembl or EnsemblAdapter()
        self._items: dict[str, Investigation] = {}

    async def create(self, request: InvestigationCreate) -> Investigation:
        investigation = Investigation(
            status=JobStatus.RUNNING,
            disease=Disease(query=request.disease_query),
            tissue=request.tissue,
            expression_direction=request.expression_direction,
            genome_assembly=request.genome_assembly,
        )
        self._items[investigation.id] = investigation

        try:
            investigation.gene = await self.ensembl.resolve_gene(request.gene_query)
        except EnsemblError as exc:
            investigation.status = JobStatus.FAILED
            investigation.errors.append(str(exc))
        else:
            investigation.status = JobStatus.PARTIAL
            investigation.warnings.extend([
                "Gene resolved. Disease normalization and evidence collection are not implemented yet.",
                "No causal mechanism is inferred by this starter; no evidence modules have run.",
            ])

        investigation.updated_at = datetime.now(timezone.utc)
        self._items[investigation.id] = investigation
        return investigation

    def get(self, investigation_id: str) -> Investigation:
        try:
            return self._items[investigation_id]
        except KeyError as exc:
            raise InvestigationNotFound(investigation_id) from exc

    def list(self) -> list[Investigation]:
        return sorted(self._items.values(), key=lambda item: item.created_at, reverse=True)
