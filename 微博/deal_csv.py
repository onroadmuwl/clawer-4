from collections import Counter
import pandas as pd
import csv
from pyecharts.charts import Pie,Map
from pyecharts import options as opts
class deal_analyze():
    def deal(self):
        l = list()
        with open('huaweidata_improve.csv', 'r', encoding='gbk') as read:
            reader = csv.reader(read)
            for i in reader:
                row=i[3]
                if ' ' in  row:
                    rows = row[:row.find(' ')]
                    i.remove(row)
                    i.append(rows)

                justice= '海外' in i[3]
                if i[3]!='其他' and justice==False:
                    l.append(i)

        df = pd.DataFrame(l)
        df.drop_duplicates(subset=None, inplace=True)
        #print(df)

        return df
    def save(self):
        df=self.deal()
        df.to_csv('huaweidataImprove.csv')
    def hotmap_location(self):
        df=self.deal()
        row_locations=df.iloc[:,3].values
        num_count=Counter(row_locations)
        location=[]
        num=[]#解析字典
        for key, value in num_count.items():
            location.append(key)
            num.append(value)
        c = (
            Map()
                .add("", [list(z) for z in zip(location, num)], "china")
                .set_global_opts(title_opts=opts.TitleOpts(title="华为手机微博粉丝用户分布图"),
                                 visualmap_opts=opts.VisualMapOpts(max_=1000))
        )

        c.render(path='location.html')

    def sex(self):
        df = self.deal()
        row_locations = df.iloc[:, 2].values[1:]
        num_count = Counter(row_locations)
        sexs = []
        num = []  # 解析字典
        for key, value in num_count.items():
            sexs.append(key)
            num.append(value)
        c = (
            Pie()
                .add("", [list(z) for z in zip(sexs, num)]
                     , center=["35%", "60%"]
                     )
                .set_global_opts(title_opts=opts.TitleOpts(title="华为手机微博粉丝用户性别比例")
                                 , legend_opts=opts.LegendOpts(pos_left="75%"),
                                 )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        c.render(path='sex.html')
    def start(self):
        self.save()
        self.hotmap_location()
        self.sex()
s=deal_analyze()
s.start()

