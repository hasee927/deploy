# import time
# import pandas as pd
import csv
from apps.yinggao.banklist.help.utils import save_collData


async def cab(data ,db):
    bank_account = ''
    dataList = []
    collList = []
    csvfile = 'static/uploads/' + data.file_name

    with open(csvfile, 'r') as file:
        reader = csv.reader(file)
        # print(reader)

        for row in reader:
            if len(row) > 0:
                if row[0].strip(" ") == 'Account Number':
                    bank_account = row[1].strip('"').strip("=").strip(" ").strip('"')
                    # print(bank_account)

                if len(row) > 3:
                    if  row[3].find('UPI') > -1 and row[3].split("/")[1] == "CR":
                        # print(row)
                        utr = row[3].split("/")[2]
                        temp_random = row[3].split("/")[6]
                        random_number = ''
                        if temp_random:
                            if not temp_random == "NA":
                                random_number = temp_random

                        # # 去掉金额中的逗号
                        tmp_amount = str(row[-2]).strip("=").strip(" ").strip('"')
                        amount = str(float(''.join(tmp_amount.split(','))))

                        tmp_balance = str(row[-1]).strip("=").strip(" ").strip('"')
                        balance = str(float(''.join(tmp_balance.split(','))))


                        post_data = {
                            "bank_name": str(data.bank_name),
                            "bank_account": str(bank_account),
                            "bank_utr": str(utr),
                            "trading_info": row[3].strip(' '),
                            "amount": amount,
                            "channel_code": str(data.channel_code),
                            "trading_time": '',
                            "account_balance": balance,
                            "info_sources": "backend",
                            "collection_type": "entry",
                            "match_type": "unmatch",
                            "file_name": str(data.file_name)
                        }
                        coll_data = {
                            "bank_utr": str(utr),
                            "amount": amount,
                            "random_number": random_number
                        }
                        collList.append(coll_data)
                        dataList.append(post_data)



    if len(dataList) > 0:
        # 批量导入
        await save_collData(db, dataList, collList)
    return {"filename": data.file_name}





# # 企业版
# async def cab(data ,db):
#     csvfile = 'static/uploads/' + data.file_name
#     newCsvFile = "static/uploads/" + "AA_" + data.file_name
#     fc = open(newCsvFile, "w+")
#     with open(csvfile, 'r') as f:
#         lines = f.readlines()
#         for line in lines[27:]:
#             if line.find("CR") > 0:
#                 fc.write(line)
#                 fc.flush()
#     fc.close()
#     dataList = []
#
#     csv = pd.read_csv(newCsvFile)
#     for index, row in csv.iterrows():
#         utr = row[3].split("/")[2]
#
#         # 去掉金额中的逗号
#         tmp_amount = str(row[-2]).strip(" ")
#         amount = str(float(''.join(tmp_amount.split(','))))
#         tmp_balance = str(row[-1]).strip(" ")
#         balance = str(float(''.join(tmp_balance.split(','))))
#
#         post_data = {
#             "bank_name": str(data.bank_name),
#             "bank_account": str(data.bank_account),
#             "bank_utr": str(utr),
#             "trading_info": str(row[3]),
#             "amount": amount,
#             "channel_code": str(data.channel_code),
#             "trading_time": str(row[0]),
#             "account_balance": balance,
#             "info_sources": "backend",
#             "collection_type": "entry",
#             "match_type": "unmatch",
#             "file_name": str(data.file_name)
#         }
#         dataList.append(post_data)
#
#     if len(dataList) > 0:
#         # 批量导入
#         await DUPLICATE_UPDATEd(db, dataList)
#
#     return {"filename": data.file_name, "count": len(dataList)}