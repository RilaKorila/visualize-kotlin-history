import csv
import re
from collections import defaultdict

start_year = 2014
start_month = 1
end_year = 2024
end_month = 6
file_names = []

BASE_PATH = "./result/KEEP/git_log_changes/"
output_csv_fname = "./result/KEEP/git_hisitory_logs_each_month.csv"

# 開始年月から終了年月までの各年月のファイル名を生成
for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        # 開始年月と終了年月の範囲内の場合にのみファイル名を生成
        if (year == start_year and month < start_month) or (
            year == end_year and month > end_month
        ):
            continue
        file_name = "git_log_changes-{}{:02d}.txt".format(year, month)
        file_names.append(BASE_PATH + file_name)

csv_columns = ["filename"]
# key: ファイル名, value: 変更履歴(list: {年月: 回数})
changed_files = defaultdict(dict)

for file_name in file_names:
    try:
        with open(file_name, "r") as file:
            match = re.search(r"\d{6}", file_name)
            extracted_start_date = match.group()
            csv_columns.append(extracted_start_date)
            lines = file.readlines()

            for line in lines[1:]:
                changed_count = int(line.split()[0])
                changed_filename = line.split()[1]
                changed_files[changed_filename][extracted_start_date] = changed_count
    except FileNotFoundError as e:
        print(e)

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
