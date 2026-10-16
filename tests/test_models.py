import pytest
from pydantic import ValidationError

from regulome_api.models import (
    Direction,
    EvidenceOrigin,
    EvidenceRecord,
    EvidenceType,
    GenomicInterval,
    InvestigationCreate,
)


def test_genomic_interval_uses_half_open_coordinates():
    interval = GenomicInterval(assembly="GRCh38", chrom="1", start=9, end=20)
    assert interval.start == 9
    assert interval.end == 20


def test_genomic_interval_rejects_invalid_range():
    with pytest.raises(ValidationError):
        GenomicInterval(chrom="1", start=20, end=20)


def test_investigation_request_defaults():
    request = InvestigationCreate(gene_query="IL6", disease_query="Crohn disease")
    assert request.genome_assembly == "GRCh38"
    assert request.expression_direction == Direction.UNKNOWN


def test_evidence_requires_provenance():
    evidence = EvidenceRecord(
        subject_type="variant",
        subject_id="rs123",
        predicate="overlaps",
        object_type="regulatory_element",
        object_id="element_1",
        evidence_type=EvidenceType.MOTIF_EFFECT,
        origin=EvidenceOrigin.COMPUTATIONAL_PREDICTION,
        source_name="JASPAR",
    )
    assert evidence.source_name == "JASPAR"
    assert evidence.direction == Direction.UNKNOWN
