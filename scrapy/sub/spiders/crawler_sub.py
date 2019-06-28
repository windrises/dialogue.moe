import scrapy
import time
import json
import collections
import traceback
from pprint import pprint
import random


class MySpider(scrapy.Spider):
    tag = '_sub'
    name = 'crawl' + tag

    def __init__(self):
        super(MySpider, self).__init__()
        tag = self.tag
        print(tag)
        self.out = open('./data' + tag + '/subtitles_info.txt', 'a', encoding='utf-8')
        self.error = open('./data' + tag + '/error.txt', 'a', encoding='utf-8')

        self.out = open('./data' + tag + '/subtitles_info.txt', 'r', encoding='utf-8')
        self.flag = {}
        for x in self.out:
            x = json.loads(x)
            self.flag[x['id']] = 1
        print(len(self.flag.keys()))
        self.out = open('./data' + tag + '/subtitles_info.txt', 'a', encoding='utf-8')

    def start_requests(self):
        data = open('./data_subject/animes_info.txt', encoding='utf-8')
        data = data.readlines()
        # random.shuffle(data)

        for x in data:
            x = json.loads(x)
            sid = x['id']
            if sid in self.flag:
                continue
            self.flag[sid] = 1
            name = x['namechs']
            cat = 0
            if len(name) == 0:
                name = x['namejp']
                cat = 1
            # print(x['id'])
            yield scrapy.Request(url='https://secure.assrt.net/sub/?searchword=' + name + '&sort=relevance&no_redir=1',
                                 callback=self.parse,
                                 meta={'subject': x, 'cat': cat})

    def parse(self, response):
        # print(response.text)
        data = response.meta['subject']
        cat = response.meta['cat']
        subs = response.xpath('//div[@onmouseover="addclass(this,\'subitem_hover\')"]')
        if len(subs) == 0 and cat == 0 and data['namechs'] != data['namejp']:
            yield scrapy.Request(url='https://secure.assrt.net/sub/?searchword=' + data['namejp'] + '&sort=relevance&no_redir=1',
                                 callback=self.parse2,
                                 meta={'subject': data})
        else:
            self.get(subs, data)

    def parse2(self, response):
        data = response.meta['subject']
        subs = response.xpath('//div[@onmouseover="addclass(this,\'subitem_hover\')"]')
        self.get(subs, data)

    def get(self, subs, data):
        # print(subs)
        subs_list = []
        for sub in subs:
            try:
                sub_title = sub.xpath('.//a[@class="introtitle"]/@title').extract()[0]
                sub_url = sub.xpath('.//a[@class="introtitle"]/@href').extract()[0]
                sub_id = sub_url[sub_url.rfind('/')+1:sub_url.find('.')]
                sub_url = 'https://assrt.net' + sub_url
                dl_url = sub.xpath('.//a[@id="downsubbtn"]/@onclick').extract()[0]
                dl_url = dl_url[dl_url.find('\'')+1:dl_url.rfind('\'')]
                dl_url = 'https://assrt.net' + dl_url
                up_date = sub.xpath(u'.//div[@id="sublist_div"]/span[contains(text(), "日期")]/text()').extract()[0]
                up_date = up_date[up_date.find('：')+2:up_date.rfind(' ')]
                dl_cnt = sub.xpath(u'.//div[@id="sublist_div"]/span[contains(text(), "下载次数")]/text()').extract()[0]
                dl_cnt = dl_cnt[dl_cnt.find('：') + 1:dl_cnt.rfind('次')]
                # print(sub_title, sub_url, sud_id, dl_url, up_date, dl_cnt)
                subs_list.append({'sub_id': sub_id,
                                  'sub_title': sub_title,
                                  'sub_url': sub_url,
                                  'up_date': up_date,
                                  'dl_cnt': dl_cnt,
                                  'dl_url': dl_url})
            except:
                traceback.print_exc()
                continue
        data['subs'] = subs_list
        ss = json.dumps(data, ensure_ascii=False)
        self.out.write(str(ss) + '\n')
        self.out.flush()

    def run(self, s):
        return s.strip('\r\n').strip('\n').replace('\r\n', ' ').replace('\n', ' ').replace('\\', '\\\\').replace('"', '\\"')

