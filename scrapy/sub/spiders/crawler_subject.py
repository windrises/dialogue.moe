import scrapy
import time
import json
import collections
import traceback
from pprint import pprint
import random


def get_cookie():
    s = '***'
    cookie = {}
    s = s.replace(' ', '').split(';')
    for x in s:
        x = x.split('=')
        cookie[x[0]] = x[1]
    return cookie


class MySpider(scrapy.Spider):
    tag = '_subject'
    name = 'crawl' + tag

    def __init__(self):
        super(MySpider, self).__init__()
        tag = self.tag
        print(tag)
        self.out = open('./data' + tag + '/animes_info.txt', 'a', encoding='utf-8')
        self.error = open('./data' + tag + '/error.txt', 'a', encoding='utf-8')

        self.out = open('./data' + tag + '/animes_info.txt', 'r', encoding='utf-8')
        self.flag = {}
        for x in self.out:
            x = json.loads(x)
            self.flag[x['id']] = 1
        print(len(self.flag.keys()))
        self.out = open('./data' + tag + '/animes_info.txt', 'a', encoding='utf-8')

    def start_requests(self):
        cookie = get_cookie()
        for i in range(1, 285462):
            yield scrapy.Request(url='https://bgm.tv/subject/' + str(i),
                                 callback=self.parse, cookies=cookie)

    def parse(self, response):
        id = response.url
        id = id[id.rfind('/') + 1:]
        message = response.xpath('//*[@id="colunmNotice"]/div/h2/text()').extract()
        if len(message) != 0:
            self.error.write(id + '\n')
            self.error.flush()
            return
        # if self.has.has_key(int(id)) == True:
        #     return
        sub_cat = response.xpath('//a[@class="focus chl"]/@href').extract()
        if len(sub_cat) == 0:
            sub_cat = response.xpath('//a[@class="focus chl anime"]/@href').extract()
        if len(sub_cat) == 0:
            sub_cat = response.xpath('//a[@class="focus chl real"]/@href').extract()
        if len(sub_cat) == 0:
            self.error.write('--------' + id + '\n')
            self.error.flush()
            return
        sub_cat = sub_cat[0]
        sub_cat = sub_cat[1:]

        img = response.xpath('//div[@id="bangumiInfo"]/div/div/a/img/@src').extract()
        namechs = response.xpath(u'//span[./text()="中文名: "]/following::text()[1]').extract()
        namejp = response.xpath('//h1[@class="nameSingle"]/a/text()').extract()
        cat = response.xpath('//h1[@class="nameSingle"]/small/text()').extract()

        all = []
        allkey = []

        if sub_cat != 'anime':
            return
        eps = response.xpath(u'//span[./text()="话数: "]/following::text()[1]').extract()
        date = response.xpath(u'//span[./text()="放送开始: "]/following::text()[1]').extract()
        if len(date) == 0:
            date = response.xpath(u'//span[./text()="上映年度: "]/following::text()[1]').extract()
        if len(date) == 0:
            date = response.xpath(u'//span[./text()="发售日: "]/following::text()[1]').extract()
        all = [namechs, namejp, cat, eps, date, star, rank, votes, author, director, personset, img]
        allkey = ['namechs', 'namejp', 'cat', 'eps', 'date', 'img']

        data = collections.OrderedDict()
        data['id'] = id
        data['sub_cat'] = sub_cat
        for i in range(0, len(all)):
            if len(all[i]) >= 1:
                data[allkey[i]] = all[i][0].strip('\r\n').strip('\n').replace('\r\n', ' ').replace('\n', ' ').replace('\\', '\\\\').replace('"', '\\"')
            else:
                data[allkey[i]] = ''

        ss = json.dumps(data, ensure_ascii=False)
        self.out.write(str(ss) + '\n')
        self.out.flush()
