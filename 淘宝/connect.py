import pandas as pd
'''如果爬取过程中被淘宝网页反扒机制限制，需要分多次完成，可采用本函数数据进行连接
因为实际上一次爬完的几率很小'''
df1=pd.read_excel("WholeHuaWeiData.xlsx")
df2=pd.read_excel("WholeHuaWeiData_1.xlsx")
df3=pd.read_excel("WholeHuaWeiData_2.xlsx")
df4=pd.read_excel("WholeHuaWeiData_3.xlsx")
df5=pd.read_excel("WholeHuaWeiData_4.xlsx")
df=[]
df.append(df1)
df.append(df2)
df.append(df3)
df.append(df4)
df.append(df5)
dfs=pd.concat(df)
dfs.to_excel('WholeHuaWeiDatas.xlsx',index=False)
print(dfs)