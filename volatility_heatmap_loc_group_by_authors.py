import csv
import re
from collections import defaultdict

# 著者のグループ分け
GROUP1_AUTHORS = {
    "Author-1",
    "Author-2",
    "Author-3",
    # 他のGroup1所属の著者を追加
}

GROUP2_AUTHORS = {
    "Author-4",
    "Author-5",
    # 他のGroup2所属の著者を追加
}

GROUP3_AUTHORS = {
    "Author-6",
    "Author-7",
    "Author-8",
    # 他のGroup3所属の著者を追加
}

start_year = 2016
start_month = 3
end_year = 2024
end_month = 5
file_names = []

BASE_PATH = "./result/KEEP/git_log_changes_loc/"
OUTPUT_BASE_PATH = "./result/KEEP/git_log_changes_loc/"

# 出力ファイル名
group1_output = f"{OUTPUT_BASE_PATH}group1_{start_year}{start_month:02d}-{end_year}{end_month:02d}.csv"
group2_output = f"{OUTPUT_BASE_PATH}group2_{start_year}{start_month:02d}-{end_year}{end_month:02d}.csv"
group3_output = f"{OUTPUT_BASE_PATH}group3_{start_year}{start_month:02d}-{end_year}{end_month:02d}.csv"

# 開始年月から終了年月までの各年月のファイル名を生成
for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        if (year == start_year and month < start_month) or (
            year == end_year and month > end_month
        ):
            continue
        file_name = f"git_log_changes_loc-{year}{month:02d}.csv"
        file_names.append(BASE_PATH + file_name)

csv_columns = ["filename"]
# key: ファイル名, value: 変更履歴(list: {年月: {author: count}})
changed_files_group1 = defaultdict(dict)
changed_files_group2 = defaultdict(dict)
changed_files_group3 = defaultdict(dict)

for file_name in file_names:
    with open(file_name, "r") as file:
        print(file_name)
        match = re.search(r"\d{6}", file_name)
        extracted_start_date = match.group()
        csv_columns.append(extracted_start_date)
        lines = file.readlines()

        for line in lines[1:]:
            parts = line.strip().split(",")
            changed_filename = parts[0]
            author = parts[1]
            try:
                added_counts = int(parts[2])
                deled_counts = int(parts[3])
            except (ValueError, IndexError):
                continue

            net_changes = added_counts - deled_counts

            # 著者のグループに基づいて適切なディクショナリに追加
            if author in GROUP1_AUTHORS:
                changed_files_group1[changed_filename][extracted_start_date] = net_changes
            elif author in GROUP2_AUTHORS:
                changed_files_group2[changed_filename][extracted_start_date] = net_changes
            elif author in GROUP3_AUTHORS:
                changed_files_group3[changed_filename][extracted_start_date] = net_changes

# 各グループごとにCSVファイルを出力する関数
def write_csv_for_group(output_file, changed_files):
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(csv_columns)

        for file, records in changed_files.items():
            padded_record = [file]
            changed_dates = set(records.keys())

            for date in csv_columns[1:]:
                if date in changed_dates:
                    padded_record.append(records[date])
                else:
                    padded_record.append(0)

            writer.writerow(padded_record)

# 各グループのデータを出力
write_csv_for_group(group1_output, changed_files_group1)
write_csv_for_group(group2_output, changed_files_group2)
write_csv_for_group(group3_output, changed_files_group3)
