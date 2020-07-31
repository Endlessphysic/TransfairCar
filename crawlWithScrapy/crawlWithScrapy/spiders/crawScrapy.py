import scrapy
from scrapy.http import FormRequest
from scrapy.crawler import CrawlerProcess
from ..items import CrawlwithscrapyItem
import json


class PostsSpider(scrapy.Spider):
    name = "posts"
    number = 2
    max_page = 2
    everything = []
    start_urls = [
        'https://portal.onlogist.com/orders?orderBy=deliveryTime&showAll=false&page=1&order=ASC',
    ]

    def parse(self, response):
        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response, formdata={
            'authenticityToken' : token,
            'username' : 'p.kocak@outlook.de',
            'password' : 'Elinar811*#'
        }, callback=self.start_scraping)

    def start_scraping(self, response):
        items = CrawlwithscrapyItem()       #Neue Instanz der Item Klasse
        page = response.url.split('&')[-2]
        orderList = []
        print("---------------" + page + "---------------")
        all_orders1 = response.css('div.table-responsive')
        all_orders = all_orders1.css('.null')

        for order in all_orders:
            price = order.css('span.buynowPrice::text').extract()[0].strip()
            start = order.css('.start_name::text').extract()[0].strip()
            destination = order.css('.destination_name::text').extract()[0].strip()
            items['price'] = price
            items['start'] = start
            items['destination'] = destination
            orderList.append(items.copy())

        PostsSpider.everything.append(orderList.copy())

        next_page = 'https://portal.onlogist.com/orders?orderBy=deliveryTime&showAll=false&page=' + str(PostsSpider.number) + '&order=ASC'
        if PostsSpider.number < PostsSpider.max_page:
            PostsSpider.number += 1
            yield response.follow(next_page, callback=self.start_scraping)

        if (PostsSpider.number == 5):
            return PostsSpider.everything

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })


            # def start_requests(self):
    #     main_url = 'https://portal.onlogist.com/secure/login'
    #     return [
    #         FormRequest(main_url, formdata={"user": "p.kocak@outlook.de", "pass": "Elinar811*#"}, callback=self.parse)]

    # start_urls = [
    #     'https://portal.onlogist.com/secure/login',
    #     'https://portal.onlogist.com/orders?orderBy=deliveryTime&showAll=false&page=1&order=ASC',
    #     'https://portal.onlogist.com/orders?orderBy=deliveryTime&showAll=false&page=2&order=ASC'
    # ]
    #<input type="hidden" name="authenticityToken" value="ed82e4f909d3f1b624512c344537ffe742d8b6ed">
    # def parse(self, response):
    #     page = response.url.split('&')[-1]
    #     filename = 'posts-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
