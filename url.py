class Url:
    url = "https://www.kvk.nl/zoeken/?source=all"

    def __init__(self, zip, title):
        self.url = self.url + "&q=" + str(zip) + "%20" + title

    def get(self):
        return self.url
