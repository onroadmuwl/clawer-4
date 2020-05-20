#encoding:utf-8--
import requests
import time
import re
import json
import os
from random import randint
import pandas as pd
class taobao():
    def __init__(self):
    #淘宝既需要用户的缓存数据，也需要用户代理识别
    #可以直接用chrome浏览器获取xpath
    #你要爬取的内容是在一个json脚本中,etree用不了的，和微博不同
        self.i=0#计数

        self.header = {
        'cookie':
          "thw=cn; t=2d725b51f7b4892f737a5358c6a8cabf; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; everywhere_service_strategy=cco_busi:ads_crmwx_wanxiang_guard_crowd:20191007@1; cookie2=1b5347fe219fe55d6135f8235aae90ff; _tb_token_=550388dee8a8f; alitrackid=login.taobao.com; _m_h5_tk=bb6838d59440d2d18824b937fe9dfc24_1571824611913; _m_h5_tk_enc=2496b0898519f5c46dc4b9804474aefd; cna=E7UZFsf7LTkCASeBBcbUMq6D; v=0; tg=0; mt=ci=38_1; x5sec=7b227365617263686170703b32223a226136313932633861626166656630616338376631346665333165333464393235434f7666774f3046454b4f7a6f506a352b76664e7977456144444d7a4d6a4d324e7a4d354d7a6b374d673d3d227d; unb=2629169972; uc3=id2=UU6jUcf%2B5ewirA%3D%3D&vt3=F8dByucibOvzT39FWPo%3D&nk2=DkXav%2Fs8eB1re1qDLQ%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D; csg=e0303e49; lgc=muwenlong2000; cookie17=UU6jUcf%2B5ewirA%3D%3D; dnk=muwenlong2000; skt=31113bab6699b46b; existShop=MTU3MTgyNzczOQ%3D%3D; uc4=id4=0%40U2xuC7ljUXd1gzI51ueOZe89h7xQ&nk4=0%40DCALmZpbYIw%2FHAzDVoMfR8ZT1JzfMB7e; tracknick=muwenlong2000; _cc_=Vq8l%2BKCLiw%3D%3D; _l_g_=Ug%3D%3D; sg=02a; _nk_=muwenlong2000; cookie1=BxUCSKR0g2SMO7GoHGYZtWtnpvnmKLYGVZ5degiwdXc%3D; uc1=cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&pas=0&cookie14=UoTbnKsoPLBhXA%3D%3D&tag=8&lng=zh_CN; enc=G8gqEzdmkAIEgubbod0E3UoTOULGZ6SnwE4y3qobI%2B4%2FNy3MnvOcM%2B76tBQTNm6h0lawcmxBsWAK4hecVYOnXw%3D%3D; JSESSIONID=D9CAB6213FDE7B08536B79D79DD0F0CE; lastalitrackid=www.taobao.com; isg=BEdHq2qU1m5VY1LJ6ZjYlwLc1vsbKM6jTYFszxk0alb9iGdKIR7dfuFKLwhzVPOm; l=dBN-Nhmmq4W3mCn9BOCgdZ12-w_tSIRvmuWbmb5Di_5C36L_B77OkZCA8Fp6DjWftELB47t-w6J9-etkiKy06Pt-g3fPTxDc."
        ,'user-agent':
               "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36"

    }
    def _save_excel(self,goodslist,filename):
        if os.path.exists(filename):#excel只能先读后写，不能追加
            df = pd.read_excel(filename)
            df = df.append(goodslist)
        else:
            df = pd.DataFrame(goodslist)

        writer = pd.ExcelWriter(filename)#重新写
        df.to_excel(excel_writer=writer, columns=['title', 'price', 'location', 'sales'], index=False,
                    encoding='utf-8', sheet_name='Sheet')
        writer.save()
        writer.close()
    def _get_goods_info(self, goods_str):#读取json的内容
        goods_json = json.loads(goods_str)
        goods_items = goods_json['mods']['itemlist']['data']['auctions']#方括号里面的标签不是并列的，而是层层递进
        goods_list = []
        #http://www.bejson.com/
        #也可以用VS code。
        #来剖析json文件
        for goods_item in goods_items:
            goods = {'title': goods_item['raw_title'],
                     'price': goods_item['view_price'],
                     'location': goods_item['item_loc'],
                     'sales': goods_item['view_sales']}
            self.i+=1
            goods_list.append(goods)
            print("("+str(self.i)+"):  "+str(goods))
        return goods_list
    def get_onePage(self,keyword,pagenum,filename):
        pagenum=44*pagenum
        #url="https://s.taobao.com/search?q=%s&sort=sale-desc&p4ppushleft=%2C44&s=%d"%(keyword,pagenum)
        url="https://s.taobao.com/search?q=%s&sort=sale-desc&s=%d"%(keyword,pagenum)
        #url = "https://s.taobao.com/search?q=%s&sort=sale-desc&bcoffset=-3&p4ppushleft=%2C44&s=%d&ntoffset=-3" % (keyword, pagenum)
        html=requests.get(url,headers=self.header).text
        goods_match=re.search(r'g_page_config = (.*?)}};',html)#正则表达式提前json
        goods_str = goods_match.group(1) + '}}'#构建成完整的json
        goods_list = self._get_goods_info(goods_str)
        self._save_excel(goods_list,filename)
    def get_allPage(self,keyword,filename):
        for k in range(31,100):
            try:
                w = k + 1
                print('第' + str(w) + '页')
                self.get_onePage(keyword, k, filename)
                time.sleep(randint(50, 60))
            except: continue
d=taobao()
d.get_allPage('华为手机','WholeHuaWeiData___4.xlsx')
#前者是搜索的关键词，后者是保存的路径
#自行补充完整header