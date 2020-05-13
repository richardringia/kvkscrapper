from search import Search
from excel import Excel

def main():
    search = Search(8401, "vve")
    print(len(search.posts))

    excel = Excel(search.posts)


if __name__ == '__main__':
    main()
