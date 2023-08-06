import requests
import os
from lxml import etree
import gensim
import random
import numpy as np
import jieba
import re
from .DATA_USE import load_negative, load_positive

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56",
    "Connection":"close"
}

class newsSpider:
    def __init__(self, sample_num=-1):
        self.base1 = "https://finance.sina.com.cn/head/finance"


    def getDayUrls(self, date, sample_num=-1):
        url = self.base1 + date + "pm.shtml"
        base = "http://finance.sina.com.cn"
        response = requests.get(url=url, headers=headers)
        response.encoding = self.__findCharSet(response.text)
        tree = etree.HTML(response.text)
        # with open(".//html.html", 'w', encoding=self.__findCharSet(response.text)) as fp:
        #     fp.write(response.text)
        response.close()
        a_s = tree.xpath("*//a/@href")
        new_a_s = []
        regex1 = re.compile("[0-9]{1}[0-9]+.html")
        regex2 = re.compile("[0-9]{1}[0-9]+.shtml")
        for a in a_s:
            l1 = regex1.search(a)
            l2 = regex2.search(a)
            if l1 or l2:
                if a[0] == "/":
                    a = base + a
                new_a_s.append(a)
        import random
        random.shuffle(new_a_s)
        curr_index = 0
        valid_a_s = []
        valid_index = 0
        while curr_index < len(new_a_s) and (sample_num==-1 or sample_num > valid_index):
            url = new_a_s[curr_index]
            try:
                response = requests.get(url, headers=headers)
                response.encoding = self.__findCharSet(response.text)
                tree2 = etree.HTML(response.text)
                response.close()
                p_s = tree2.xpath("*//p")
                texts = []
                for p in p_s:
                    if p.text and len(p.text) > 80:
                        texts.append(p.text)

                if len(texts) > 3:
                    valid_index += 1
                    valid_a_s.append(url)
                curr_index += 1
            except:
                curr_index += 1
                response.close()

        return valid_a_s


    def getDayText(self, date, dir_path, num=-1):
        urls = self.getDayUrls(date, sample_num=num)

        for i in range(1, len(urls)+1):
            with open(dir_path+"/"+date+str(i)+".txt", 'w', encoding="UTF-8") as fp:
                response = requests.get(urls[i-1], headers=headers)
                response.encoding = self.__findCharSet(response.text)
                text = response.text
                response.close()
                p_s = etree.HTML(text).xpath("*//p")
                for p in p_s:
                    if p.text and len(p.text) > 80:
                        fp.write(p.text + "\n")


    def getMonthUrls(self, date, sample_num_each_day=-1):
        import datetime
        # 解析date
        year = eval(date[:4])
        month = eval(date[-1] if date[4] == "0" else date[4:])
        curr_date = datetime.date(year, month, 1)
        end_date = datetime.date(year if month!= 12 else year+1, month+1 if month != 12 else 1, 1)
        dic_urls = {}
        while curr_date < end_date:
            print(curr_date)
            dic_urls[curr_date] = self.getDayUrls(curr_date.strftime("%Y%m%d"), sample_num_each_day)
            curr_date += datetime.timedelta(1)
        return dic_urls


    def getMonthText(self, date, dir_path ,sample_num_each_day=-1):
        dic_url = self.getMonthUrls(date, sample_num_each_day)
        # 开始下载
        for key, value in dic_url.items():
            os.makedirs(dir_path+"/"+key.strftime("%Y%m%d"))
            count = 1
            for day in value:
                with open(dir_path + "/" + key.strftime("%Y%m%d") + '/' + str(count) + ".txt", 'w', encoding="UTF-8") as fp:
                    response = requests.get(day)
                    response.encoding = self.__findCharSet(response.text)
                    text = response.text
                    response.close()
                    p_s = etree.HTML(text).xpath("*//p")
                    for p in p_s:
                        if p.text and len(p.text) > 80:
                            fp.write(p.text + "\n")
                count += 1



    def __findCharSet(self, text):
        index1 = text.find('charset')
        text2 = text[index1+8:]
        index2 = text2.find('"')

        return text2[:index2]


class newsAnalyser:
    def __init__(self, positive_path = None, negative_path = None):
        if not positive_path:
            self.positive_dic = gensim.corpora.Dictionary([load_positive()])
        else:
            ls = []
            with open(positive_path, 'r', encoding="UTF-8") as fp:
                for line in fp.readlines():
                    ls.append(line[:-1])
            self.positive_dic = gensim.corpora.Dictionary([ls])

        if not negative_path:
            self.negative_dic = gensim.corpora.Dictionary([load_negative()])
        else:
            ls = []
            with open(negative_path, 'r', encoding='utf-8') as fp:
                for line in fp.readlines():
                    ls.append(line[:-1])
            self.negative_dic = gensim.corpora.Dictionary([ls])
        
        for i in self.negative_dic.itervalues():
            jieba.add_word(i)
        for i in self.positive_dic.itervalues():
            jieba.add_word(i)

    def getSentiment(self, dir_path, sample_percent=1):
        file_list = []
        for curDir, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".txt"):
                    file_list.append(os.path.join(curDir, file))
        random.shuffle(file_list)

        file_list = file_list[:len(file_list)*sample_percent]

        num_pos = 0
        num_neg = 0
        for file in file_list:
            with open(file, 'r', encoding="utf-8") as fp:
                text_list = fp.readlines()
                for sentence in text_list:
                    pos_trans = self.positive_dic.doc2idx(jieba.lcut(sentence))
                    num_pos += (sum(np.array(pos_trans) != -1))
        for file in file_list:
            with open(file, 'r', encoding="utf-8") as fp:
                text_list = fp.readlines()
                for sentence in text_list:
                    neg_trans = self.negative_dic.doc2idx(jieba.lcut(sentence))
                    num_neg += (sum(np.array(neg_trans) != -1))
        if (num_neg + num_pos == 0):
            return None
        return (num_neg * -1 + num_pos) / (num_neg + num_pos)

if __name__ == "__main__":
    base = r"D:\SinaNews"
    dic_base = 'E:\大学本科\学术\第二阶段 提前学习\情感词典\chinese_sentiment_dictionary-master\chinese_sentiment_dictionary-master\\file\情感词典\清华大学李军中文褒贬义词典\\'
    dic = {}
    for year in range(2020, 2021):
        base_dir_path = base + "/" + str(year) + "/"
        for month in range(1, 2):
            date = str(year) + "0"*(1-month//10) + str(month)
            print(date)
            sa = newsAnalyser(dic_base+"praise.txt", dic_base+"degrade.txt")
            dic[date] = sa.getSentiment(base_dir_path+"/"+date)
    print(dic)
