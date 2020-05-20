#encoding:utf-8--
import pandas as pd
def deal(orignalfile,improvefile):
    df = pd.read_excel(orignalfile)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('max_colwidth', 100)
    newSlaerows = []
    salerows = df['sales'].values
    for row in salerows:
        row = row[:-3]
        row = row.replace('+', '')
        if '万' in row:
            row = row.replace('万', '')
            if '.' in row:
                row = row.replace('.', '')
                row = row + '000'
            else:
                row = row + '0000'
        newSlaerows.append(row)
    df['sales'] = newSlaerows
    newtitle=[]
    titles=df['title']
    for title in titles:
        title=title.replace('】','')
        title=title.replace('【','')
        newtitle.append(title)
    df['title']=newtitle
    newloaction = []
    loationrows = df['location'].values
    for rows in loationrows:
        if ' ' in rows:
            rows = rows[:rows.find(' ')]
        newloaction.append(rows)
    df['location'] = newloaction
    df.to_excel(improvefile, columns=['title', 'price', 'location', 'sales'], index=False, encoding='utf8')
    print(df)

if __name__=='__main__':
    deal('WholeHuaWeiDatas.xlsx','WholeHuaWeiDataImprove.xlsx')
#前者是原文件，后者是处理后的文件
'''对数据进行处理，更加规范化'''