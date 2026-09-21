process HUMANN4_JOIN {
    label 'process_medium'
    input:
    path genes, stageAs: 'genefamilies/*'
    path reactions, stageAs: 'reactions/*'
    path pathways, stageAs: 'pathabundance/*'
    output:
    path '*.tsv', emit: tables
    path 'versions.yml', emit: versions
    when:
    task.ext.when == null || task.ext.when
    script:
    def args = task.ext.args ?: ''
    """
    for kind in genefamilies reactions pathabundance; do
        humann_join_tables --input "\$kind" --output "\$kind.tsv" ${args}
        humann_split_stratified_table --input "\$kind.tsv" --output .
    done
    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        humann: \$(humann --version | sed 's/humann v//')
    END_VERSIONS
    """
    stub:
    """
    for kind in genefamilies reactions pathabundance; do
        printf '# Feature\\tstub\\nTEST\\t1\\n' > "\$kind.tsv"
    done
    printf '"${task.process}":\\n    humann: "stub"\\n' > versions.yml
    """
}
