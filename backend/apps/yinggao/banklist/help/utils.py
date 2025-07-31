from application.settings import PayAddr
from apps.yinggao.banklist.help.duplicate_key_update import DUPLICATE_UPDATEd
import aiohttp



async def save_collData(db, dataList, collList):
    # 批量导入
    res = await DUPLICATE_UPDATEd(db, dataList)
    print("批量导入返回值-------->>>>>>>>>", res)
    if res == 'success':
        headers = {"content-type": "application/json"}
        url = f'{PayAddr}/yg/collorder/update'
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=collList) as response:
                await response.text()