FROM gcc:latest

# Multi-language execution sandbox.
# gcc image already provides gcc + g++. Add Python and Java.
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

WORKDIR /box
