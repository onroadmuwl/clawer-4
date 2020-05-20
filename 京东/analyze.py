import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts
df=pd.read_excel("jingdong.xlsx")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 100)
columns=df.columns.tolist()
columns.append("price_range")
df.reindex(columns=columns)
prices=[]
a='price(10k~15k)'
b='price(5k~10k)'
c='price(3k~5k)'
d='price(2k~3k)'
e='price(1k~2k)'
f='price(0~1k)'
for i in range(0,len(df)):
    price=df.iloc[i]['price']
    if price<=1000:
        prices.append(f)
    elif price>1000 and price<=2000:
        prices.append(e)
    elif price>2000 and price<=3000:
        prices.append(d)
    elif price>3000 and price<=5000:
        prices.append(c)
    elif price>5000 and price<=10000:
        prices.append(b)
    elif price>10000 and price<=20000:
        prices.append(a)
df['price_range']=prices
gf=df.groupby(df['price_range'])
gfs=gf.sum()
total_price=[f,a,e,d,c,b]
total_sales=[]
print(gfs)
for i in gfs['comment_num'].values:
    total_sales.append(int(i))
c = (
        Pie()
        .add("", [list(z) for z in zip(total_price, total_sales)],center=["50%", "60%"],label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
).set_global_opts(title_opts=opts.TitleOpts(title="京东网各价位华为手机累计销量图",pos_right="60%") ,legend_opts=opts.LegendOpts(pos_left="85%"))
    )

c.render(path='jingdonghuawei.html')
