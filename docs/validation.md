# Validation scope

The repository is derived from the official nf-core/tools 3.5.1 template. The `.nf-core.yml` exceptions are for independent organisation branding, institution-specific GitHub CI, no iGenomes use, no predefined full-cohort test, and no remote institutional config loaded automatically. The local test data come from the HUMAnN package rather than nf-core test-data URLs. These choices do not disable sample or parameter validation.

Unit tests reject incorrect database versions, relative-abundance-only profiles, nonfinite coverage, malformed/empty profiles and accept valid profiles with no SGB detections. Nextflow validates unique sample identifiers and disallows reused FASTQs before dispatch.

The integration fixture exercises actual HUMAnN 4.0.0a2, Bowtie2, DIAMOND, pathway quantification, table merging and MultiQC. It uses demo references and an explicitly synthetic profile; it tests software integration rather than scientific accuracy. CI verifies resume and both staged and shared database delivery. AWS execution and full database resource requirements require a separate pilot with authorised study data.

## Local validation, 2026-09-21

Six profile-validation unit tests passed. Nextflow 25.10.2 completed the actual Docker demo for paired and single-end reads in both staged and shared-reference modes. Result structure and merged table columns passed assertions. A second identical run cached all four tasks with `-resume`. This validation used Linux/amd64 containers under Docker on macOS, not AWS Batch or production reference databases.
