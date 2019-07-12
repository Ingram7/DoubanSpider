# -*- coding: utf-8 -*-

from scrapy import Request
from ..items import *
import json
import random
import string

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['douban.com']

    base_url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start={page}&genres={genres}&year_range={year}&limit=150"
    def start_requests(self):
        genres_list = ['剧情','喜剧','动作','爱情','科幻','动画','悬疑','惊悚','恐怖','犯罪','同性',
                       '音乐','歌舞','传记','历史','战争','西部','奇幻','冒险','灾难','武侠','情色']
        year_list = ['2019,2019','2018,2018','2015,2017','2010,2014','2005,2009','2000,2004',
                     '1990,1999','1980,1989','1970,1979','1960,1969','1,1959']

        for genres in genres_list:
            for year in year_list:
                bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
                cookies ={'bid': bid}
                yield Request(self.base_url.format(page=0, genres=genres, year=year), callback=self.parse,
                            meta={'page': 0, 'genres': genres, 'year': year}, cookies=cookies)

    # 获取电影id，构造电影链接
    def parse(self, response):
        result = json.loads(response.text)
        if len(result.get('data')) != 0:
            for node in result.get('data'):
                id = node.get('id')
                bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
                cookies = {'bid': bid}
                yield Request(url='https://movie.douban.com/subject/{}/'.format(id), callback=self.parse_subject,
                              meta={'id': id}, cookies=cookies)

            page = response.meta['page'] + 20
            genres = response.meta['genres']
            year = response.meta['year']
            yield Request(self.base_url.format(page=page, genres=genres, year=year), callback=self.parse,
                          meta={'page': page, 'genres': genres, 'year': year})

    def parse_subject(self, response):
        item = MovieItem()
        id = response.meta['id']
        item['id'] = id
        # 导演
        directors = ';'.join(response.xpath('//*[@rel="v:directedBy"]/text()').extract())
        if len( directors ) != 0:
            item['directors'] = directors
        else:
            item['directors'] = None
        # 评分
        item['rate'] = response.xpath('//strong[@property="v:average"]/text()').extract_first()
        # 电影名
        item['title'] = response.xpath('//span[@property="v:itemreviewed"]/text()').extract()[0]
        # 主演
        actor = ';'.join(response.xpath('//*[@rel="v:starring"]/text()').extract())
        if len(actor) != 0:
            item['actor'] = actor
        else:
            item['actor'] = None
        # 链接
        item['url'] = 'https://movie.douban.com/subject/{}/'.format(id)
        # 封面链接
        item['cover'] =response.xpath('//*[@rel="v:image"]/@src').extract()[0]
        # 编剧
        scriptwriter = ';'.join(response.xpath('//span[contains(text(),"编剧")]/..//span[@class="attrs"]/a/text()').extract())
        if len(scriptwriter) != 0:
            item['scriptwriter'] = scriptwriter
        else:
            item['scriptwriter'] = None
        # 上映日期
        Date = ';'.join(response.xpath('//span[@property="v:initialReleaseDate"]/text()').extract())
        if len(Date) != 0:
            item['Date'] = Date
        else:
            item['Date'] = None
        # 类型
        item['type'] = '/'.join(response.xpath('//span[@property="v:genre"]//text()').extract())
        # 评分人数
        item['rating_num'] =response.xpath('//span[@property="v:votes"]/text()').extract_first()
        # 制片国家/地区
        try:
            item['region'] = response.xpath('//*[@id="info"]').re('制片国家/地区:</span>\s(.*)<br>')[0]
        except IndexError:
            item['region'] = None
        # 评分语言
        try:
            item['language'] = response.xpath('//*[@id="info"]').re('语言:</span>\s(.*)<br>')[0]
        except IndexError:
            item['language'] = None
        # 片长
        if response.xpath('//span[@property="v:runtime"]/text()').extract():
            item['runtime'] = response.xpath('//span[@property="v:runtime"]/text()').extract()[0]
        elif response.xpath('//*[@id="info"]').re('片长:</span>\s(.*)<br>'):
            item['runtime'] = response.xpath('//*[@id="info"]').re('片长:</span>\s(.*)<br>')[0]
        else:
            item['runtime'] = None
        # IMDb
        try:
            item['IMDb'] = response.xpath('//a[@rel="nofollow" and contains(@href, "www.imdb.com/title/")]/@href').extract()[0]
        except IndexError:
            item['IMDb'] = None

        yield item