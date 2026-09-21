# MicrobialGenomics-IrsicaixaOrg/nf-gem-humann4

![Nextflow](https://img.shields.io/badge/nextflow-%E2%89%A525.04.0-brightgreen)
![nf-core template](https://img.shields.io/badge/nf--core%20template-3.5.1-blue)

HUMAnN **4.0.0a2** functional profiling from preprocessed shotgun reads and existing individual MetaPhlAn profiles. Built from the nf-core/tools 3.5.1 template, using Nextflow DSL2, nf-schema validation, resource labels, containerised modules, MultiQC and execution reports. This is an independent pipeline, not an official nf-core release.

Each sample supplies cleaned FASTQ reads and its matching MetaPhlAn `rel_ab_w_read_stats` profile. HUMAnN receives `--taxonomic-profile`; MetaPhlAn, quality filtering and host removal are not repeated. The required marker index is `mpa_vOct22_CHOCOPhlAnSGB_202403`.

```bash
nextflow run MicrobialGenomics-IrsicaixaOrg/nf-gem-humann4 -r main \
  -profile awsbatch -params-file params.yml \
  -c awsbatch.config \
  -work-dir s3://YOUR-WORK-BUCKET/humann4/run01/work \
  -with-tower
```

The HUMAnN runtime is defined in `containers/humann4/Dockerfile`; build it or publish it using the container workflow before the first run. For AWS, use an accessible image (for example in ECR) via `--humann_container`. Use a released tag or commit SHA for production. Copy `assets/params.example.yml` and `assets/awsbatch.example.config`, then set your paths and existing queue. Local execution uses `-profile docker` with local paths. Nextflow requires Java 17+ and Nextflow >=25.04; CI uses 25.10.2.

- [Inputs, databases and AWS](docs/usage.md)
- [Outputs and interpretation](docs/output.md)
- [Testing and container](docs/testing.md)

HUMAnN 4 remains a prerelease. The integration test uses small packaged demo references and synthetic taxonomic profiles; full reference databases and AWS Batch execution need a representative pilot before cohort launch. No AWS infrastructure or jobs are created by installing this repository.
