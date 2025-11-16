FROM ubuntu:22.04

# 必要なパッケージのインストール
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    wget \
    tar \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# CC65のビルドとインストール
WORKDIR /tmp
RUN wget -q https://github.com/cc65/cc65/archive/refs/tags/V2.19.tar.gz && \
    tar xzf V2.19.tar.gz && \
    cd cc65-2.19 && \
    make && \
    make install PREFIX=/usr/local && \
    cd / && \
    rm -rf /tmp/*

# 作業ディレクトリ
WORKDIR /workspace

# デフォルトコマンド
CMD ["make"]
