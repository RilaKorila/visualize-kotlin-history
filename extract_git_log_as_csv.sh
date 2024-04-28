#!/bin/bash

directories=("./sources/KEEP" "sources/kotlinx.coroutines" "sources/kotlinx.serialization")
fname="test.csv"

# ディレクトリごとに処理
for dir in "${directories[@]}"; do
    output_dir="../../result/$(basename "$dir")"

    # 出力ディレクトリが存在しない場合は作成
    if [ ! -d "$output_dir" ]; then
        mkdir -p "$output_dir"
    fi

    cd "$dir" || exit

    echo "author,commit_time,message,lines_changed,branches" > "$output_dir/$fname"
    # コミット情報を取得し、CSV形式で出力
    # git log --format='%an,%ad,%s' --date=iso-local --numstat --branches | awk -v OFS=',' '
    #   /^[0-9]+[[:space:]]+[0-9]+[[:space:]]+/ { added+=$1; removed+=$2 }
    #   /^commit/ { if (NR > 1) print author, commit_time, message, added "+" removed, branches; 
    #               author=$2; commit_time=$3 " " $4 " " $5 " " $6 " " $7; added=removed=0; branches=$NF }
    #   END { if (NR > 1) print author, commit_time, message, added "+" removed, branches }
    # ' >> "$output_dir/$fname"
    git log --format='%an,%ad,%s' --date=iso-local --numstat --branches >> "$output_dir/$fname"

    cd - || exit
done
