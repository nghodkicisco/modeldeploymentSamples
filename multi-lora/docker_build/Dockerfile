#Copyright Cisco Systems, Inc. and its affiliates
#Licensed under the MIT License


FROM ghcr.io/predibase/lorax:latest

COPY sagemaker_entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

