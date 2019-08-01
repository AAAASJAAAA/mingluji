import scrapy
from mingluji.items import MinglujiItem
import datetime
class ItcastSpider(scrapy.Spider):
    name = 'mlj'

    allowed_domains = ['gongshang.mingluji.com']
    # start_urls = ['https://gongshang.mingluji.com/jilin/riqi']

    import datetime

    def dateRange(self,start, end, step=1, format="%Y-%m-%d"):
        strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
        days = (strptime(end, format) - strptime(start, format)).days
        return ['https://gongshang.mingluji.com/jilin/riqi/' + strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


    def start_requests(self):#构造url到解析
        urls = self.dateRange('1970-01-01','2019-07-30')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_company)

    def parse(self, response):#需求修改，丢弃
        region_links = response.xpath('//*[@class="views-view-grid cols-3"]/tbody/tr/td/div/span/a[1]/@href').extract()
        for link in region_links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_company)


    def parse_company(self, response):
        # company_links = response.xpath('//td[@class="views-field views-field-name"]/a/@href').extract()#获取列表页中所有的连接
        company_names = response.xpath('//td[@class="views-field views-field-name"]/a/text()').extract()#名字
        province = response.xpath('//td[@class="views-field views-field-city"]/a/text()').extract()#城市
        time = response.xpath('//*[@id="page-title"]/text()').re('\d+-\d+-\d+')#时间
        # company_times = response.xpath('//td[@class="views-field views-field-date"]/a/text()').extract()


        for name,pro in zip(company_names,province):#获取解析到管道
            item = MinglujiItem()
            item['province'] = pro if pro else ''
            item['corporate_name'] = name if name else ''
            item['registration_date'] = time[0] if time else ''
            yield item
            # yield scrapy.Request(response.urljoin(link), callback=self.parse_info)


        nextlink = response.xpath('//*[@class="pager-next last"]/a/@href').extract()#获取下一页地址
        if nextlink:
            yield scrapy.Request(response.urljoin(nextlink[0]), callback=self.parse_company)



    def parse_info(self,response):#需求修改，丢弃

        item = MinglujiItem()
        province = response.xpath('//*[@class="breadcrumb"]/span[3]/a/span/text()').extract()
        corporate_name = response.xpath('//*[@class="field-item"]/span[@itemprop="name"]/a/text()').extract()
        address = response.xpath('//*[@class="field-item"]/span[@itemprop="address"]/text()').extract()
        id_code = response.xpath('//*[@class="field-item"]/span[@itemprop="identifier"]/a/text()').extract()
        region = response.xpath('//*[@class="field-item"]/span[@itemprop="foundingLocation"]/a/text()').extract()
        registration_date = response.xpath('//*[@class="field-item"]/span[@itemprop="foundingDate"]/a/text()').extract()
        business_scope = response.xpath('//*[@class="field-item"]/span[@itemprop="makesOffer"]/text()').re('(.+)/\（.*\）/')
        legal_representative = response.xpath('//*[@class="field-item"]/span[@itemprop="founder"]/a/text()').extract()
        registered_funds = response.xpath('//fieldset[@class="ad_biger"]/div').re('<span class="field-label">注册资金</span>：<span class="field-item">(.*?)</span>')
        corporate_type = response.xpath('//*[@class="field-item"]/span[@itemprop=""]/text()').extract()

        item['province'] = province[0] if province else ''
        item['corporate_name'] = corporate_name[0] if corporate_name else ''
        item['address'] = address[0] if address else ''
        item['id_code'] = id_code[0] if id_code else ''
        item['region'] = region[0] if region else ''
        item['registration_date'] = registration_date[0] if registration_date else ''
        item['business_scope'] = business_scope[0] if business_scope else ''
        item['legal_representative'] = legal_representative[0] if legal_representative else ''
        item['registered_funds'] = registered_funds[0] if registered_funds else ''
        item['corporate_type'] = corporate_type[0] if corporate_type else ''
        # item['url'] = response.url
        yield item