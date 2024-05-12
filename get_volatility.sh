#!/bin/bash

start_date="2016-06-01"
end_date="2024-05-01"

one_month_from=$start_date
one_month_to=$(date -j -v+1m -f "%Y-%m-%d" "$start_date" "+%Y-%m-%d")

output_base_name="git_log_changes"

# 開始日から終了日まで1ヶ月ごとに繰り返す
while [ "$(date -j -f "%Y-%m-%d" "$one_month_from" "+%Y%m")" -lt "$(date -j -f "%Y-%m-%d" "$end_date" "+%Y%m")" ]; do

    # 現在の期間を表示
    echo "Processing changes from: $one_month_from to: $one_month_to"

    # 出力ファイル名を設定
    output_file="$output_base_name-$(date -j -f "%Y-%m-%d" "$one_month_from" "+%Y%m").txt"

    # 期間内のコミットログを取得して、変更されたファイルのリストを取得
    git_log_output=$(git log --since="$one_month_from" --until="$end_date" --format=format: --name-only)
    sleep 5
    
    # ファイルに書き込む
    echo "Changes from $one_month_from to $one_month_to:" >> "$output_file"
    echo "$git_log_output" | egrep -v '^$' | sort | uniq -c | sort -r >> "$output_file"

    # 調査期間を1ヶ月進める
    one_month_from=$one_month_to
    one_month_to=$(date -j -v+1m -f "%Y-%m-%d" "$one_month_to" "+%Y-%m-%d")
done

echo "Finished processing changes."
