# Outputs

- `humann4/<sample>/`: original MetaPhlAn profile, validation JSON, HUMAnN log, gene families, reactions and pathway abundance.
- `tables/`: joined cohort tables for those three feature types, plus stratified and unstratified versions generated with the same HUMAnN release.
- `multiqc/`: software/provenance report, input SGB counts and native unaligned-read percentages from the HUMAnN logs. Per-sample logs remain the authoritative alignment QC.
- `pipeline_info/`: Nextflow parameters, software versions, trace, HTML execution report, timeline and DAG.

Tables retain native HUMAnN output units. This workflow does not renormalise, filter features, test group differences, or convert abundance estimates to raw integer read counts. Keep stratified and community-level features distinct in downstream analysis. EC-filtered translated search limits the recovered protein families to that reference scope. HUMAnN functional profiles do not replace a dedicated resistome analysis.

`--save_temp` additionally publishes large per-sample HUMAnN temporary directories. Normally these are removed by HUMAnN after a successful sample. Nextflow's work directory still holds staged files; clear it only after verifying results and deciding that resume is no longer needed.
