# visualize-kotlin-history

## GitHubの履歴から調べる

### Software Design X-raysを参考に

> git log --format=format: --name-only | egrep -v '^$' | sort | uniq -c | sort -r | head -5

## Emergeを参考にdependency graphを可視化

### 使用したライブラリ

[Emerge](https://github.com/glato/emerge) (このライブラリに付随する論文はなし)

### 現時点の不明点

- 色, clustering手法
- Testに関する

### 改善させるなら

- clustering に基づくレイアウト
- Test系のファイルを分離 or グレーアウト
- サブグラフの抽出
- 別のversionとの比較のためにkey nodeを指定(dynamic graphとみなして可視化)

### 他の手法の候補

- [repositories related to dependency graph](https://github.com/topics/dependency-graph)
    - scabbard
        - graphvisを使っている点で有力候補
        - json exportも可能
        - 実行方法が若干不明(coroutineの指定versionがうまくいかず一旦保留)
- code property graph
    - [code](https://github.com/Fraunhofer-AISEC/cpg)
    - [論文](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6956589&casa_token=jBAMWOOlhx4AAAAA:iww2hXLSL_2bRvwIolenlAICOuYUgIdLTg90ZHRXXLocMZ4TlF9XxWdGKF1VaaGPadhWpdyKDjcoAg)
- [github api](https://docs.github.com/ja/code-security/supply-chain-security/understanding-your-software-supply-chain/about-the-dependency-graph)?


## 資料
- coroutine: https://speakerdeck.com/n_takehata/sabasaidodefalsekotlin-coroutines
