from datetime import datetime
from loguru import logger
import requests
from ofanalysis import const
import ofanalysis.utility as ut
import pandas as pd


def update_profit_ratio_to_notion():
    def get_profit_ratio(fund_code: str, start_date: str) -> float:
        today = datetime.today().date().strftime('%Y%m%d')
        start_date = pd.to_datetime(start_date).strftime('%Y%m%d')
        result = ut.db_get_dict_from_mongodb(
            mongo_db_name=const.MONGODB_DB_TUSHARE,
            col_name=const.MONGODB_COL_TS_FUND_NAV,
            query_dict={
                'ts_code': f'{fund_code}.OF',
                'nav_date': {'$gt': start_date, '$lte': today},
            }
        )
        if not result:  # 没取到
            return -999.0
        nav_series = pd.DataFrame(result).sort_values(
            by='nav_date', ascending=False)['accum_nav']
        profit_ratio = (nav_series.iloc[0] -
                        nav_series.iloc[-1])/nav_series.iloc[-1]
        if pd.isna(profit_ratio):
            return -999.0
        return round(profit_ratio, 4)
        
    # get all of fund in 基金池
    url = "https://api.notion.com/v1/databases/8aa76020501c4ca18c3c4dace60ee0ea/query"

    payload = {"page_size": 100}
    headers = {
        "Authorization": "secret_GYvWLjO0on50lqzHpp8Pqhz8RM1sh6K1QzJ7EIOW0hI",
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_dict = response.json()

    # update profit ratio for each fund
    for item in response_dict['results']:
        page_id = item['id']
        fund_code = item['properties']['基金代码']['rich_text'][0]['plain_text']
        logger.info(f'Processing fund code ->{fund_code}...')
        start_date = item['properties']['入池日期']['date']['start']
        profit_ratio = get_profit_ratio(fund_code, start_date)

        update_url = f'https://api.notion.com/v1/pages/{page_id}'

        headers = {
            "Authorization": "secret_GYvWLjO0on50lqzHpp8Pqhz8RM1sh6K1QzJ7EIOW0hI",
            "Accept": "application/json",
            "Notion-Version": "2022-02-22",
            "Content-Type": "application/json"
        }
        payload = {
            'properties': {
                '涨跌幅': {
                    'number': profit_ratio
                }
            }
        }

        requests.patch(update_url, json=payload, headers=headers)
