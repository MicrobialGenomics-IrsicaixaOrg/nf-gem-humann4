include { HUMANN4_RUN } from '../modules/local/humann4/run/main'
include { HUMANN4_JOIN } from '../modules/local/humann4/join/main'
include { MULTIQC } from '../modules/nf-core/multiqc/main'
include { softwareVersionsToYAML } from '../subworkflows/nf-core/utils_nfcore_pipeline'

workflow HUMANN4 {
    take:
    samples
    main:
    // Shared mode intentionally passes strings, so Nextflow does not copy the databases.
    def db = [params.nucleotide_db, params.protein_db, params.utility_db]
    def staged = params.database_mode == 'staged'
    def paths = staged ? db.collect { file(it, checkIfExists: true) } : []
    HUMANN4_RUN(samples, paths, staged ? [] : db, params.metaphlan_index, params.save_temp)
    HUMANN4_JOIN(HUMANN4_RUN.out.genefamilies.collect { it[1] },
                HUMANN4_RUN.out.reactions.collect { it[1] },
                HUMANN4_RUN.out.pathabundance.collect { it[1] })
    versions = softwareVersionsToYAML(HUMANN4_RUN.out.versions.mix(HUMANN4_JOIN.out.versions))
        .collectFile(sort: true, newLine: true, name: 'humann4_software_mqc_versions.yml', storeDir: "${params.outdir}/pipeline_info")
    MULTIQC(HUMANN4_RUN.out.qc.map { it[1] }.mix(versions).collect(),
        [file("${projectDir}/assets/multiqc_config.yml")],
        params.multiqc_config ? [file(params.multiqc_config)] : [], params.multiqc_logo ? [file(params.multiqc_logo)] : [], [], [])
    emit:
    multiqc_report = MULTIQC.out.report.toList()
}
