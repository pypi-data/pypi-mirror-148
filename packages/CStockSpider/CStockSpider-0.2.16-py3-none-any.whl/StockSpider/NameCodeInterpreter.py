import requests
import pandas as pd

class NameCodeInterpreter:
    """
    股票名称与公司名称转换器
    """
    def __init__(self):
        self.base = "http://quotes.money.163.com/stocksearch/json.do?"

    def Name2Code(self, name, count=5):
        """
        通过股票（模糊）名称查找股票代码
        :param name: 模糊名称   数据类型：str
        :param count: 查找数量  数据类型：int
        :return: DataFrame对象
        """
        query = {
            "word": name,
            "count": count
        }
        response = requests.get(url=self.base, params=query)
        text = response.text
        lindex = text.find("(")
        rindex = text.rfind(")")
        import json
        new_text = text[lindex+1: rindex]
        js = list(json.loads(new_text))

        return pd.DataFrame(js)

    def Code2Name(self, code, count=5):
        """
        通过股票代码（模糊）查询股票名称
        :param code: 6位股票代码   数据类型： str
        :param count: 查找数量  数据类型：int
        :return: DataFrame对象
        """
        query = {
            "word" : code,
            "count": count
        }
        response = requests.get(url=self.base, params=query)
        text = response.text
        lindex = text.find("(")
        rindex = text.rfind(")")
        import json
        new_text = text[lindex + 1: rindex]
        js = list(json.loads(new_text))

        return pd.DataFrame(js)

    def Names2Codes(self, names):
        """
        通过股票精确名称查询股票代码
        :param names: 股票名称序列    数据类型：iterable
        :return: DataFrame对象
        """
        import json
        res = []
        for name in names:
            query = {
                "word": name,
                "count": 1
            }
            text = requests.get(self.base, params=query).text
            lindex = text.find("(")
            rindex = text.rfind(")")
            res.append(json.loads(text[lindex+1: rindex])[0])
        return pd.DataFrame(data=res)

    def Codes2Names(self, codes):
        """
        通过股票代码名称查询股票名称
        :param codes: 6位股票代码序列    数据类型：iterable
        :return: DataFrame对象
        """
        import json
        res = []
        for code in codes:
            query = {
                "word": code,
                "count": 1
            }
            text = requests.get(self.base, params=query).text
            lindex = text.find("(")
            rindex = text.rfind(")")
            res.append(json.loads(text[lindex + 1: rindex])[0])
        return pd.DataFrame(data=res)