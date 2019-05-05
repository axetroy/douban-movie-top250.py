from scrapy import Request, Spider, Field
import json
import csv
import urllib
import os.path
import re
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-HK;q=0.7'
}

domain = "https://movie.douban.com"


class DoubanMovieSpider(Spider):
    name = 'douban_movie'
    start_urls = [domain + '/top250']

    DEFAULT_REQUEST_HEADERS = HEADERS

    def start_requests(self):
        fields = [
            '电影名',  # 仅有一个
            '别名',  # 不同地区名称不同，以 | 分割
            '上映日期',  # 多个地区可能是不同的上映日期，以 | 分割
            '导演',  # 有可能有多个导演, 以 | 分割
            '演员',  # 多个演员以 | 分割
            '片长',  # 分钟数
            "语言",
            "类型",  # 多个类型以 | 分割
            "地区",  # 多个地区以 | 分割
            "综合评分",
            "评分人数",
        ]

        # if not exists
        if not os.path.exists('./dist/data.csv'):
            with open(r'./dist/data.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)

        for url in self.start_urls:
            yield Request(url=url, headers=HEADERS)

    def parseDetail(self, response):
        def extract(xpath):
            return response.selector.xpath(xpath).extract_first()

        movie_info = response.selector.xpath(
            '//div[@id="info"]').xpath('string(.)').extract_first()

        score = response.selector.xpath(
            '//strong[@class="ll rating_num"]/text()').extract_first()

        properties = map(
            str.strip,
            movie_info.split('\n')
        )

        properties = [x for x in properties if x != '']

        name = extract('//div[@id="content"]/h1/span/text()')  # 电影名
        directors = ''  # 导演们
        screenwriter = ''  # 编剧们
        actors = ''  # 演员们
        types = ''  # 影片类型
        alias = ''  # 影片别名

        for v in properties:

            directorNameMatchObj = re.match(r'^导演:\s(.*)', v)
            if directorNameMatchObj:
                directors = '|'.join(
                    list(
                        map(str.strip, directorNameMatchObj.group(1).split('/'))
                    )
                )

            screenwriterNameMatchObj = re.match(r'^编剧:\s(.*)', v)
            if screenwriterNameMatchObj:
                screenwriter = '|'.join(
                    list(
                        map(str.strip, screenwriterNameMatchObj.group(1).split('/'))
                    )
                )

            actorsNameMatchObj = re.match(r'^主演:\s(.*)', v)
            if actorsNameMatchObj:
                actors = '|'.join(
                    list(
                        map(str.strip, actorsNameMatchObj.group(1).split('/'))
                    )
                )

            typesMatchObj = re.match(r'^类型:\s(.*)', v)
            if typesMatchObj:
                types = '|'.join(
                    list(
                        map(str.strip, typesMatchObj.group(1).split('/'))
                    )
                )

            aliasNameMatchObj = re.match(r'^又名:\s(.*)', v)
            if aliasNameMatchObj:
                alias = '|'.join(
                    list(
                        map(str.strip, aliasNameMatchObj.group(1).split('/'))
                    ))

        print(name, directors, score)

    # 解析电影列表
    def parse(self, response):

        movieLinks = response.selector.xpath(
            '//div[@class="info"]//a/@href'
        ).extract()

        for link in movieLinks:
            yield response.follow(link, self.parseDetail, headers=HEADERS)

        next_page_query = response.selector.xpath(
            '//span[@class="next"]/a/@href').extract_first()

        if next_page_query is not None:
            next_page_url = domain + '/top250' + next_page_query
            yield response.follow(next_page_url, self.parse, headers=HEADERS)
