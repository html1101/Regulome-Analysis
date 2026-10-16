from __future__ import annotations

import httpx

from regulome_api.models import Gene, GenomicInterval


class EnsemblError(RuntimeError):
    pass


class EnsemblAdapter:
    """Small Ensembl REST client. Provider-specific parsing stays in this adapter."""

    BASE_URL = "https://rest.ensembl.org"

    async def resolve_gene(self, query: str) -> Gene:
        if query.upper().startswith("ENSG"):
            url = f"{self.BASE_URL}/lookup/id/{query.split('.')[0]}"
        else:
            url = f"{self.BASE_URL}/lookup/symbol/homo_sapiens/{query}"

        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.get(url, headers={"Accept": "application/json"})
            if response.status_code == 404:
                raise EnsemblError(f"Gene '{query}' was not found by Ensembl.")
            response.raise_for_status()
            payload = response.json()
        except httpx.HTTPError as exc:
            raise EnsemblError(f"Ensembl request failed: {exc}") from exc

        if not payload.get("id") or not payload.get("seq_region_name"):
            raise EnsemblError(f"Ensembl returned incomplete gene data for '{query}'.")

        # Ensembl returns 1-based inclusive coordinates. Convert to 0-based half-open.
        interval = GenomicInterval(
            assembly="GRCh38",
            chrom=str(payload["seq_region_name"]),
            start=int(payload["start"]) - 1,
            end=int(payload["end"]),
            strand="+" if int(payload.get("strand", 1)) == 1 else "-",
        )
        return Gene(
            ensembl_id=payload["id"],
            symbol=payload.get("display_name"),
            interval=interval,
            source="Ensembl REST",
        )
