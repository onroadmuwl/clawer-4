from lxml import etree
import requests
import json
import time
import os
import pandas as pd
class jingdong():
    n=0
    header={'cookie':
                "xtest=5725.cf6b6759; __jdv=122270672|direct|-|none|-|1571814902388; __jdu=15718149023862073199854; shshshfpa=b1239f4e-18d2-a519-a723-976a84fa0ba8-1571814903; rkv=V0000; areaId=25; ipLoc-djd=25-2235-27497-0; qrsc=3; shshshfpb=psYCfknVLVr%207Xp9GQ0viAQ%3D%3D; __jda=122270672.15718149023862073199854.1571814902.1571831142.1571842723.4; __jdc=122270672; shshshfp=4d02fba05d40ad0d0221a118573e45ef; wlfstk_smdl=m7634wjznad8k55hc08hw2dzzxj86vss; TrackID=10-uiUmVUauFMhiA7QMVvlJJYok5ktbz2SeIE90n7AkKKowcv01sxhE65BQJXQKZlE2pfESwn_XMsvRdy4MzfGFeE9iVcvyP2-sznU_7jhmg; thor=7E8B9D19610AAE3B74C158B3DC3F5E693BD14A7F9DDDF3B04C45AF3B25B5C615579B97D6B1D1015C88B2844B1076D220B968DE07F347C4036F8E905B332FDD70714B709F3FDF00902049246E12C085DBCC0ED2E3E3C86B67E5792C967899F02BB068F14A9621C876FAFFE28CD3975FB6D2E41490D03917A98C2F558C9B6DFD7476A331A1A6A4F7B4037F6A3C32E8074C849C5F78D0A7764FE0E04B008FE9433A; pinId=mfEknONzvN4SRaqZdW7IgA; pin=jd_sOAUcuPAlzBe; unick=jd_sOAUcuPAlzBe; ceshi3.com=000; _tp=%2BFFpGI5ny3sBav7yCWg21g%3D%3D; _pst=jd_sOAUcuPAlzBe; __jdb=122270672.5.15718149023862073199854|4.1571842723; shshshsID=dce6dcebb15372b1ce5433e3b473f1b7_3_1571843349393; 3AB9D23F7A4B3C9B=3F3XCX2EEUS2JUA6NULVNGPQNMKANYM5NLOHW2V3FTPD4HG3SY53UMHO3O2ASWXADOUWHIQFFVRG2X5LSC4SRTXOBE"
            ,'user-agent':"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36"

            }
    def url(self,i):
        #第一页为0
        p=int(i+1)
        num=int(1+i*60)
        urls="https://search.jd.com/Search?keyword=华为手机&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&psort=3&page=%d&s=%d&click=0"%(p,num)
        return urls
    def deal_html(self,url):
        html=requests.get(url,headers=self.header).content
        html=etree.HTML(html)
        return html
    def get_price(self,htmls):
        selector_1=htmls.xpath('//div[@class="p-price"]/strong/i/text()')
        return selector_1
    def get_title(self,htmls):
        selector_3 = htmls.xpath('//div[@class="p-name p-name-type-2"]/a/@title')
        return selector_3
    def get_comment(self,htmls):
        html = htmls.xpath('//div[@class="p-focus"]/a/@data-sku')
        json_comments=[]
        for htm in html:

            url="https://club.jd.com/comment/productCommentSummaries.action?referenceIds="+str(htm)
            html_api=self.deal_html(url)
            jsons=html_api.xpath('//text()')[0]
            json_comment=list(json.loads(jsons)['CommentsCount'])[0]['CommentCount']
            json_comments.append(json_comment)
        return json_comments

    def get_onepage(self,w,filename):
        url=self.url(w)
        html=self.deal_html(url)
        t=self.get_title(html)
        p=self.get_price(html)
        c=self.get_comment(html)
        print(t)
        print(p)
        print(c)
        good_info=[]
        for i in range(0,30):
            try:
                goods={
                'title':self.get_title(html)[i],
                'price':self.get_price(html)[i],
                'comment_num':self.get_comment(html)[i]
                }
                self.n+=1
                good_info.append(goods)
                print("(" + str(self.n) + "):  " + str(goods))
            except: continue
        self.write_excel(filename,good_info)

    def write_excel(self,filename,goodinfo):
        if os.path.exists(filename):
            df=pd.read_excel(filename)
            df=df.append(goodinfo)
        else:
            df=pd.DataFrame(goodinfo)
        writer=pd.ExcelWriter(filename)
        df.to_excel(excel_writer=writer,columns=['title','price','comment_num'],encoding='utf8',index=False)
        writer.save()
        writer.close()


    def get_all_page(self,filename):
        for k in range(0,27):
            try:
                self.get_onepage(k,filename)
            except:
                continue

d=jingdong()
d.get_all_page("jingdong.xlsx")