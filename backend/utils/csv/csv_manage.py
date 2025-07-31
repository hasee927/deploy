#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/5/6 17:25 
# @File           : excel_manage.py
# @IDE            : PyCharm
# @desc           : EXCEL 文件操作

import datetime, csv
import os
import re
from pathlib import Path
from typing import Dict

from application.settings import STATIC_ROOT, STATIC_URL
from utils.file.file_base import FileBase



class CsvManage:

    def __init__(self):
        self.wb = None


    def create_csv(self, column_names: list = None, rows: list = None) -> dict[str, str]:
        file_path = FileBase.generate_static_file_path(path='csv_manage', suffix="csv")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)  # 写入列名
            writer.writerows(rows)  # 写入数据行
            file.flush()
            file.close()

        return { "local_path": file_path, "remote_path": file_path.replace(STATIC_ROOT, STATIC_URL) }


