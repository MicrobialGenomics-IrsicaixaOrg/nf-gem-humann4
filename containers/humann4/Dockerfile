FROM mambaorg/micromamba:2.0.5@sha256:8d0d4cad074afe3ac93b58dce88bd2659153d3fa6de3a6968f501710e8d3c832
USER root
RUN mkdir -p /opt/humann4 && chmod 755 /opt/humann4
COPY --chown=$MAMBA_USER:$MAMBA_USER containers/humann4/environment.yml /tmp/environment.yml
COPY --chown=$MAMBA_USER:$MAMBA_USER containers/humann4/requirements.txt /tmp/requirements.txt
USER $MAMBA_USER
RUN micromamba install --yes --name base --file /tmp/environment.yml && micromamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN python -m pip install --no-cache-dir MetaPhlAn==4.1.1 \
    && python -m pip install --no-cache-dir --no-deps --only-binary=:all: --require-hashes -r /tmp/requirements.txt \
    && humann --version && bowtie2 --version && diamond version && glpsol --version
ENV PATH=/opt/conda/bin:$PATH
USER root
WORKDIR /data
ENTRYPOINT []
