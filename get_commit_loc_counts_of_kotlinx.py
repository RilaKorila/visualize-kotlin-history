import glob
import os

import pandas as pd

## get_commit_loc_counts_of_kotlinx で出力したcsvをさらに1つにまとめる


def sort_by_first_non_zero(df):
    """
    DataFrameを0以外の数字が最初に登場するタイミング順に並び替える関数。

    Args:
        df (pd.DataFrame): 並び替え対象のDataFrame。

    Returns:
        pd.DataFrame: 並び替えたDataFrame。
    """

    def find_first_non_zero(row):
        for col in df.columns[1:]:
            if row[col] != 0:
                return col
        return df.columns[-1]  # 全て0の場合は最後の列を返す

    # 新しい列 'first_non_zero' に最初に0以外の数字が登場する列を記録
    df["first_non_zero"] = df.apply(find_first_non_zero, axis=1)

    # 'first_non_zero' 列を基にデータを並び替える
    sorted_df = df.sort_values(by="first_non_zero", ascending=False).drop(
        columns=["first_non_zero"]
    )

    return sorted_df


def main():
    data_dir = "./result/kotlin_organization/"
    dfs = []

    # 全てのCSVファイルを取得
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))

    for csv_file in csv_files:
        repository_name = os.path.splitext(os.path.basename(csv_file))[0]
        df = pd.read_csv(csv_file)

        # リポジトリ名の列を追加
        df["repository"] = repository_name
        dfs.append(df)

    # 全てのデータフレームを結合
    combined_df = pd.concat(dfs)

    # add_linesとdel_linesの差を計算して新しい列を追加
    combined_df["net_lines"] = combined_df["add_lines"] - combined_df["del_lines"]

    sorted_df = sort_by_first_non_zero(combined_df)
    pivot_df = sorted_df.pivot_table(
        index="repository",
        columns="date",
        values="net_lines",
        aggfunc="sum",
        fill_value=0,
    )
    pivot_df.to_csv("commit_loc_counts.csv")


if __name__ == "__main__":
    main()
