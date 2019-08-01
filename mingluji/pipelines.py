# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs

class MinglujiPipeline(object):

    def process_item(self, item, spider):
        pass


class JsonCreatePipeline(object):
    """
    将数据保存到json文件，由于文件编码问题太多，这里用codecs打开，可以避免很多编码异常问题
        在类加载时候自动打开文件，制定名称、打开类型(只读)，编码
        重载process_item，将item写入json文件，由于json.dumps处理的是dict，所以这里要把item转为dict
        为了避免编码问题，这里还要把ensure_ascii设置为false，最后将item返回回去，因为其他类可能要用到
        调用spider_closed信号量，当爬虫关闭时候，关闭文件
    """
    def __init__(self):
        self.file = codecs.open('数据.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        json_data = {}
        json_data['企业名称'] = item['corporate_name']
        # json_data['注册地址'] = item['address']
        # json_data['统一社会信用代码'] = item['id_code']
        # json_data['地区'] = item['region']
        json_data['注册日期'] = item['registration_date']
        # json_data['经营范围'] = item['business_scope']
        # json_data['法定代表人'] = item['legal_representative']
        # json_data['注册资金'] = item['registered_funds']
        # json_data['企业类型'] = item['corporate_type']

        lines = json.dumps(dict(json_data), ensure_ascii=False) + "\n"
        self.file.write(lines)

        return item

    def spider_closed(self, spider):
        self.file.close()