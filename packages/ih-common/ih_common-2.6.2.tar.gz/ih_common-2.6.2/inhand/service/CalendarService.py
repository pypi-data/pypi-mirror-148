import http.client
import json
import time
import ssl
import requests
from datetime import datetime
from urllib import parse
import logging,traceback

class CalendarService:
    def __init__(self,settings):
        import sys
        sys.path.append('../../')
        from inhand.utilities.URLUtility import GenericURL
        self.settings = settings
        ssl._create_default_https_context = ssl._create_unverified_context


    # 月份
    def query(self,year,month):
        raise  NameError('This is a parent class, there is nothing to do!')


    @staticmethod
    def createCalendarService(settings):
        #if settings.app.calendar_provider == 'baidu':
        #    return BaiduCalendarService(settings)
        if settings.calendar_provider == 'wannianli':
            return BaiduCalendarService(settings)
        else:
            return None




class WanNianLi:
#    def __init__(self,settings):
#        CalendarService.__init__(self,settings)
#        self.calendar_provider = self.settings.calendar_provider
#        self.calendar_url = self.settings.calendar_url

    def __init__(self,provider,url):
        self.calendar_provider = provider
        self.calendar_url = url


    # 输入参数：月份
    # 参考： https://www.mxnzp.com/doc/detail?id=1
    def query(self, year, month):
        ym = datetime.now().strftime('%Y%m')
        if year is not None and month is not None:
            ym = "{}{}".format(year,str(month).zfill(2))
        url=self.calendar_url.format(ym)
        days={}
        try:
            r=requests.get(url)
            f = r.json()
            for item in f['data']:
                #type; 类型 0 工作日 1 假日 2 节假日 如果ignoreHoliday参数为true，这个字段不返回
               days[item['date']] = 1 if item['type'] != 0 else 2

            return days

        except Exception as e:
            traceback.print_exc()
            logging.warning("While call %s, There is an exception: %s" % (self.calendar_url, e))
            return None



#作废，结果不对
class BaiduCalendarService(CalendarService):
    def __init__(self,settings):
        CalendarService.__init__(self,settings)
        self.calendar_provider = self.settings.calendar_provider
        self.calendar_url = self.settings.calendar_url
#    def __init__(self,provider,url):
#        self.calendar_provider = provider
#        self.calendar_url = url

    # 输入参数：月份
    def query(self,year,month):
        url = self.calendar_url
        bits = list(parse.urlparse(url))
        qs = parse.parse_qs(bits[4])
        qs['query'] = '{}年{}月'.format(year,month)
        bits[4] = parse.urlencode(qs, True)
        url = parse.urlunparse(bits)
        lst = []
        lst1 = []
        lst2 = []
        lst3 = []
        try:
            r = requests.get(url)
            f = r.json()
            holiday = f['data'][0]['holiday']

            for i in range(len(holiday)):
                if len(holiday[i]['list']) == 1:
                    lst.append(holiday[i]['list'][0])
                else:
                    for j in range(len(holiday[i]['list'])):
                        lst.append(holiday[i]['list'][j])
            for i in range(len(lst)):
                for key in lst[i].keys():
                    t = lst[i][key]
                    lst1.append(t)

            for i in range(len(lst1)):
                if (i % 2) == 0:
                    lst2.append(lst1[i])
                else:
                    lst3.append(lst1[i])

            for i in range(len(lst2)):
                lst2[i] = datetime.strptime(lst2[i], '%Y-%m-%d').strftime('%Y-%m-%d')

            # del (dict)
            dit = dict(map(lambda x, y: [x, int(y)], lst2, lst3))
            return dit
        except Exception as e:
            traceback.print_exc()
            logging.warning("While call %s, There is an exception: %s" % (self.calendar_url,e))
            return None
"""
if __name__ == '__main__':
    import sys

    #sys.path.append('../../')
    #from inhand.service.SettingService import SpringCloudSettings
    #settings=SpringCloudSettings()
    #settings.readLocalSettings(path="../../../../test.json",module="jx-attendance-stat-svc")

    #calcendar = CalendarService.createCalendarService(settings)
    calcendar=WanNianLi("wangnianli","https://www.mxnzp.com/api/holiday/list/month/{}?app_id=j89kjqhkrnxtlorm&app_secret=c1lkY0dneElHNDdtQVlZWTRkNjlGZz09")
    ret = calcendar.query('2022','04')
    print(ret)
    ret = calcendar.query(2022,4)
    print(ret)
"""
