# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

from scrapy.exceptions import DropItem

from amazon_spider.helper import Helper
from amazon_spider.sql import ReviewSql, RankingSql
from amazon_spider.items import ReviewDetailItem, SalesRankingItem, KeywordRankingItem
from amazon_spider.items import ReviewProfileItem


class AmazonSpiderPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ReviewProfileItem):
            ReviewSql.insert_profile_item(item)
            return item

        if isinstance(item, ReviewDetailItem):
            delay_date = Helper.delay_forty_days()  # 40天的截止时间
            item_date = Helper.convert_date_str(item['date'])
            if item_date < delay_date:   # 判断是否过了40天限额，如果超出范围 则抛弃此item
                raise DropItem('the review_id:[%s] has been expired' % item['review_id'])
            else:
                item['review_url'] = 'https://www.amazon.com' + item['review_url']
                item['date'] = item_date.strftime('%Y-%m-%d')
                ReviewSql.insert_detail_item(item)

                return item

        if isinstance(item, SalesRankingItem):
            RankingSql.insert_sales_ranking(item)
            return item

        if isinstance(item, KeywordRankingItem):
            RankingSql.insert_keyword_ranking(item)
            return item

        pass