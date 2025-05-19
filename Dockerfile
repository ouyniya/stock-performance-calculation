# README at: https://github.com/microsoft/vscode-dev-containers/tree/main/containers/ubuntu

# Define variables
ARG USERNAME=vscode
ARG GROUPNAME=$USERNAME
ARG VIRTUAL_ENV=/opt/venv
ARG DEBIAN_FRONTEND=noninteractive
ARG WORKDIR_PATH=/app

ARG VARIANT=ubuntu-24.04
FROM mcr.microsoft.com/vscode/devcontainers/base:${VARIANT} AS builder-image

# Set noninterative
ARG DEBIAN_FRONTEND

# Install python
RUN apt-get update \
    && apt-get -y install --no-install-recommends \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv

# Install some python packages dependencies
RUN apt-get update \
    && apt-get -y install --no-install-recommends \
    unixodbc \
    unixodbc-dev \
    freetds-dev \
    freetds-bin \
    tdsodbc \
    cmake \
    libopenblas-dev \
    build-essential

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create venv and activate
ARG VIRTUAL_ENV
ENV VIRTUAL_ENV=$VIRTUAL_ENV
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Ensure all python outputs are sent to terminal
ENV PYTHONUNBUFFERED=1

# Set working directory
ARG WORKDIR_PATH
WORKDIR $WORKDIR_PATH

# Copy from local
COPY . ./

# Change owner to non-root user
ARG USERNAME
ARG GROUPNAME
RUN chown -R $USERNAME:$GROUPNAME $VIRTUAL_ENV

# Switch to non-root user
USER $USERNAME

# Install python requirements
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

# # Create runner-image
# FROM ubuntu:24.04 AS runner-image

# # Set noninterative
# ARG DEBIAN_FRONTEND

# # Install python
# RUN apt-get update \
#     && apt-get -y install --no-install-recommends \
#     python3 \
#     python3-pip \
#     python3-venv

# # Clean up
# RUN apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# # Copy venv from build-image and activate
# ARG VIRTUAL_ENV
# ENV VIRTUAL_ENV=$VIRTUAL_ENV
# COPY --from=builder-image $VIRTUAL_ENV $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# # Ensure all python outputs are sent to terminal
# ENV PYTHONUNBUFFERED=1

# # Set working directory
# ARG WORKDIR_PATH
# WORKDIR $WORKDIR_PATH

# # Copy from local
# COPY . ./

# # Create group and user
# ARG USERNAME
# ARG GROUPNAME
# RUN groupadd $GROUPNAME
# RUN useradd -s /bin/bash --gid $GROUPNAME -m $USERNAME

# # Change owner to non-root user
# RUN chown -R $USERNAME:$GROUPNAME $VIRTUAL_ENV

# CMD ["streamlit", "run", "hello.py"]