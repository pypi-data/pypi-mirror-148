# Insert your code here. 
from dataclasses import replace
import requests
import pandas as pd
from lxml import etree
import json
import re


class StockSpider:
    """
    爬取股票交易信息。
    """
    def __init__(self):
        """
        对象参数成员：
            url1：接口url
            default_params1：数据属性
        """
        self.encoding = "GBK"
        self.url1 = "http://quotes.money.163.com/service/chddata.html"
        self.default_params1 = ["TCLOSE", "HIGH", "LOW", "TOPEN", "LCLOSE", "CHG", "PCHG", "TURNOVER", "VOTURNOVER", "VATURNOVER", "TCAP", "MCAP"]

    def get(self, exchange, code, start, end, params=None):
        """
        获取历史（按日）交易信息
        :param exchange: 交易所信息  数据类型：int   交易所信息 0：上证交易所；1：深圳交易所
        :param code: 股票代码   数据类型：str
        :param start: 开始日期  数据类型：str    格式：yyyyMMdd
        :param end: 结束日期    数据类型：str    格式：yyyyMMdd
        :param params: 访问数据类型   数据类型：List[str]
            TCLOSE: 收盘价
            HIGH: 当日最高
            LOW: 当日最低
            TOPEN: 开盘价
            LCLOSE: 前收盘
            CHG: 涨跌额
            PCHG: 涨跌幅
            TURNOVER: 换手率
            VATURNOVER: 成交量
            VOTURNOVER: 成交金额
            TCAP: 总市值
            MCAP: 流通市值

        :return: DataFrame对象
        """
        if not params:
            params = self.default_params1
        query = {
            "code": str(exchange) + code,
            "start": start,
            "end": end,
            "fields": ";".join(params)
        }
        response = requests.get(self.url1, params=query)
        response.encoding = self.encoding

        # 处理数据格式
        text_ls = response.text.split(sep='\n')
        response.close()
        new_ls = []
        for i in text_ls:
            new_ls.append(i.split(','))

        columns = new_ls[0]
        columns[-1] = columns[-1][:-1]
        new_ls.pop(-1)
        data = new_ls[:0:-1]
        for i in range(len(data)):
            data[i][-1] = data[i][-1][:-1]
        df = pd.DataFrame(data=data, columns=columns)
        df.iloc[:, 3:] = df.iloc[:, 3:].applymap(self.__process)
        df.iloc[:, 3:] = df.iloc[:, 3:].applymap(eval)
        return df

    def getPeersinfo(self, code):
        """
        获取同行业股票信息
        接口：东方财富
        @param code: 股票代码   格式：交易所地点+股票代码   数据类型：str
        """
        url = "http://emweb.securities.eastmoney.com/PC_HSF10/StockRelationship/StockRelationshipAjax"
        query = {
            "orderBy" : 1,
            "code": code.upper(),
            "isAsc": False
        }
        response = requests.get(url, params=query)
        response.encoding = "UTF-8"
        text = response.text
        response.close()
        js= json.loads(text)
        columns = ["股票代码","股票名称","总市值","流通市值","营业收入","归属净利润","营业收入同比增长","归属净利润同比增长"]
        
        df = pd.DataFrame((js["stockRandList"]))
        df.drop(["xh", "bgrq"],axis=1, inplace=True)
        df.columns = columns
        df.iloc[:, 2:] = df.iloc[:, 2:].applymap(self.__process)
        df.iloc[:, 2:] = df.iloc[:, 2:].applymap(eval)
        return df

    def __process(self, text):
            text = text.replace(" ", "")
            text = text.replace("③", "")
            text = text.replace("④", "")
            text = text.replace("%", "e-2")
            text = text.replace("亿", "e+8")
            text = text.replace("万", "e+4")
            text = text.replace("--", "np.nan")
            text = text.replace("①", "")
            return text


if __name__ == "__main__":
    sp = StockSpider()
    df = sp.get(1, "000036", "20220301", "20220401")
    print(df)


        