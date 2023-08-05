import pandas as pd
import requests

class smSpider:
    """
    获取报表（Statement）信息
    """

    def __init__(self):
        """
        初始化
        数据成员：
            url1: 接口url
            headers: 主要是用于存放UA伪装
            encoding: 编码
            type_ls: 报表类型 包括：资产负债表、利润表、现金流量表、财务报表摘要、主要财务指标（又包括：偿债能力、营运能力、盈利能力）
            parts: 财务指标类型， 包括：偿债能力、盈利能力、营运能力
        """
        self.url1 = "http://quotes.money.163.com/service/"
        self.headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56"
        }
        self.encoding = "GBK"
        self.type_ls = {
            "资产负债表": 'zcfzb',
            "利润表": 'lrb',
            "现金流量表": 'xjllb',
            "财务报告摘要": 'cwbgzy',
            "主要财务指标": 'zycwzb'
        }

        self.parts = {
            "盈利能力": 'ylnl',
            "偿债能力": 'chnl',
            "营运能力": 'yynl',
            "成长能力": 'cznl'
        }

    def get(self, code,  sm_type, frequency="report", part=""):
        """
        获取财报信息
        :param code: 6位股票代码   数据类型：str
        :param sm_type: 报表类型
            可选参数: 资产负债表、利润表、资金流量表、财务报告摘要、主要财务指标
        :param frequency: 频率    数据类型
            可选参数: report、year、season
        :param part: 主要财务指标追加参数
            可选参数: 盈利能力、偿债能力、营运能力、成长能力
        :return: DateFrame对象
        """
        url1 = self.url1 + self.type_ls[sm_type] + "_" + code + ".html"

        if sm_type == "主要财务指标" and part != "":
            part = self.parts[part]
        else:
            part = ""

        query = {
            "part": part,
            "type": frequency
        }
        response = requests.get(url1, params=query, headers=self.headers)
        response.encoding = self.encoding
        text = response.text
        response.close()
        lines = text.split("\n")
        columns = (lines[0].split(','))[1:-1]
        indexes = [line.split(',')[0] for line in lines[1:]]
        data = [line.split(',')[1:-1] for line in lines[1:]]
        indexes.pop(-1)
        data.pop(-1)
        res = pd.DataFrame(data=data, columns=columns, index=indexes)
        res= res.dropna()
        res = res.applymap(self.__process)
        res = res.applymap(eval)
        return res

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
    sp = smSpider()
    print(sp.get("000036", "资产负债表", "year"))

