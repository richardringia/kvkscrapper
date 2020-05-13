import xlsxwriter


class Excel:

    def __init__(self, posts):
        workbook = xlsxwriter.Workbook('hello.xlsx')
        worksheet = workbook.add_worksheet()

        counter = 2

        worksheet.write('A1', 'Naam')
        worksheet.write('B1', 'KVK')

        for post in posts:
            worksheet.write('A' + str(counter), post.name)
            worksheet.write('B' + str(counter), post.kvk)
            counter += 1

        workbook.close()