#coding=utf-8
import numpy as np
import pandas as pd


def concat_xls(path):
	host_all = pd.DataFrame()
	print(glob.glob(path+'/192*.xls'))

	for file in glob.glob(path+'/192*.xls'):
	    df = pd.read_excel(file,usecols="D:S",sheet_name="漏洞信息",index_col=0)
	    host_all = host_all.append(df)
	    
	print(host_all.shape)
	# print(host_all.columns)
	host_all.drop_duplicates(inplace=True)
	host_all.to_excel(path+"/hosts.xls")
	print("\n")
	return path+"/hosts.xls"


# for _dir in glob.glob("*深圳农商行*xls"):
# 	concat_xls_host(_dir)