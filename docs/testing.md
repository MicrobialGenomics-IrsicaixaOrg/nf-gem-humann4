# Testing

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
docker build -f containers/humann4/Dockerfile -t humann4:test .
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:$PWD" -w "$PWD" humann4:test python tests/prepare_demo.py
nextflow run . -profile test,docker --humann_container humann4:test --outdir results-test
python tests/assert_outputs.py results-test
```

The fixture contains 10,000 reads from the pinned HUMAnN package and an explicitly synthetic profile selecting three demo pangenomes. It covers paired and single-end inputs and runs actual Bowtie2, DIAMOND and pathway quantification. It does not establish biological accuracy or production throughput. CI also verifies resume and shared-reference delivery. `nf-test` can run `tests/default.nf.test` after fixture preparation with the test and docker profiles.

A `-stub-run` verifies process wiring but does not compute biological results. The real-output assertions deliberately reject stub logs.

The tested image is public on Docker Hub as `francesccatala/nf-gem-humann4:4.0.0a2`; the pipeline pins its immutable digest. The separate container publication workflow requires manual dispatch and repository secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` with push access to that repository. These secrets are not configured by a local Docker login. After rebuilding, verify the new image before updating the pipeline digest.
