import json
import scrapy
from datetime import datetime

OUTPUT_FILENAME = 'output/Dantri/Dantri_{}.txt'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))

class VnexpressSpider(scrapy.Spider):
    name = 'Dantri'
    start_urls = ['https://dantri.com.vn/xa-hoi/thu-tuong-xu-ly-sao-voi-o-dich-covid-19-o-do-thi-lon-nhu-ha-noi-tphcm-20200807115954397.htm']
    allowed_domains = ['dantri.com.vn']
    CRAWLED_COUNT = 0

    def parse(self, response):
        print('Crawling from:', response.url)
        data = {
            'link': response.url,
            'description': response.css('h1.dt-news__title::text').get(),
            'dt-news_tital': response.css('h2::text').get(),
            'date & time': response.css('div.dt-news__meta span.dt-news__time::text').get(),
            'content': '\n'.join([
                ''.join(c.css('*::text').getall())
                for c in response.css('div.dt-news__content p')
            ]),

            'keywords': [
                k.strip() for k in response.css('meta[name="keywords"]::attr("content")').get().split(',')
            ],


        }

        with open(OUTPUT_FILENAME, 'a', encoding='utf8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
            f.write('\n')
            self.CRAWLED_COUNT += 1
            self.crawler.stats.set_value('CRAWLED_COUNT', self.CRAWLED_COUNT)
            print('SUCCESS:', response.url)

        yield from response.follow_all(css='a[href^="https://dantri.com.vn/"]::attr(href), a[href^="/"]::attr(href)',callback=self.parse)


