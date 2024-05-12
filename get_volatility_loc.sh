#!/bin/bash

# 指定された期間内のファイルごとの追加行数と削除行数を集計する関数
file_changes_in_range() {
    local date_from="$1"
    local date_to="$2"
    local fname="$3"
    
    echo "filename,add_lines,del_lines" >> "$fname"

    # 変更されたファイルのリストを取得
    changed_files=$(git log --pretty=format: --numstat --since="$date_from" --before="$date_to" | awk '{print $3}' | sort -u)
    
    # 各ファイルごとに追加行数と削除行数を集計
    for file in $changed_files; do
        add_lines=$(git log --since="$date_from" --before="$date_to" --pretty=tformat: --numstat -- "$file" | awk '{ add += $1 } END { print add }')
        del_lines=$(git log --since="$date_from" --before="$date_to" --pretty=tformat: --numstat -- "$file" | awk '{ del += $2 } END { print del }')
        echo "$file,$add_lines,$del_lines" >> "$fname"
    done
}

main() {
    start_date="2011-01-01"
    end_date="2024-05-01"

    one_month_from=$start_date
    one_month_to=$(date -j -v+1m -f "%Y-%m-%d" "$start_date" "+%Y-%m-%d")

    output_base_name="git_log_changes_loc"

    # 開始日から終了日まで1ヶ月ごとに繰り返す
    while [ "$(date -j -f "%Y-%m-%d" "$one_month_from" "+%Y%m")" -lt "$(date -j -f "%Y-%m-%d" "$end_date" "+%Y%m")" ]; do

        # 現在の期間を表示
        echo "Processing changes from: $one_month_from to: $one_month_to"

        # 出力ファイル名を設定
        output_file="$output_base_name-$(date -j -f "%Y-%m-%d" "$one_month_from" "+%Y%m").csv"

        # 指定した期間に対してfile_changes_in_rangeを呼び出す
        file_changes_in_range "$one_month_from" "$one_month_to" "$output_file"
        
        # 調査期間を1ヶ月進める
        one_month_from=$one_month_to
        one_month_to=$(date -j -v+1m -f "%Y-%m-%d" "$one_month_to" "+%Y-%m-%d")
    done
}

# main関数を呼び出す
main
