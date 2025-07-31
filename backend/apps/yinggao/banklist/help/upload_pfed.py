import pandas as pd
from apps.yinggao.banklist.help.duplicate_key_update import DUPLICATE_UPDATEd


async def pfed(data ,db):
    csvfile = 'static/uploads/' + data.file_name
    csv = pd.read_csv(csvfile)
    csvList = []
    for index, row in csv.iterrows():
        if str(row['Unnamed: 2']).find("UPI") > -1:
            csvList.append(row)

    dataList = []
    if len(csvList) > 0:
        for row in csvList:
            # 去掉金额中的逗号
            tmp_amount = str(row['Unnamed: 8']).strip(" ")
            amount = str(float(''.join(tmp_amount.split(','))))
            tmp_balance = str(row['Unnamed: 9']).strip(" ")
            balance = str(float(''.join(tmp_balance.split(','))))

            post_data = {
                "bank_name": str(data.bank_name),
                "bank_account": str(data.bank_account),
                "bank_utr": str(row['Unnamed: 2'].split('/')[1]),
                "trading_info": str(row['Unnamed: 2']),
                "amount": amount,
                "channel_code": str(data.channel_code),
                "trading_time": str(row['Unnamed: 1']),
                "account_balance": balance,
                "info_sources": "backend",
                "collection_type": "entry",
                "match_type": "unmatch",
                "file_name": str(data.file_name)
            }
            dataList.append(post_data)

    if len(dataList) > 0:
        # 批量导入
        await DUPLICATE_UPDATEd(db, dataList)

    return {"filename": data.file_name, "count": len(dataList)}