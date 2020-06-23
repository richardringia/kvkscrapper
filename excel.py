import xlsxwriter


class Excel:

    def __init__(self, posts, start, end):
        workbook = xlsxwriter.Workbook('output/' + str(start) + ' - ' + str(end) + '.xlsx')
        worksheet = workbook.add_worksheet()

        counter = 2

        worksheet.write('A1', 'Naam')
        worksheet.write('B1', 'KVK')
        worksheet.write('C1', 'Adres')
        worksheet.write('D1', 'Postcode')
        worksheet.write('E1', 'Woonplaats')

        for post in posts:
            worksheet.write('A' + str(counter), post.name)
            worksheet.write('B' + str(counter), post.kvk)
            worksheet.write('C' + str(counter), post.address)
            worksheet.write('D' + str(counter), post.zip)
            worksheet.write('E' + str(counter), post.city)
            counter += 1

        workbook.close()
