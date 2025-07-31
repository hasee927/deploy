import pandas as pd
from apps.yinggao.banklist.help.duplicate_key_update import DUPLICATE_UPDATEd


async def iob(data ,db):
    csvfile = 'static/uploads/' + data.file_name
    csv = pd.read_csv(csvfile)
    dataList = []
    for index, row in csv.iterrows():
        obj = row.Narration
        if obj.find("CR") > 0:
            utr = row.Narration.split("/")[1]

            # 去掉金额中的逗号
            tmp_amount = str(row.Credit).strip(" ")
            amount = str(float(''.join(tmp_amount.split(','))))
            tmp_balance = str(row.Balance).strip(" ")
            balance = str(float(''.join(tmp_balance.split(','))))

            post_data = {
                "bank_name": data.bank_name,
                "bank_account": str(data.bank_account),
                "bank_utr": utr,
                "trading_info": str(row.Narration),
                "amount": amount,
                "channel_code": data.channel_code,
                "trading_time": str(row.Date),
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