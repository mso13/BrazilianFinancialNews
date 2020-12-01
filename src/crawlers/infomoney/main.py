import re
import json
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest


class InfoMoneySpider(scrapy.Spider):

    name = "infomoney_spider"

    def start_requests(self):

        data = list()

        # URL to POST request
        url_base = 'https://www.infomoney.com.br/?infinity=scrolling'

        # Set number of pages to download on range(1, x)
        for i in range(1, 10):

            params = dict()
            params['action'] = 'infinite_scroll'
            params['page'] = str(i)
            params['order'] = 'DESC'

            data.append(params)

        for form_data in data:
            yield FormRequest(url=url_base, callback=self.parse_front, formdata=form_data,
                                     cb_kwargs=dict(metadata=form_data), dont_filter=True, headers={'Content-Type': 'application/x-www-form-urlencoded','charset':'UTF-8'})

    def parse_front(self, response, metadata):

        # Narrow in on the news cards (10 cards per page)
        news_cards = response.css('div')

        # Direct to news links
        news_links = news_cards.xpath('./a/@href')

        # Extract the links (as a list of strings)
        links_to_follow = news_links.extract()

        # Follow the links to the next parser
        for url in links_to_follow:
            yield response.follow(url=url.replace('\\', ''), callback=self.parse_pages)

    def parse_pages(self, response):

        # Direct to the news title text
        news_title = response.xpath('//h1[contains(@class,"page-title-1")]/text()')

        # Extract and clean the news title text
        news_title_ext = news_title.extract_first().strip()

        # Direct to the news date
        news_date = response.xpath('//div[contains(@class, "author-info-container")]//time/text()')

        # Extract the news date
        news_date_ext = news_date.extract_first().strip()

        # Direct to the news tags
        news_tags = response.css('ul.article-terms li a ::text')

        # Extract the news tags
        news_tags_ext = [t.strip() for t in news_tags.extract()]

        # Extract main topic from URL
        full_url = response.url

        m = re.search('https://www.infomoney.com.br/(.+?)/', full_url)
        if m:
            main_topic = m.group(1)
        else:
            main_topic = ''

        # Save all the data collected
        results_dict = dict()

        results_dict['topic'] = main_topic
        results_dict['title'] = news_title_ext
        results_dict['date'] = news_date_ext
        results_dict['link'] = response.url
        results_dict['tags'] = news_tags_ext

        results_list.append(results_dict)


if __name__ == '__main__':

    # List to save the data collected
    results_list = list()

    # Initiate a CrawlerProcess
    process = CrawlerProcess()

    # Tell the process which spider to use
    process.crawl(InfoMoneySpider)

    # Start the crawling process
    process.start()

    # Save the list of dicts
    with open('data/results-infomoney.json', 'w', encoding='utf8') as f:
        json.dump(results_list, f, ensure_ascii=False)