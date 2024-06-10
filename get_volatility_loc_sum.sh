#!/bin/bash

# リポジトリ全体で指定された期間の追加行数と削除行数を集計
# (get_volatility_loc.shではファイルごとの追加行数と削除行数を集計)

start_date="2014-01-01"
end_date="2024-06-01"

one_month_from=$start_date
one_month_to=$(date -j -v+1m -f "%Y-%m-%d" "$start_date" "+%Y-%m-%d")

output_file="git_log_changes_loc_sum_per_month.csv"
echo "date,add_lines,del_lines" >> "$output_file"

# 開始日から終了日まで1ヶ月ごとに繰り返す
while [ "$(date -j -f "%Y-%m-%d" "$one_month_from" "+%Y%m")" -lt "$(date -j -f "%Y-%m-%d" "$end_date" "+%Y%m")" ]; do

    # 現在の期間を表示
    echo "Processing changes from: $one_month_from to: $one_month_to"

    add_lines=$(git log --since="$one_month_from" --before="$one_month_to" --pretty=tformat: --numstat | awk '{ add += $1 } END { print add }')
    del_lines=$(git log --since="$one_month_from" --before="$one_month_to" --pretty=tformat: --numstat | awk '{ del += $2 } END { print del }')

    echo "$one_month_from,$add_lines,$del_lines" >> "$output_file"
    
    # 調査期間を1ヶ月進める
    one_month_from=$one_month_to
    one_month_to=$(date -j -v+1m -f "%Y-%m-%d" "$one_month_to" "+%Y-%m-%d")
done
