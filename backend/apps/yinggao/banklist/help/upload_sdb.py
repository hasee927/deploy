import pandas as pd
from apps.yinggao.banklist.help.duplicate_key_update import DUPLICATE_UPDATEd


async def sdb(data ,db):
    filename = data.file_name.split(".")[0]
    excel_file = 'static/uploads/' + data.file_name
    # CSV文件路径
    csv_file = 'static/uploads/' + filename + ".csv"
    # 使用pandas读取Excel文件
    df = pd.read_excel(excel_file)
    # 将DataFrame保存为CSV文件
    df.to_csv(csv_file, index=False)
    csv = pd.read_csv(csv_file)
    dataList = []


    for index, row in csv.iterrows():
        tmpData = str(row['Unnamed: 10'])
        if tmpData.find('UPI') > -1:
            # 去掉金额中的逗号
            tmp_amount = str(row['Unnamed: 24']).strip(" ")
            amount = str(float(''.join(tmp_amount.split(','))))
            tmp_balance = str(row['Unnamed: 27']).strip(" ")
            balance = str(float(''.join(tmp_balance.split(','))))
            utr = tmpData.split('/')[2]
            post_data = {
                "bank_name": str(data.bank_name),
                "bank_account": str(data.bank_account),
                "bank_utr": utr,
                "trading_info": str(row['Unnamed: 10'].strip(" ")), #流水详情
                "amount": amount,
                "channel_code": str(data.channel_code),
                "trading_time": str(row['Unnamed: 7'].strip(" ")),
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

    return {"filename": data.file_name}