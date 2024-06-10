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

    sh ${BASE_DIR}/get_volatility_loc_sum.sh

    # リポジトリ名に . を含むものは _ に置換
    REPOSITORY_NAME=${REPOSITORY//./_}
    mv git_log_changes_loc_sum_per_month.csv ${BASE_DIR}/result/kotlin_organization/${REPOSITORY_NAME}.csv

    cd ${BASE_DIR}/
done
