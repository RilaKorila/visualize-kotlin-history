import csv
import datetime
from collections import defaultdict

import matplotlib.pyplot as plt

TOP_N = 10

commit_counts_by_month = defaultdict(dict)
commit_all_counts = defaultdict(int)

start_year = 2008
start_month = 10
end_year = 2024
end_month = 5

months = []
for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        if (year == start_year and month < start_month) or (
            year == end_year and month > end_month
        ):
            continue
        dt = datetime.datetime(year, month, 1)
        months.append(dt.strftime("%Y-%m"))


authors = set()

with open("./result/kotlin/authors.csv", "r") as f:
    reader = csv.reader(f)
    for line in reader:
        author, date_str = line

        # dictの初期化
        if author not in authors:
            authors.add(author)
            for month in months:
                commit_counts_by_month[author][month] = 0

        date = datetime.datetime.strptime(date_str.strip(), "%a %b %d %H:%M:%S %Y %z")
        month_key = date.strftime("%Y-%m")

        commit_counts_by_month[author][month_key] += 1
        commit_all_counts[author] += 1

## authorごとのcommit数を示す棒グラフ

### 全体のグラフ
sorted_commits = sorted(commit_all_counts.items(), key=lambda x: x[1], reverse=True)
authors = [item[0] for item in sorted_commits]
counts = [item[1] for item in sorted_commits]
print("commiter 総数: ", len(authors))

# 棒グラフを作成
plt.figure(figsize=(20, 6))
plt.bar(authors, counts)

# グラフの装飾
plt.xlabel("Author")
plt.ylabel("Number of Commits")
plt.title("Number of Commits by Author")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("counts_by_author.png")
plt.clf()


### top30の棒グラフ
#####
top_10_authors = sorted_commits[:10]
authors = [item[0] for item in sorted_commits[:30]]
counts = [item[1] for item in sorted_commits[:30]]
print(sorted_commits[:30])

# 棒グラフを作成
plt.figure(figsize=(20, 6))
plt.bar(authors, counts)

# グラフの装飾
plt.xlabel("Author")
plt.ylabel("Number of Commits")
plt.title("Number of Commits by Author")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("counts_by_author.png")
plt.clf()


### top10のcommiterの動きを折れ線グラフで可視化
# コミット数の多いauthorを特定する
top_10_authors = sorted_commits[:10]
print(top_10_authors)
plt.figure(figsize=(20, 10))

for author in commit_counts_by_month.keys():
    if author in set(top_10_authors):
        counts = [commit_counts_by_month[author].get(month, 0) for month in months]

        author_commits = [
            count_dict[month]
            for auth, count_dict in commit_counts_by_month.items()
            if auth == author
        ]
        plt.plot(months, counts, label=author)

# グラフの装飾
plt.xlabel("Month")
plt.ylabel("Number of Commits")
plt.title("Commits per Month by Alexander Udalov")
plt.xticks(rotation=45)
plt.legend()

plt.savefig("commit_hisotry.png")


### 1人ずつline chartを出す
def draw_line_chart_of(name):
    plt.figure(figsize=(20, 10))

    counts = []
    for author in commit_counts_by_month.keys():
        if author == name:
            counts = [commit_counts_by_month[author].get(month, 0) for month in months]
            plt.plot(months, counts, label=author)

    # グラフの装飾
    plt.xlabel("Month")
    plt.ylabel("Number of Commits")
    plt.title("Commits per Month by " + name)
    plt.xticks(rotation=45)
    plt.ylim(0, 140)
    plt.legend()

    plt.savefig("commit_hisotry_" + name + ".png")


### kotlin の top30
draw_line_chart_of("Alexander Udalov")
draw_line_chart_of("Mikhail Glukhikh")
draw_line_chart_of("Nikolay Krasko")
draw_line_chart_of("Andrey Breslav")
draw_line_chart_of("Dmitriy Novozhilov")
draw_line_chart_of("Valentin Kipyatkov")
draw_line_chart_of("Ilya Gorbunov")
draw_line_chart_of("Evgeny Gerashchenko")
draw_line_chart_of("Alexey Sedunov")
draw_line_chart_of("Ilya Kirillov")
draw_line_chart_of("Denis Zharkov")
draw_line_chart_of("Yan Zhulanow")
draw_line_chart_of("Pavel V. Talanov")
draw_line_chart_of("Dmitry Petrov")
draw_line_chart_of("Dmitry Jemerov")
draw_line_chart_of("Ilya Chernikov")
draw_line_chart_of("Alexey Tsvetkov")
draw_line_chart_of("Ilya Goncharov")
draw_line_chart_of("Mikhael Bogdanov")
draw_line_chart_of("Zalim Bashorov")
draw_line_chart_of("Svyatoslav Scherbina")
draw_line_chart_of("Dmitriy Dolovov")
draw_line_chart_of("Svetlana Isakova")
draw_line_chart_of("Mikhail Zarechenskiy")
draw_line_chart_of("Ilya Matveev")
draw_line_chart_of("Dmitrii Gridin")
draw_line_chart_of("Vyacheslav Gerasimov")
draw_line_chart_of("Yahor Berdnikau")
draw_line_chart_of("Igor Chevdar")
draw_line_chart_of("Dmitry Gridin")

## kotlinx.coroutinesのtop30
# draw_line_chart_of('Roman Elizarov')
# draw_line_chart_of('Vsevolod Tolstopyatov')
# draw_line_chart_of('Sergey Mashkov')
# draw_line_chart_of('Dmitry Khalanskiy')
# draw_line_chart_of('dkhalanskyjb')
# draw_line_chart_of('Denis Zharkov')
# draw_line_chart_of('Nikita Koval')
# draw_line_chart_of('Margarita Bobova')
# draw_line_chart_of('Victor Turansky')
# draw_line_chart_of('Louis CAD')
# draw_line_chart_of('mvicsokolova')
# draw_line_chart_of('Danil Pavlov')
# draw_line_chart_of('Masood Fallahpoor')
# draw_line_chart_of('Sean McQuillan')
# draw_line_chart_of('Francesco Vasco')
# draw_line_chart_of('Ilya Gorbunov')
# draw_line_chart_of('Victoria Petrakovich')
# draw_line_chart_of('Yanis Batura')
# draw_line_chart_of('paolop')
# draw_line_chart_of('Sebastian Aigner')
# draw_line_chart_of('Victoria.Petrakovich')
# draw_line_chart_of('Konrad Kamiński')
# draw_line_chart_of('Nikita Bobko')
# draw_line_chart_of('Marek Langiewicz')
# draw_line_chart_of('Inego')
# draw_line_chart_of('Dmitry Borodin')
# draw_line_chart_of('Wojtek Kaliciński')
# draw_line_chart_of('SokolovaMaria')
# draw_line_chart_of('Pavel Semyonov')
# draw_line_chart_of('koshachy')
