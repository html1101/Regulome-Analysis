from __future__ import annotations

import httpx

from regulome_api.models import Study


class PubMedAdapter:
    """Minimal PubMed search adapter; stores metadata, not full-text articles."""

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    async def search(self, query: str, limit: int = 10) -> list[Study]:
        async with httpx.AsyncClient(timeout=20) as client:
            search_resp = await client.get(
                f"{self.BASE_URL}/esearch.fcgi",
                params={"db": "pubmed", "term": query, "retmax": limit, "retmode": "json"},
            )
            search_resp.raise_for_status()
            ids = search_resp.json().get("esearchresult", {}).get("idlist", [])
            if not ids:
                return []

            summary_resp = await client.get(
                f"{self.BASE_URL}/esummary.fcgi",
                params={"db": "pubmed", "id": ",".join(ids), "retmode": "json"},
            )
            summary_resp.raise_for_status()
            result = summary_resp.json().get("result", {})

        studies: list[Study] = []
        for pmid in ids:
            item = result.get(pmid, {})
            if not item:
                continue
            pubdate = str(item.get("pubdate", ""))
            year = next(
                (int(token) for token in pubdate.split() if token.isdigit() and len(token) == 4),
                None,
            )
            studies.append(
                Study(
                    id=pmid,
                    title=item.get("title"),
                    year=year,
                    url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                )
            )
        return studies
