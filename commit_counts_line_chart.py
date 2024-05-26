import csv
import sys

# コマンドライン引数からリポジトリ名を取得
if len(sys.argv) != 2:
    print("Usage: python commit_counts_line_chart.py REPOSITORY_NAME")
    sys.exit(1)

REPOSITORY_NAME = sys.argv[1]


# BASE_PATH = "./result/" + REPOSITORY_NAME + "/git_log_changes/"
BASE_PATH = "./tmp/"  # シェルスクリプト一括実行用
output_csv_fname = "./result/commit_counts_per_month.csv"

start_year = 2011
start_month = 1
end_year = 2024
end_month = 5
file_names = []

commited_months = []
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
        commited_months.append("{}-{:02d}".format(year, month))

csv_columns = ["filename"]
csv_columns.extend(commited_months)

commited_counts = [REPOSITORY_NAME]
for file_name, commited_month in zip(file_names, commited_months):
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()

            changed_counts_sum = 0
            for line in lines[1:]:
                changed_counts_sum += int(line.split()[0])

        commited_counts.append(changed_counts_sum)
    except FileNotFoundError as e:
        print(e)
        commited_counts.append(0)


# csvに追記
with open(output_csv_fname, "a") as f:
    writer = csv.writer(f)

    # writer.writerow(csv_columns)
    writer.writerow(commited_counts)
