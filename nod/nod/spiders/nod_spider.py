from scrapy.item import Item, Field
from scrapy.http import FormRequest
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from nod.items import Notice


class NodSpider(BaseSpider):

    name = "nod"
    allowed_domains = ["mypublicnotices.com"]
    start_urls = ["http://www.mypublicnotices.com/OrangeCounty/PublicNotice.asp?Page=SearchResults"]

    def parse(self, response):
        formdata = {'DateRange': 'Last60', 'Category': '17'}
        yield FormRequest.from_response(response, formdata, callback=self.parse1)

    def parse1(self, response):
        formdata = {'Count': '100', 'FullTextType': '0'}
        yield FormRequest.from_response(response, formdata, callback=self.parse2)

    def parse2(self, response):
        public_notice_content = Selector(response).xpath('.//div[@id="PublicNoticeContent"]//table')

        g_search_results = public_notice_content.xpath('.//tr//td[contains(@class, "SearchResults1")]')
        w_search_results = public_notice_content.xpath('.//tr//td[contains(@class, "SearchResults2")]')

        items = []
        for s in range(0, 3):
            item = Notice()

            notice_cell = g_search_results[3*s]
            url = notice_cell.xpath('.//a[@class="SearchResultsHeading"]//@href').extract()[0].encode('ascii', errors='ignore')
            item['ad_id'] = re.sub("(\D)+(AdId=)", "", url)
            item['url'] = url
            item['heading'] = notice_cell.xpath('.//a[@class="SearchResultsHeading"]//text()').extract()[0].encode('ascii', errors='ignore')
            item['body'] = ''.join(notice_cell.xpath('descendant-or-self::text()').extract()).encode('ascii', errors='ignore')

            publication_cell = g_search_results[3*s+1]
            publication_info = publication_cell.sxpath('descendant-or-self::text()').extract()
            item['publication_name'] = publication_info[1].encode('ascii', errors='ignore')
            item['publication_dates'] = publication_info[2].encode('ascii', errors='ignore')

            items.append(item)

        return items

#         for s in range(0, 50):
#             w_search_results
#         notice_cells = public_notice_content.xpath('.//td[@class="SearchResults1 TopPadMedium BottomPadMedium LeftPadLarge RightPadLarge"]')
#         publication_cells = public_notice_content.xpath('.//td[@class="SearchResults1 BottomPadMedium LeftPadLarge RightPadLarge"]')
#

#         for s in range(0,300):
#             (s + 1) % 3 == 0
#             if (s % 3) == 0:
#                 notice_body = search_results[s].extract()
#             else if (s % 3) == 1:
#                 publication_info = search_results[s].extract()
#             path = 'self::*[contains(@class, SearchResults{})]'.format(s+1)
#             a_result = search_results.xpath(path)
#
#         notices = pcn.xpath('.//a[@class="SearchResultsHeading"]')
#
#         for no in notices:
#             cell = no.xpath('.//ancestor::table[1]//tr')
#             nodeId = no.xpath('@href')
#             notice_id = nodeId.extract()
#             notice_heading = no.xpath('text()').extract()
#             notice_body = cell[0].xpath()
#             appearedin = cell[1].xpath('td[text()]')
#             appearancePublication = appearedin.xpath('self::*//text()[2]').extract() # news paper
#             appearanceDate = appearedin.xpath('self::*//text()[3]').extract() # appearance dates
#             print appearancePublication # this is the appearance data
#
#         pcn.xpath()
#
#     def parse3(self, response):
#         print response
# #
# # url = 'http://www.mypublicnotices.com/OrangeCounty/PublicNotice.asp?Page=SearchResults'
# # req = FormRequest.from_response(response, formdata={'DateRange':'Last60', 'Category':'17'})
# # c
# #
# # req = FormRequest.from_response(response, formdata={'Count':'100', 'FullTextType':'0'})
# # fetch(req)
# #
# #
# # SearchResults
# # Count = 100
# # FullTextType = 0
