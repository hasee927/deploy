from apps.yinggao.banklist.help.duplicate_key_update import DUPLICATE_UPDATEd
import xmltodict

async def equ(data ,db):
    jsonList = []
    dataList = []
    excel_file = 'static/uploads/' + data.file_name
    with open(excel_file, encoding='gbk', errors='ignore') as file:
        xml_data = file.read()

    data_dict = xmltodict.parse(xml_data)

    WorkbookList = (data_dict['Workbook']['Worksheet']['ss:Table']['Row'])
    for item in WorkbookList:
        strItem = str(item)
        if strItem.find('UPI REF NO') > -1:
            tempList = []
            for row in item['Cell']:
                value = row['Data']['#text']
                tempList.append(value.replace("\n", ""))

            jsonList.append(tempList)


    for row in jsonList:
        # 去掉金额中的逗号
        tmp_amount = str(row[-2]).strip(" ")
        amount = str(float(''.join(tmp_amount.split(','))))
        tmp_balance = str(row[-1]).strip(" ")
        balance = str(float(''.join(tmp_balance.split(','))))
        utr = row[2].split(' ')[3]

        post_data = {
            "bank_name": str(data.bank_name),
            "bank_account": str(data.bank_account),
            "bank_utr": utr,
            "trading_info": str(row[2].strip(" ")), #流水详情
            "amount": amount,
            "channel_code": str(data.channel_code),
            "trading_time": row[0],
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