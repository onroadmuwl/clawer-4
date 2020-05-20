import pandas as pd
import numpy as np
from wordcloud import WordCloud
from PIL import Image
import jieba
from collections import Counter
from pyecharts.charts import Pie,Map
from pyecharts import options as opts
class Analyze():
    def wordCloud_title(self,filename):
        df=pd.read_excel(filename)
        row_titles=df['title']
        row_title_list=[]
        for row_t in row_titles:
            row_title_list.append(row_t)
        row_title_str="".join(row_title_list)#列表变成字符串
        data=' '.join(jieba.cut(row_title_str))
        img=Image.open(r'original.jpg')
        imgarray=np.array(img)#转化为数组
        my_word_cloud=WordCloud(
            font_path='C:\Windows\Fonts\simkai.ttf',
            mask=imgarray,
            background_color='white',
            scale=8#构造精细度
        )
        myWordCloud=my_word_cloud.generate(data)
        myWordCloud.to_file('title_keyword.jpg')

    def hotmap_location(self,filename):
        df=pd.read_excel(filename)
        row_locations=df['location']
        row_location_list=[]
        for row_t in row_locations:
            row_location_list.append(row_t)
        num_count=Counter(row_location_list)
        location=[]
        num=[]#解析字典
        for key, value in num_count.items():
            location.append(key)
            num.append(value)
        c = (
            Map()
                .add("", [list(z) for z in zip(location, num)], "china")
                .set_global_opts(title_opts=opts.TitleOpts(title="淘宝T恤卖家分布图"),
                                 visualmap_opts=opts.VisualMapOpts(max_=200))
        )

        c.render(path='saler_location.html')

    def price_map(self,filename):
        df = pd.read_excel(filename)
        df_price=df['price']
        category=[0,20,30,50,80,100,150,200,500,16000]
        price_range=pd.cut(df_price,category)
        #counts=len(price_range)#这是一个列表
        #print(counts)
        #print(price_range)
        Count=Counter(price_range)
        price=[]#导入列表之后格式不对
        num=[]
        for key, value in Count.items():
            price.append(key)
            num.append(value)
        prices=[]#另建一个
        for i in price:
            i=str(i)
            i=i[i.find('('):i.find('c')]
            i=i.replace('(','')
            i='价格区间('+i+')'
            prices.append(i)
        c = (
            Pie()
                .add("", [list(z) for z in zip(prices,num )]
            ,center=["35%", "60%"]
        )
                .set_global_opts(title_opts=opts.TitleOpts(title="价格区间")
                ,legend_opts=opts.LegendOpts(pos_left="75%"),
        )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        c.render(path='price_range.html')
    def start(self,filename):
        self.wordCloud_title(filename)
        self.price_map(filename)
        self.hotmap_location(filename)

d=Analyze()
d.start('WholeTaobaoDataImprove.xlsx')