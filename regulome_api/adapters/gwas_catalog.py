class GWASCatalogAdapter:
    """TODO: implement against the current GWAS Catalog REST API v2 docs.

    Keep pagination, rate limiting, retries, and provider JSON parsing here.
    Do not let upstream response shapes leak into domain models.
    """

    BASE_URL = "https://www.ebi.ac.uk/gwas/rest"

    async def search_trait(self, trait_query: str) -> list[dict]:
        raise NotImplementedError("GWAS Catalog adapter not implemented yet")
