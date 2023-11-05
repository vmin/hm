# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class MyCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    data = scrapy.Field()
    h1 = scrapy.Field()

class MySpider(scrapy.Spider):
    name = "myspider"
    
    start_urls = ['https://www2.hm.com/en_gb/productpage.1170404004.html',
 'https://www2.hm.com/en_gb/productpage.1089156007.html',
 'https://www2.hm.com/en_gb/productpage.1170404001.html',
 'https://www2.hm.com/en_gb/productpage.1172927001.html',
 'https://www2.hm.com/en_gb/productpage.0992208020.html',
 'https://www2.hm.com/en_gb/productpage.1191555003.html',
 'https://www2.hm.com/en_gb/productpage.1160917001.html',
 'https://www2.hm.com/en_gb/productpage.0992208017.html',
 'https://www2.hm.com/en_gb/productpage.0992208018.html',
 'https://www2.hm.com/en_gb/productpage.1207898001.html']
        
    script = """
        function main(splash, args)
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3")
            local ok, reason = splash:go(args.url)
            if not ok then
                return {
                    error = "Failed to navigate: " .. reason,
                }
            end
            
            local result = {}
            pcall(function()
                result['data'] = splash:evaljs('productArticleDetails')
            end)

            local h1_element = splash:select('h1')
            if h1_element then
                result['h1'] = h1_element:text()
            end
            
            return result
        end
    """
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'lua_source': self.script}, endpoint='execute')
            
    def parse(self, response):
        if 'error' in response.data:
            self.logger.error('Error while accessing the URL: %s', response.data['error'])
        elif 'data' not in response.data:
            self.logger.error('Error while accessing the data field for the URL: %s.', response.url)
        elif 'h1' not in response.data:
            self.logger.error('Error while accessing the h1 field for the URL: %s.', response.url)
        else:
            item = MyCrawlerItem()
            item['url'] = response.url
            item['data'] = response.data['data']
            item['h1'] = response.data['h1']
            yield item
