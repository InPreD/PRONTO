FROM continuumio/miniconda3:23.9.0-0
LABEL maintainer="Xiaoli.Zhang@rr-research.no"
RUN conda update -n base -c defaults conda \
    && conda install xlrd -c conda-forge \
    && conda install xlutils -c conda-forge \
    && conda install python-pptx -c conda-forge \
    && conda install python-docx -c conda-forge
RUN mkdir -p /pronto
COPY Config /pronto/Config
COPY In /pronto/In
COPY Out /pronto/Out
COPY Script /pronto/Script
COPY Testing_data /pronto/Testing_data
