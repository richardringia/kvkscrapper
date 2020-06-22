from search import Search
from excel import Excel
from search2 import Search2


def main():
    posts = []
    start = 8401
    i = start
    while i < 8430:
        search = Search2(i, "vve")
        search.scrap()
        for post in search.get_posts():
            posts.append(post)
        i += 1

    # search2 = Search2(8401, "vve")
    # search2.scrap()
    # search2.getBende()

    # for post in search2.get_posts():
    #     posts.append(post)

    # search = Search(9000, "vve")
    # for post in search.posts:
    #     posts.append(post)

    # print(posts)

    excel = Excel(posts, 8401, 8420)


if __name__ == '__main__':
    main()
