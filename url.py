class Url:
    # url = "https://www.kvk.nl/zoeken/?source=all&"
    url = "https://zoeken.kvk.nl/search.ashx?"

    def __init__(self, zip, title):
        self.url = self.url + "q=" + str(zip) + "%20" + title

    def get(self):
        return self.url

    def get_start(self, start):
        return self.url + "&start=" + str(start)
