from apps.yinggao.banklist.help.duplicate_key_update import DUPLICATE_UPDATEd
import csv

async def indian(data ,db):
    csvfile = 'static/uploads/' + data.file_name
    dataList = []
    with open(csvfile, 'r' , encoding='gbk', errors='ignore') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0:
                if row[-1]:
                    try:
                        if row[-1].find('UPI') > -1:
                            # 去掉金额中的逗号
                            tmp_amount = str(row[2]).strip(" ")
                            amount = str(float(''.join(tmp_amount.split(','))))
                            tmp_balance = str(row[4]).strip(" ")
                            balance = str(float(''.join(tmp_balance.split(','))))
                            utr = row[-1].split("/")[1]

                            post_data = {
                                "bank_name": data.bank_name,
                                "bank_account": str(data.bank_account),
                                "bank_utr": utr,
                                "trading_info": str(row[-1]),
                                "amount": amount,
                                "channel_code": data.channel_code,
                                "trading_time": str(row[1]),
                                "account_balance": balance,
                                "info_sources": "backend",
                                "collection_type": "entry",
                                "match_type": "unmatch",
                                "file_name": str(data.file_name)
                            }
                            dataList.append(post_data)
                    except:
                        pass

    if len(dataList) > 0:
        # 批量导入
        await DUPLICATE_UPDATEd(db, dataList)
