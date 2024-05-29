## paths.txtを、ファイルパスに特定の単語をを含むか否かで分割する

# ファイルパスを定義
BASE_PATH = "./result/kotlin/"
input_file = BASE_PATH + "paths.txt"
keyword = "test"
included_output_file = BASE_PATH + f"paths_included_{keyword}.txt"
excluded_output_file = BASE_PATH + f"paths_excluded_{keyword}.txt"

# paths.txtを読み込み
with open(input_file, "r") as file:
    paths = file.readlines()

# 含むパスと含まないパスに分割
included_paths = [path for path in paths if keyword in path.lower()]
excluded_paths = [path for path in paths if keyword not in path.lower()]

# 含むパスをファイルに書き込み
with open(included_output_file, "w") as file:
    file.writelines(included_paths)

# 含まないパスをファイルに書き込み
with open(excluded_output_file, "w") as file:
    file.writelines(excluded_paths)

print(f'Paths containing "{keyword}" are written to {included_output_file}')
print(f'Paths not containing "{keyword}" are written to {excluded_output_file}')
