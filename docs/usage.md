# Usage

## Input

CSV columns: `sample,fastq_1,fastq_2,taxonomic_profile`. One row per unique sample. `fastq_2` may be empty. Paths may be local or S3. Sample identifiers contain only letters, numbers, dot, underscore and hyphen. The same FASTQ cannot appear twice. Merge sequencing runs upstream and use the taxonomic profile from those same reads.

For TaxProfiler, retain `save_analysis_ready_fastqs: true` and run MetaPhlAn with `-t rel_ab_w_read_stats`. Use the published analysis-ready reads and each individual profile, not the merged abundance matrix. Profiles must retain the original five columns, coverage, estimated counts, SGB rows and the `mpa_vOct22_CHOCOPhlAnSGB_202403` header. A profile with no detected SGBs is valid. Validate microbial read yield and human removal in TaxProfiler before launching this workflow.

R1 and R2 are concatenated within the HUMAnN task as gzip members; HUMAnN does not use pairing. Inputs are never subsampled in production. The profile is checked before alignment and archived unchanged alongside results. Header validation establishes format compatibility, not that FASTQs and profile are biologically matched: retain the upstream run manifest.

## Runtime and databases

The pipeline defaults to the public Linux AMD64 image `francesccatala/nf-gem-humann4@sha256:317965c67e022321706dd0ffd1fc2dbe236f993331dd24cbff4cddf98d3ec528`. Rebuild it with `containers/humann4/Dockerfile` when changing the runtime. The runtime pins HUMAnN 4.0.0a2 with its official wheel SHA-256, Python, MetaPhlAn, Bowtie2, DIAMOND and GLPK versions. The base image is pinned by digest; transitive conda/Python packages are not fully locked; pin the resulting container digest in `humann_container` for production. MetaPhlAn is installed because HUMAnN checks for the executable even when an external profile is supplied; it is not rerun. The image contains packaged demo data, not the full production references.

Download production references using this HUMAnN version:

```bash
humann_databases --download chocophlan full /reference/humann4
humann_databases --download uniref uniref90_ec_filtered_diamond /reference/humann4
humann_databases --download utility_mapping full /reference/humann4
```

Version 4.0.0a2 advertises the EC-filtered protein database. Do not substitute HUMAnN 3 references or assume a full protein build is available. Point the three parameters to the resulting directories, not the parent directory or tar archives. Record reference URLs/releases in your project manifest. HUMAnN checks database naming and compatibility at execution.

## AWS Batch

Use `-profile awsbatch`, `--aws_queue`, `--aws_region`, an S3 output directory and an S3 `-work-dir`. The controller needs AWS credentials and must remain running; `-with-tower` adds monitoring. The queue, compute environment, IAM roles, S3 permissions and AWS CLI on the worker AMI must already exist. The example config sets an example worker AWS CLI location. The controller and worker roles need access to inputs/references/work/results. No credentials are stored here.

HUMAnN requests 16 CPUs, 64 GB and 24 hours, capped using Nextflow `process.resourceLimits` (16 CPUs, 128 GB, 48 hours; override in your config). Memory/time scale once for resource-related retry. AWS Batch handles up to three Spot attempts; an interrupted task can repeat substantial computation. The AWS profile permits eight concurrent HUMAnN tasks and 16 pending tasks. Tune after measuring real reference sizes, scratch usage, wall time and CPU utilisation. Disk capacity is controlled by the worker AMI/launch template, not these Nextflow memory limits. Size it for every concurrently resident task's databases, uncompressed reads, indexes and intermediate alignments.

### Database delivery

- `staged`: local/S3 directories are staged normally by Nextflow for each sample. This needs no new infrastructure, but copies may be repeated per task and references consume worker scratch. Use for the pilot and measure overhead.
- `shared`: pass absolute **worker-local** directories as strings. Nextflow does not copy them. All workers and containers must already see a read-only reference mount at these paths. Configure your Batch job/container mounts separately; selecting this option does not create EFS, FSx, EBS caches or mounts. Keep reference directories immutable for correct resume behaviour. Change paths when updating a reference version.

The default Docker Hub image is public. For large Batch runs, an ECR mirror in the Batch region can avoid Docker Hub pull-rate limits; set `humann_container` to the mirror digest. Private images require worker-side registry access; a local `docker login` does not authenticate Batch workers.

## Resuming and provenance

Keep the controller `.nextflow/` directory and the original S3 work directory. Re-run the same command with `-resume`. HUMAnN tasks remain per sample, so successful samples are cached independently. Execution trace/report/timeline, parameter JSON and software versions are stored under `pipeline_info/`. Save the input CSV, reference manifest, pipeline SHA and container digest in your study repository.

Use a small representative pilot before releasing the full cohort. Confirm selected pangenomes, nucleotide/translated mapping fractions, unclassified fraction, real scratch usage and that MetaPhlAn was not executed. This workflow has not itself validated full-database performance on your AWS Batch queue.
