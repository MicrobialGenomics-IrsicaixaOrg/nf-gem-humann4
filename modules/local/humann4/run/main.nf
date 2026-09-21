process HUMANN4_RUN {
    tag "${meta.id}"
    label 'process_high'
    input:
    tuple val(meta), path(reads, stageAs: 'reads??/*'), path(profile, stageAs: 'profile/*')
    path staged_db, stageAs: 'db??/*'
    val shared_db
    val index
    val save_temp
    output:
    tuple val(meta), path('*_2_genefamilies.tsv'), emit: genefamilies
    tuple val(meta), path('*_3_reactions.tsv'), emit: reactions
    tuple val(meta), path('*_4_pathabundance.tsv'), emit: pathabundance
    tuple val(meta), path('*_1_metaphlan_profile.tsv'), emit: profile
    tuple val(meta), path('*_0.log'), emit: log
    tuple val(meta), path('*_validation.json'), emit: validation
    tuple val(meta), path('*_humann_temp*'), optional: true, emit: temp
    tuple val(meta), path('*_mqc.json'), emit: qc
    path 'versions.yml', emit: versions
    when:
    task.ext.when == null || task.ext.when
    script:
    def args = task.ext.args ?: ''
    def db = shared_db ?: staged_db
    def clean = save_temp ? '' : '--remove-temp-output'
    def fastqs = [reads].flatten().collect { "'${it}'" }.join(' ')
    """
    validate_profile.py '${profile}' '${index}' '${meta.id}' > '${meta.id}_validation.json'
    test -d '${db[0]}' && test -d '${db[1]}' && test -d '${db[2]}'
    cat ${fastqs} > '${meta.id}.fastq.gz'
    humann \\
        --input '${meta.id}.fastq.gz' \\
        --output . \\
        --output-basename '${meta.id}' \\
        --threads ${task.cpus} \\
        --taxonomic-profile '${profile}' \\
        --nucleotide-database '${db[0]}' \\
        --protein-database '${db[1]}' \\
        --utility-database '${db[2]}' \\
        ${clean} ${args}
    # Preserve the exact input profile, including coverage and estimated read counts.
    cp '${profile}' '${meta.id}_1_metaphlan_profile.tsv'
    humann_qc.py '${meta.id}_validation.json' '${meta.id}_0.log' > '${meta.id}_mqc.json'
    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        humann: \$(humann --version | sed 's/humann v//')
        bowtie2: \$(bowtie2 --version | head -n 1 | sed 's/.*version //')
        diamond: \$(diamond version | sed 's/diamond version //')
    END_VERSIONS
    """
    stub:
    """
    validate_profile.py '${profile}' '${index}' '${meta.id}' > '${meta.id}_validation.json'
    cp '${profile}' '${meta.id}_1_metaphlan_profile.tsv'
    for kind in 2_genefamilies 3_reactions 4_pathabundance; do
        printf '# Feature\\t${meta.id}\\nTEST\\t1\\n' > "${meta.id}_\${kind}.tsv"
    done
    echo 'STUB: no biological computation' > '${meta.id}_0.log'
    humann_qc.py '${meta.id}_validation.json' '${meta.id}_0.log' > '${meta.id}_mqc.json'
    printf '"${task.process}":\\n    humann: "stub"\\n' > versions.yml
    """
}
