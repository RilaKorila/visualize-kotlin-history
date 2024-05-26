#!/bin/bash

# 空の配列を定義
REPOSITORIES=()

# ファイルの内容を一行ずつ読み込み、配列に格納
while IFS= read -r line; do
    REPOSITORIES+=("$line")
done < all_repositories_in_Kotlin.txt

BASE_DIR="/path/to/visualize-kotlin-history"

cd ${BASE_DIR}/sources/

# 各リポジトリをクローン
for REPOSITORY in "${REPOSITORIES[@]}"; do
    echo "Cloning repository: $REPOSITORY"

    git clone https://github.com/Kotlin/$REPOSITORY.git
    if [ $? -ne 0 ]; then
        echo "Failed to clone $REPOSITORY"
    fi
    # 15秒スリープ
    sleep 15
done

# 各リポジトリに対して変化量を抽出しcsvに出力
for REPOSITORY in "${REPOSITORIES[@]}"; do
    cd ${BASE_DIR}/sources/${REPOSITORY}

    sh ${BASE_DIR}/get_volatility.sh

    mv git_log_changes-20*.txt ${BASE_DIR}/tmp/

    cd ${BASE_DIR}/

    python commit_counts_line_chart.py ${REPOSITORY}

    rm ${BASE_DIR}/tmp/*.txt
done
