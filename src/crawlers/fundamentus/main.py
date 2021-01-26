import os
import re
import json
import scrapy
from scrapy.crawler import CrawlerProcess


class FundamentusSpider(scrapy.Spider):

    name = "fundamentus_spider"

    def start_requests(self):

        # Set number of pages to download on range(1, x)
        urls = ['https://www.fundamentus.com.br/fr.php?&pg=%s' % i for i in range (1, 12)]

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

        for url in urls:
            yield scrapy.Request( url=url, callback=self.parse_front, headers=headers )

    def parse_front(self, response):

        # Main Table
        news_table = response.css('table#comunicados > tbody')

        # Loop over rows
        for i in range(1, len(news_table.css('tr')) + 1):

            data_row = news_table.css('tr:nth-of-type(%s)' % i)

            news_date_ext = data_row.css('td.dth-entrega ::text').get().replace('  ', ' ')
            news_company_ext = data_row.css('td:nth-of-type(2)::text').get()
            news_title_ext = data_row.css('td.descricao::text').get()
            news_type_ext = data_row.css('td.col-tipo::text').get()
            news_url_ext = data_row.css('td.download > a::attr(href)').get().strip()
            news_ticker_ext = data_row.css('td:nth-of-type(6) > a::text').get().strip()

            # JSON final
            results_dict = dict()

            results_dict['date'] = news_date_ext
            results_dict['company'] = news_company_ext
            results_dict['title'] = news_title_ext
            results_dict['type'] = news_type_ext
            results_dict['url'] = news_url_ext
            results_dict['ticker'] = news_ticker_ext

            results_list.append(results_dict)


if __name__ == '__main__':

    THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    filename = 'fundamentus'

    # List to save the data collected
    results_list = list()

    # Initiate a CrawlerProcess
    process = CrawlerProcess()

    # Tell the process which spider to use
    process.crawl(FundamentusSpider)

    # Start the crawling process
    process.start()

    # Save the list of dicts
    with open(os.path.join(THIS_DIR + '/data/results-{}.json'.format(filename)), 'w', encoding='utf8') as f:
        json.dump(results_list, f, ensure_ascii=False)