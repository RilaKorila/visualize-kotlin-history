import csv
import re
from collections import defaultdict

start_year = 2016
start_month = 3
end_year = 2024
end_month = 5
file_names = []

BASE_PATH = "./result/KEEP/git_log_changes_loc/"
output_csv_fname = "./result/KEEP/git_log_changes_loc/201603-202405.csv"

# 開始年月から終了年月までの各年月のファイル名を生成
for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        # 開始年月と終了年月の範囲内の場合にのみファイル名を生成
        if (year == start_year and month < start_month) or (
            year == end_year and month > end_month
        ):
            continue
        file_name = "git_log_changes_loc-{}{:02d}.csv".format(year, month)
        file_names.append(BASE_PATH + file_name)

csv_columns = ["filename"]
# key: ファイル名, value: 変更履歴(list: {年月: 回数})
changed_files = defaultdict(dict)

for file_name in file_names:
    with open(file_name, "r") as file:
        print(file_name)
        match = re.search(r"\d{6}", file_name)
        extracted_start_date = match.group()
        csv_columns.append(extracted_start_date)
        lines = file.readlines()

        for line in lines[1:]:
            changed_filename = line.split(",")[0]
            # FIXME ファイル名に{ }が含まれていると集計に失敗している
            try:
                added_counts = int(line.split(",")[1])
            except ValueError:
                added_counts = 0

            try:
                deled_counts = int(line.split(",")[2])
            except ValueError:
                deled_counts = 0

            if added_counts == "" or deled_counts == "":
                changed_files[changed_filename][extracted_start_date] = 0
                continue

            changed_files[changed_filename][extracted_start_date] = (
                added_counts - deled_counts
            )

# csvで出力
# 縦軸: filename, 横軸: changed_date, セルの中: changed_counts
with open(output_csv_fname, "w") as f:
    writer = csv.writer(f)
    writer.writerow(csv_columns)

    for file, records in changed_files.items():
        # if file.split(".")[-1] != "kt":
        #     # 拡張子がkt以外はskip
        #     continue
        padded_record = [file]
        changed_dates = set(records.keys())

        for date in csv_columns[1:]:
            if date in changed_dates:
                padded_record.append(records[date])
            else:
                padded_record.append(0)

        writer.writerow(padded_record)
