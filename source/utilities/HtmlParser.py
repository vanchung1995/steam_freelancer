from lxml import etree
from urllib.request import urlopen
class HtmlParser():
    def __init__(self):
        self.parser = etree.HTMLParser()

    def parse(self, url):
        response = urlopen(url)
        tree = etree.parse(response, self.parser)
        return tree

    def getElemsByXpath(self, tree, xpath):
        return tree.xpath(xpath)

if __name__ == '__main__':
    html = HtmlParser()
    url = 'https://finance.yahoo.com/quote/AAPL'
    xpath = '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[4]/div/div/div/div[3]/div[1]/div/span[1]'
    tree = html.parse(url)
    print(html.getElemsByXpath(tree,xpath)[0].text)
