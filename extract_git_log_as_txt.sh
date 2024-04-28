#!/bin/bash

directories=("./sources/KEEP" "sources/kotlinx.coroutines" "sources/kotlinx.serialization")
fname="test.txt"

for dir in "${directories[@]}"; do
    output_dir="../../result/$(basename "$dir")"

    # 出力ディレクトリが存在しない場合は作成
    if [ ! -d "$output_dir" ]; then
        mkdir -p "$output_dir"
    fi

    cd "$dir" || exit

    # 実行コマンド
    git log --format='%an' | sort | uniq -c | sort -nr > "$output_dir/$fname"

    cd - || exit
done
