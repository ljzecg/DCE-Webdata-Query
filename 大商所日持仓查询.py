import requests
from bs4 import BeautifulSoup


def query(query_date: str, query_company: str, contract_id: str):

	query_date = query_date
	query_company = query_company.lower()
	contract_id = contract_id.lower()
	
	if len(query_date) != 8:
		print("日期长度错误，请确保为8位，格式为：yyyyMMdd，如：20190102")
		return False
	
	index_id = 0
	for i, c in enumerate(contract_id):
		if 48 <= ord(c) <= 57:
			index_id = i
			break
	query_id = contract_id[:index_id].lower()
	
	query_d = {
		"cjl": "0",
		"buy": "0",
		"sell": "0",
	}
	
	query_main_list = list()
	
	year = query_date[:4]
	month = str(int(query_date[4:6]) - 1)   # 月份需要减1
	day = query_date[6:]
	
	form_data = {                                       # name:value
		"memberDealPosiQuotes.variety": query_id,       # 期货代码
		"memberDealPosiQuotes.trade_type": 0,           # 0是期货，1是期权
		"year": year,
		"month": month,
		"day": day,
		"contract.contract_id": contract_id,
		"contract.variety_id": query_id,
		"currDate": query_date
	}
	
	url = r"http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html"
	
	r = requests.post(url=url, data=form_data)
	
	if r.status_code == requests.codes.ok:
		# if is_query_valid(r.text, contract_id, query_date):
		soup = BeautifulSoup(r.text.split(sep="查询日期：")[1], 'html.parser')
		tables = soup.findAll('table')
		try:
			tab = tables[1]
			for tr in tab.findAll('tr'):        # 行
				query_sub_list = list()
				for td in tr.findAll('td'):     # 列
					txt_strip = td.getText().strip()
					query_sub_list.append(txt_strip)
				if len(query_sub_list) == 12:
					query_main_list.append(query_sub_list)
		except IndexError:
			print("%s, %s 查询参数有误！请检查日期和合约代码是否有效!(当日数据未生成或当日非交易日)" % (contract_id.upper(), query_date,))
			return False
		# else:
		# 	print("%s, %s 查询参数有误！请检查合约代码是否有效！" % (contract_id.upper(), query_date, ))
		# 	return False
	else:
		print("%s, %s 连接失败！" % (query_company, contract_id.upper(),))
		return False
	
	if query_main_list is not None:
		for sub_lst in query_main_list:
			if sub_lst[1] == query_company:
				query_d["cjl"] = sub_lst[2]
			if sub_lst[5] == query_company:
				query_d["buy"] = sub_lst[6]
			if sub_lst[9] == query_company:
				query_d["sell"] = sub_lst[10]
		print("-=-" * 10)
		print("查询成功！")
		print("日期：%s" % (query_date, ))
		print("合约名称：%s" % (contract_id.upper(), ))
		print("期货公司：%s" % (query_company, ))
		print("买持仓量：%s" % (query_d["buy"], ))
		print("卖持仓量：%s" % (query_d["sell"], ))
		print("-=-" * 10)


if __name__ == "__main__":
	
	date = "20191011"
	company = "永安期货"
	
	lst = [
		[date, company, "EG2001"],
		[date, company, "EG2005"],
		[date, company, "EG2009"],
		[date, company, "PP2001"],
		[date, company, "PP2005"],
		[date, company, "PP2009"],
		[date, company, "L2001"],
		[date, company, "L2005"],
		[date, company, "L2009"],
		[date, company, "L2009"],
		
		# 还需要查询其他大商所的，自己再添加即可
		# [date, company, "L2009"],
		# [date, company, "L2009"],
		# [date, company, "L2009"],
	]

	for l in lst:
		query(l[0], l[1], l[2])
