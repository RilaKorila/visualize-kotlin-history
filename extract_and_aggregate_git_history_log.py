import pandas as pd

EXTRACTED_CSV_FILE = "./result/kotlin/extracted_git_hisitory_logs_each_month.csv"
AGGREGATED_CSV_FILE = "./result/kotlin/aggregated_git_hisitory_logs_each_month.csv"
GIT_LOG_CSV_FILE = "./result/kotlin/git_hisitory_logs_each_month.csv"
PATHS_FILE = "./result/kotlin/paths.txt"
CUT_LAYER_LEBEL = 2

## path.txtの取得方法
## find "$(pwd)" > paths.txt


def __extract_current_repository_files():
    df = pd.read_csv(GIT_LOG_CSV_FILE)
    print(df.shape[0])

    with open(PATHS_FILE, "r") as file:
        paths = file.read().splitlines()

    filtered_df = df[df["filename"].isin(paths)]
    filtered_df.to_csv(EXTRACTED_CSV_FILE, index=False)

    print(filtered_df.shape[0])
    return filtered_df


# 指定された階層までのパスを抽出する関数
def __get_cut_path(path):
    parts = path.split("/")
    return (
        "/".join(parts[:CUT_LAYER_LEBEL]) if len(parts) > CUT_LAYER_LEBEL - 1 else path
    )


filtered_df = __extract_current_repository_files()

# 指定された階層までのパスを新しい列に追加
filtered_df["n_level_path"] = filtered_df["filename"].apply(__get_cut_path)

# 合計する列名をリストとして取得（filenameとn_level_pathを除く全ての列）
columns_to_sum = [
    col for col in filtered_df.columns if col not in ["filename", "n_level_path"]
]

# 2階層までのパスでグループ化し、指定された列を合計
aggregated_df = filtered_df.groupby("n_level_path")[columns_to_sum].sum().reset_index()

# n_level_pathをfilenameにリネーム
aggregated_df.rename(columns={"n_level_path": "filename"}, inplace=True)


aggregated_df.to_csv(AGGREGATED_CSV_FILE, index=False)
print("フィルタリングと集計が完了しました。\n" + "open " + AGGREGATED_CSV_FILE)
