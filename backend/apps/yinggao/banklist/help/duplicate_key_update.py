from sqlalchemy import text

async def DUPLICATE_UPDATEd(db, dataList):

    tempList = []
    table_name = (f"INSERT INTO yg_bank_list(bank_name,channel_code,bank_account,bank_utr,amount,account_balance,"
                  f"trading_time,trading_info,info_sources,match_type,collection_type,file_name,create_datetime,"
                  f"update_datetime,is_delete) VALUES")
    # 处理批量导入的值
    for item in dataList:
        value = (f"('{item['bank_name']}','{item['channel_code']}','{item['bank_account']}','{item['bank_utr']}',"
                 f"'{item['amount']}','{item['account_balance']}','{item['trading_time']}','{item['trading_info']}',"
                 f"'{item['info_sources']}','{item['match_type']}','{item['collection_type']}','{item['file_name']}',NOW(),NOW(),0)")
        tempList.append(value)

    joined_values = ','.join(tempList)
    # 批量导入如果bank_utr有值，则更新【ON DUPLICATE KEY UPDATE bank_utr = VALUES(bank_utr)】
    # sql = text(f"{table_name}{joined_values}  AS alias ON DUPLICATE KEY UPDATE bank_utr = VALUES(bank_utr);")
    sql = text(f"{table_name}{joined_values}  AS alias ON DUPLICATE KEY UPDATE bank_utr = alias.bank_utr;")
    await db.execute(sql)
    await db.commit()

    return "success"