# Research

This is a sample research pipeline describing how somebody might go about researching a particular gene computationally and how this looks to automate that process as much as possible.

A disease can be associated with a gene through coding mutations, altered expression, cell-type composition, regulatory elements, splicing, epigenetic changes, or downstream effects.

ClinGen does Mendelian disease research (looks whether damaging variation causes a defined disorder through looking at rare variants in affected individuals + inheritance patterns).

This is looking at complex disease research--looking at how genetic+environmental factors contribute to a condition, with many correlated variants and some plausible target genes.

Ex: IL6 expression is increased in some Crohn's disease-associated samples.

1. Normalize gene + disease name
    - Map gene to stable identifier (Ensembl/NCBI gene ID)--some symbols can have aliases or be reused in historical literature, Ensembl, HGNC, NCBI Gnee
    - Disease names - MONDO, Disease Ontology, MedGen
2. Survey existing literature - can do with PubMed (small scale could just be with ClinVar), looking for publications like:
    - Primary disease-association: find if gene or nearby locus is associated with disease risk
    - Molecular mechanism - regulatory variants, TF, enhancers, pathways
    - Perturbation studies - knockdowns + how they affect relevant phenotype
    - Replication/contradictory studies
    - Reviews + meta-analyses
3. Investigate differential expression, could come from:
    - Bulk RNA-seq from affected/control tissues
    - Single-cell RNA-seq
    - Microarray datasets
    - Microbe data
    - Tissue-specific expression atlases
    - Protein abundance, activity measurements
    - Longitudinal studies
4. Can do (3) at the gene level, or transcript level (abundance of the individual transcript isoforms)
5. Establish whether inherited genetic variation implicates gene or its regulatory neighborhood
    - Search GWAS catalog
6. Connect genetic variation to gene expression/splicing
    1. eQTL/GTEx data (variants associated with gene expression)
    2. Colocalization - whether two signals share a causal variant (e.g. GWAS association + eQTL signal, they share a causal signal)
    3. Splicing
7. Find what tissue/cell type/cell states this variant is relevant in
    - Ex: maybe variant overlaps an active enhancer in macrophages, but it's under closed chromatin in intestinal epithelial cells
    - Use histone modification profiles, scATAC-seq, DNA methylation
8. Find involved epigenetic and regulatory elements
    - ChIP-seq: find active enhancers + promoter elements
    - ATAC-seq, DNase-seq: open chromatin to make accessible to regulatory proteins
    - Map regulatory elements to target genes
9. TFs + sequence-level regulatory effects
    - Connect variant to altered binding + regulatory activity, target gene, disease phenotype
    - Compare reference and alternate alleles against TF motifs


## Example pipeline

Obesity-associated variation near FTO, with regulatory effects on IRX3 and IRX5

The FTO locus is a classic example of why gene-centric interpretation based on genomic proximity can be misleading.

### The initial observation
- Genome-wide association studies identified common variants within introns of FTO that were associated with obesity and related traits.
- A simple gene-centric pipeline might have stopped there and concluded that the variants must influence obesity through FTO.
- But a GWAS association within a gene does not establish that the gene itself mediates the association.

### The investigation
- In 2014, Smemo and colleagues reported that obesity-associated noncoding sequences in the FTO region have long-range regulatory connections with IRX3. They combined chromatin-interaction evidence, enhancer experiments, expression analyses, and mouse studies to investigate the relationship. Their results supported IRX3 as a functional target of the region. Smemo et al., Nature (2014)(nature.com)
- A subsequent study investigated a specific variant, rs1421085, and reported a mechanism involving both IRX3 and IRX5 in adipocyte precursor cells. The study linked the obesity-associated allele to disruption of a binding motif for the transcriptional repressor ARID5B, increased enhancer activity, altered IRX3 and IRX5 expression during adipocyte differentiation, and changes in thermogenesis and fat storage. It also used CRISPR editing and perturbation experiments to test the proposed mechanism. Claussnitzer et al., FTO Obesity Variant Circuitry and Adipocyte Browning in Humans(nejm.org)

## Definitions

**sQTL** - splicing quantitative trait locus, genomic variant associated with variation in alternative splicing ot pre-mRNA