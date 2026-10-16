from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class EvidenceOrigin(StrEnum):
    EXPERIMENTAL = "experimental"
    OBSERVATIONAL = "observational"
    COMPUTATIONAL_PREDICTION = "computational_prediction"
    CURATED = "curated"


class EvidenceType(StrEnum):
    DIFFERENTIAL_EXPRESSION = "differential_expression"
    GWAS = "gwas"
    EQTL = "eqtl"
    SQTL = "sqtl"
    TF_BINDING = "tf_binding"
    MOTIF_EFFECT = "motif_effect"
    CHROMATIN_ACCESSIBILITY = "chromatin_accessibility"
    HISTONE_MARK = "histone_mark"
    DNA_METHYLATION = "dna_methylation"
    ENHANCER_GENE_LINK = "enhancer_gene_link"
    LITERATURE = "literature"


class Direction(StrEnum):
    INCREASED = "increased"
    DECREASED = "decreased"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"


class GenomicInterval(BaseModel):
    """Internal coordinates are 0-based, half-open: [start, end)."""

    model_config = ConfigDict(extra="forbid")
    assembly: str = "GRCh38"
    chrom: str
    start: int = Field(ge=0)
    end: int = Field(gt=0)
    strand: Literal["+", "-", "."] = "."

    def model_post_init(self, __context: Any) -> None:
        if self.end <= self.start:
            raise ValueError("end must be greater than start")


class Gene(BaseModel):
    ensembl_id: str
    symbol: str | None = None
    name: str | None = None
    interval: GenomicInterval | None = None
    source: str = "Ensembl"


class Disease(BaseModel):
    query: str
    ontology_id: str | None = None
    canonical_name: str | None = None
    synonyms: list[str] = Field(default_factory=list)
    resolution_status: Literal["unresolved", "resolved", "ambiguous"] = "unresolved"


class Variant(BaseModel):
    id: str
    assembly: str | None = None
    chrom: str | None = None
    position: int | None = None
    ref: str | None = None
    alt: str | None = None
    rsids: list[str] = Field(default_factory=list)


class RegulatoryElement(BaseModel):
    id: str
    interval: GenomicInterval
    element_type: str | None = None
    biosample: str | None = None
    source_accession: str | None = None


class TranscriptionFactor(BaseModel):
    id: str
    symbol: str
    motif_id: str | None = None


class Study(BaseModel):
    id: str
    title: str | None = None
    year: int | None = None
    doi: str | None = None
    url: str | None = None
    abstract: str | None = None


class EvidenceRecord(BaseModel):
    """One observation or prediction; not a whole causal mechanism."""

    id: str = Field(default_factory=lambda: f"ev_{uuid4().hex[:12]}")
    subject_type: str
    subject_id: str
    predicate: str
    object_type: str
    object_id: str
    evidence_type: EvidenceType
    origin: EvidenceOrigin
    direction: Direction = Direction.UNKNOWN
    tissue_label: str | None = None
    tissue_id: str | None = None
    effect_size: float | None = None
    p_value: float | None = Field(default=None, ge=0, le=1)
    source_name: str
    source_record_id: str | None = None
    source_url: str | None = None
    retrieved_at: datetime = Field(default_factory=utc_now)
    method: str | None = None
    limitations: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class MechanismStep(BaseModel):
    subject: str
    predicate: str
    object: str
    evidence_ids: list[str] = Field(default_factory=list)
    direction: Direction = Direction.UNKNOWN


class MechanismHypothesis(BaseModel):
    id: str = Field(default_factory=lambda: f"mech_{uuid4().hex[:12]}")
    title: str
    target_gene_id: str
    steps: list[MechanismStep] = Field(default_factory=list)
    genetic_support: Literal["none", "limited", "moderate", "strong", "unknown"] = "unknown"
    regulatory_support: Literal["none", "limited", "moderate", "strong", "unknown"] = "unknown"
    tissue_relevance: Literal["low", "moderate", "high", "unknown"] = "unknown"
    directional_consistency: Literal["consistent", "inconsistent", "unknown"] = "unknown"
    experimental_validation: Literal["absent", "partial", "present", "unknown"] = "unknown"
    limitations: list[str] = Field(default_factory=list)


class InvestigationCreate(BaseModel):
    gene_query: str = Field(min_length=1, examples=["IL6"])
    disease_query: str = Field(min_length=1, examples=["Crohn disease"])
    tissue: str | None = None
    expression_direction: Direction = Direction.UNKNOWN
    genome_assembly: Literal["GRCh38"] = "GRCh38"


class Investigation(BaseModel):
    id: str = Field(default_factory=lambda: f"inv_{uuid4().hex[:12]}")
    status: JobStatus = JobStatus.QUEUED
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    gene: Gene | None = None
    disease: Disease
    tissue: str | None = None
    expression_direction: Direction = Direction.UNKNOWN
    genome_assembly: str = "GRCh38"
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    mechanisms: list[MechanismHypothesis] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class InvestigationSummary(BaseModel):
    id: str
    status: JobStatus
    gene: Gene | None
    disease: Disease
    tissue: str | None
    expression_direction: Direction
    evidence_count: int
    mechanism_count: int
    warnings: list[str]
    errors: list[str]
