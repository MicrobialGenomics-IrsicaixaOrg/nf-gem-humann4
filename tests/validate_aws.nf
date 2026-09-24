include { validateAwsPaths } from '../subworkflows/local/utils_nfcore_humann4_pipeline'

workflow {
    def remote = file('s3://example-work/run/work')
    validateAwsPaths(remote, 's3://example-results/run', 'example-queue')
    def rejected = 0
    [[file('/tmp/local-work'), 's3://example-results/run', 'queue'],
                    [remote, '/tmp/results', 'queue'],
                    [remote, 's3://example-results/run', null]].each { values ->
        try { validateAwsPaths(values[0], values[1], values[2]) }
        catch (Exception e) { rejected = rejected + 1 }
    }
    assert rejected == 3
    println 'AWS path checks passed: S3 accepted; local work, local output and missing queue rejected'
}
