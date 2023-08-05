import requests
import pandas as pd

class holderSpider:
    """
    爬取持股信息
    """
    def __init__(self):
        """
        初始函数
        数据成员：
            encoding: GBK编码
            url1: 股东分析接口
            url2: 基金持股接口
            period: 报告期
        """
        self.encoding = "GBK"
        self.url1 = 'http://quotes.money.163.com/service/gdfx.html'
        self.url2 = 'http://quotes.money.163.com/service/jjcg.html'
        self.url3 = 'http://quotes.money.163.com/f10/fhpg_'
        self.period = {
            1: "-03-31%2C,-12-31",
            2: "-06-30%2C,-03-31",
            3: "-09-30%2C,-06-30",
            4: "-12-31%2C,-09-30"
        }

    def getTop10(self, code, year, period=1, lt=False):
        """
        获取10大股东信息
        :param code: 6位股票编码   数据类型：str
        :param year: 年份 数据类型：int
        :param period: 报告期  数据类型：int    可选参数：1、2、3、4
        :param lt: 是否是流通股
        :return: DataFrame数据对象
        """
        if lt:
            lt = "lt"
        else:
            lt = ""

        query_date = lt + "date"

        date_ls = self.period[1].split(',')
        if period == 1:

            date = str(year)+date_ls[0]+str(year-1)+date_ls[1]
        else:
            date = str(year)+date_ls[0]+str(year)+date_ls[1]

        query = {
            query_date: date,
            "symbol": code
        }

        response = requests.get(self.url1, params=query)
        response.encoding = "UTF-8"
        text = response.text

        #使用lxml解析
        from lxml import etree
        tree = etree.HTML(text)
        columns = [i.text for i in tree.xpath("*//tr/th")]
        text_ls = [i.text for i in tree.xpath("*//tr/td")]
        data = [text_ls[4*i: 4*(i+1)] for i in range(10)]
        df = pd.DataFrame(data=data, columns=columns)
        return df

    def getFundHolders(self, code, year, period=1):
        """
        获取基金持股信息（按报告期）
        :param code: 6位股票代码   数据类型：str
        :param year: 年份 数据类型：int
        :param period: 报告期 数据类型：int 可选参数：1、2、3、4
        :return: DataFrame对象
        """
        query_date = "date"

        date_ls = self.period[period].split(',')
        if period == 1:
            date = str(year)+date_ls[0]+str(year-1)+date_ls[1]
        else:
            date = str(year)+date_ls[0]+str(year)+date_ls[1]

        query = {
            query_date: date,
            "symbol": code
        }

        response = requests.get(self.url2, params=query)
        response.encoding = "UTF-8"
        text = response.text

        # 用lxml解析
        from lxml import etree
        etree = etree.HTML(text=text)

        # 定义函数，处理转义字符
        import json
        import re
        def transform(string):
            if not string:
                return ""
            elif len(string) < 5:
                return string
            string = string.replace(" ", "")
            string = string.replace("\\r", "")
            string = string.replace("\\n", "")
            string = string.replace("\\t", "")
            string = string.replace("\\", "")

            regex = re.compile("u[0-9a-f]{4}")
            body = "\\".join(regex.findall(string))
            try:
                name = json.loads('\"\\'+body+'\"')
            except:
                return string
            iter_ = list(regex.finditer(string))
            iter_name = iter(name)
            string_list = list(string)
            for i in range(len(iter_)):
                span = iter_[i].span()
                string_list[span[0]:span[1]] = list(next(iter_name) + " "*4)
            string = "".join(string_list).replace(" ", "")
            return string

        # 处理数据
        columns = ["基金名称"] + [transform(i.text) for i in etree.xpath("*//thead//*//th")][1:]
        fundNames = [transform(i.text) for i in etree.xpath("*//thead//*//td//*")[:-10]]
        sub_data = [transform(i.text) for i in etree.xpath("*//thead//*//td")[:]]
        info_index = sub_data[-1].find("info")
        sub_data[-1] = sub_data[-1][:info_index-3]

        data = []
        for i in range(len(fundNames)):
            curr = []
            curr.append(fundNames[i])
            for j in range(1,6):
                curr.append(sub_data[i*6+j])
            data.append(curr)

        df = pd.DataFrame(data, columns=columns)
        return df

    def getFundHolders2(self, code, start, end):
        """
        获取基金持股信息（不推荐，参数格式要求高）
        代码：复用getFundHolders，代码简化将在以后进行
        :param code: 6位股票代码   数据类型：int
        :param start: 开始日期  数据类型：str    必须符合报告期要求，包括：yyyy-03-31、yyyy-06-30、yyyy-09-30、yyyy-12-31
        :param end: 结束日期    数据类型：str    必须符合报告期要求，与start参数要求一直
        :return: DataFrame对象
        """
        query_date = "date"
        date = end + "%2C" + start

        query = {
            query_date: date,
            "symbol": code
        }

        response = requests.get(self.url2, params=query)
        response.encoding = "UTF-8"
        text = response.text

        # 用lxml解析
        from lxml import etree
        etree = etree.HTML(text=text)

        # 定义函数，处理转义字符
        import json
        import re
        def transform(string):
            if not string:
                return ""
            elif len(string) < 5:
                return string
            string = string.replace(" ", "")
            string = string.replace("\\r", "")
            string = string.replace("\\n", "")
            string = string.replace("\\t", "")
            string = string.replace("\\", "")

            regex = re.compile("u[0-9a-f]{4}")
            body = "\\".join(regex.findall(string))
            try:
                name = json.loads('\"\\' + body + '\"')
            except:
                return string
            iter_ = list(regex.finditer(string))
            iter_name = iter(name)
            string_list = list(string)
            for i in range(len(iter_)):
                span = iter_[i].span()
                string_list[span[0]:span[1]] = list(next(iter_name) + " " * 4)
            string = "".join(string_list).replace(" ", "")
            return string

        # 处理数据
        columns = ["基金名称"] + [transform(i.text) for i in etree.xpath("*//thead//*//th")][1:]
        fundNames = [transform(i.text) for i in etree.xpath("*//thead//*//td//*")[:-10]]
        sub_data = [transform(i.text) for i in etree.xpath("*//thead//*//td")[:]]
        info_index = sub_data[-1].find("info")
        sub_data[-1] = sub_data[-1][:info_index - 3]

        data = []
        for i in range(len(fundNames)):
            curr = []
            curr.append(fundNames[i])
            for j in range(1, 6):
                curr.append(sub_data[i * 6 + j])
            data.append(curr)

        df = pd.DataFrame(data, columns=columns)
        return df

    def getDividen(self, code):
        """
        分红信息查询
        :param code: 6位股票代码   数据类型：int
        :return: DataFrame数据结构
        """
        # 表头columns
        columns = ["公告日期", "分红年度", "送股", "转增", "派息", "股权登记日", "除权登记日", "红股上市日"]

        url = self.url3 + code + ".html"
        response = requests.get(url)
        text = response.text

        # 解析网页
        from lxml import etree
        tree = etree.HTML(text)
        text_ls = [i.text for i in tree.xpath("*//div[@class='inner_box']//tr//td")]
        data = []
        for i in range(len(text_ls)//8):
            data.append(text_ls[i*8: (i+1)*8])
        df = pd.DataFrame(data, columns=columns)
        return df