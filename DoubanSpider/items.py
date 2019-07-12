# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class BookReviewLatestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    review = Field()
    book = Field()
    user_name = Field()
    useful_count = Field()
    review_url = Field()
    id = Field()

class MovieItem(scrapy.Item):
    collection = 'Movie'

    directors = Field()             # 导演
    rate = Field()                  # 评分
    title = Field()                 # 电影名
    url = Field()                   # 链接
    actor = Field()                 # 主演
    cover = Field()                 # 封面链接
    id = Field()                    # 电影id
    scriptwriter = Field()          # 编剧
    Date = Field()                  # 上映日期
    type = Field()                  # 类型
    region = Field()                # 制片国家/地区
    runtime = Field()               # 片长
    language = Field()              # 语言
    rating_num = Field()            # 评分人数
    IMDb = Field()                  # IMDb
    crawled_at = Field()            # 时间戳