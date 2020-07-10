# -*- coding: utf-8 -*-
import scrapy
from lianjiaSpider.items import LianjiaspiderItem
import re


class LianjiazufangSpider(scrapy.Spider):
    name = 'lianjiazufang'
    allowed_domains = ['lianjia.com']

    def get_list(self, city):
        import requests
        def get_html(url):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4167.0 Safari/537.36"
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return response.content.decode()
            except:
                pass
            return ''

        from lxml import etree
        url = f'https://{city}.lianjia.com/zufang'
        html = get_html(url)
        base_url = f"https://{city}.lianjia.com/"
        from urllib.parse import urljoin
        if html:
            mytree = etree.HTML(html)
            areas_list = mytree.xpath("//div[@id=\"filter\"]//ul[2]//li/a")
            area_info = []
            for area in areas_list:
                area_name = area.xpath("./text()")[0]
                area_link = area.xpath("./@href")[0]

                if area_name == '不限':
                    continue
                area_link = urljoin(base_url, area_link)
                area_info.append((area_link, area_name))

            if mytree.xpath("//a[text()=\"下一页\"]/preceding-sibling::a[1]//text()"):
                pns = int(mytree.xpath("//a[text()=\"下一页\"]/preceding-sibling::a[1]//text()"))
            else:
                pns = 1
            return pns, area_info
        else:
            return None, None

    def start_requests(self):
        citys = ["sh", "sz", "bj", "gz", "hz", "cs"]
        for city in citys:
            pns, area_list = self.get_list(city)
            if pns and area_list:
                for url, name in area_list:
                    for pn in range(pns + 1):
                        new_url = url + f'pg{str(pn)}/'
                        yield scrapy.Request(
                            url=new_url,
                            callback=self.parse,
                            meta={"city": city, 'area': name}
                        )

    def parse(self, response):
        city = response.meta['city']
        area = response.meta['area']
        house_list = response.xpath('//div[@class="content__list"]/div')

        for house in house_list:
            item = LianjiaspiderItem()
            item['title'] = house.xpath('./a[@class="content__list--item--aside"]/@title').extract_first()
            item['rent'] = item['title'][:2]
            item['link'] = f'https://{city}.lianjia.com' + house.xpath(
                './a[@class="content__list--item--aside"]/@href').extract_first()
            item['location'] = '.'.join(house.xpath('./div/p[2]/a/text()').extract())
            yield scrapy.Request(
                url=item['link'],
                callback=self.parse_detail,
                meta={'item': item, "city": city, "area": area}
            )

    def parse_detail(self, response):
        item = response.meta['item']
        city = response.meta['city']
        area = response.meta['area']

        if item['rent'] == "整租" or item['rent'] == "合租":

            content = response.xpath("//div[@class=\"content__article__info\"]//ul/li/text()").extract()
            content = [c for c in content if c.find("：") != -1]
            d = {}
            for line in content:
                k, v = line.split("：")
                d[k] = v

            item['apartment_layout'] = response.xpath(
                "//*[@class=\"content__aside__list\"]//li[2]/text()").extract_first().strip()

            item['area'] = content[0].split("：")[-1]

            item['orientation'] = content[1].split("：")[-1]

            publish_time = response.xpath('//div[@class="content__subtitle"]/text()').extract()[1]
            item['publish_time'] = publish_time.split(' ')[1]

            item['unit_price'] = response.xpath('//*[@class="content__aside--title"]/span/text()').extract_first()

            floor = response.xpath('//div[@class="content__article__info"]/ul/li[8]').extract_first()
            item['floor'] = re.findall('.*楼层：(.*).*</li>', floor)[0]
            item['longitude'] = re.findall("longitude: '(.*)',", response.text)[0]
            item['latitude'] = re.findall("latitude: '(.*)'", response.text)[0]

            item['city'] = city
            item['area'] = area

            # 推荐房源
            temp = response.url.rsplit("/", 1)[0]
            _id = response.url.rsplit("/", 1)[-1].split(".")[0]
            city_id = "310000"
            similarity_url = temp + f'/aj/house/similarRecommend?house_code={_id}&city_id={city_id}&has_nearby=1'
            yield scrapy.Request(
                url=similarity_url, callback=self.parse_similarity, meta={'item': item}
            )
        else:
            pass

    def parse_similarity(self, response):
        item = response.meta['item']
        text = response.text
        import json
        json_data = json.loads(text)
        if json_data['status'] == 0:
            item['recomend'] = json_data['data']
        else:
            item['recomend'] = ''
        yield item
