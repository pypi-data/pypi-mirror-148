import time
from tcoreapi_mq import * 
import numpy as np
import pandas as pd

#登入
TCoreAPI= TCoreZMQ(quote_port="51630",trade_port="51600")

his=TCoreAPI.SubHistory("TC.F.SHFE.rb.202110", "1K", "2021052000", "2021060807")#time.strftime("%Y%m%d",time.localtime()
his1=TCoreAPI.SubHistory("TC.F.SHFE.ni.202107", "1K", "2021052000", "2021060807")
print("历史数据：\n",pd.DataFrame(his),"\n",pd.DataFrame(his1))
TCoreAPI.SubQuote("TC.F.SHFE.rb.202110")
TCoreAPI.SubQuote("TC.F.SHFE.ni.202107")
while True:
    message=TCoreAPI.mdupdate()
    if message and message['DataType']=='REALTIME':
        print("实时行情 \n 合约：",message['Quote'])
        print("实时行情 \n 合约：",datetime.datetime.now(),message['Quote']['Symbol'],"  ",int(message['Quote']['FilledTime'])+80000,"  当日成交量：%s" % message['Quote']['TradeVolume'])
        print("最新历史\n",TCoreAPI.barupdate("TC.F.SHFE.rb.202110", "1K"))#SubHistory的结束日期必须是大于或等于最新 日期才能获取到最新K
