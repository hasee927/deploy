import pandas as pd

from apps.yinggao.banklist.help.utils import save_collData


async def bom(data ,db):
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
    collList = []
    bank_account = ''
    for index, row in csv.iterrows():

        account = str(row['Unnamed: 4'])
        if account.find('Account No') > -1:
            bank_account = row['Unnamed: 4'].split(':')[1].strip(' ')

        if row['Unnamed: 1'] == "UPI":
            # 去掉金额中的逗号
            tmp_amount = str(row['Unnamed: 5']).strip(" ")
            amount = str(float(''.join(tmp_amount.split(','))))
            tmp_balance = str(row['Unnamed: 6']).strip(" ")
            balance = str(float(''.join(tmp_balance.split(','))))

            tmp_random_number = row['Unnamed: 2'].strip(" ")
            temp_random = tmp_random_number.split("/")[-1]
            random_number = ''
            if temp_random:
                if not temp_random == "NA":
                    random_number = temp_random

            post_data = {
                "bank_name": str(data.bank_name),
                "bank_account": str(bank_account),
                "bank_utr": str(row['Unnamed: 3']),
                "trading_info": str(row['Unnamed: 2'].strip(" ")),
                "amount": amount,
                "channel_code": str(data.channel_code),
                "trading_time": str(row['Unnamed: 0']),
                "account_balance": balance,
                # "random_number": random_number,
                "info_sources": "backend",
                "collection_type": "entry",
                "match_type": "unmatch",
                "file_name": str(data.file_name)
            }

            coll_data = {
                "bank_utr": str(row['Unnamed: 3']),
                "amount": amount,
                "random_number": random_number
            }
            collList.append(coll_data)
            dataList.append(post_data)

    if len(dataList) > 0:
        # 批量导入
        await save_collData(db, dataList, collList)
        # res = await DUPLICATE_UPDATEd(db, dataList)
        # print("批量导入返回值-------->>>>>>>>>", res)
        # if res == 'success':
        #     headers = {"content-type": "application/json"}
        #     url = 'http://127.0.0.1:8060/yg/collorder/update'
        #     async with aiohttp.ClientSession() as session:
        #         async with session.post(url, headers=headers, json=collList) as response:
        #             await response.text()

    return {"filename": data.file_name}