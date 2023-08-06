#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime
import logging

import pandas
import re

from openpyxl import load_workbook


logger = logging.getLogger(__name__)


def glob(directory, name):
    pattern = f"*{name}*.xlsx"
    files = list(directory.glob(pattern))
    if len(files) == 1:
        return files[0]
    if len(files) == 0:
        return f"{directory}里面不存在 {name} 的xlsx文件"
    return f"{directory}里面有不止1个{name}的xlsx文件"


def get_type(string):
    """
    返回括号内的数值
    Parameters:
        "2022-04 (aabb-cc) AY8A"
    Returns:
        "aabb-cc"
    """
    try:
        return re.split(r'[\(\)（）]', string)[1]
    except Exception:
        raise Exception(f"{string}格式不正确")


def get_sheet_type(path):
    """
    返回丰通的dict
    Returns:
        {
            "sheet_name": "typename"
        }
    """
    wb = load_workbook(path)
    result = {}
    for sheetname in wb.sheetnames:
        sheet = wb[sheetname]
        _type = get_type(sheet["A3"].value)
        result[sheetname] = _type
    return result


def parse_data(path, end=None):
    """
    解析丰通的日报
    Parameters:
        path: 文件路径
        end: datetime.date
    Returns:
        {
            {
                "type1": {
                    TimeStamp("2022-04-01"): {
                        "D": 1,
                        "收货数": 2,
                        "发货数": 3,
                        "其他出货 4,
                    }
                }
            }
        }
    """
    sheet_name_type = get_sheet_type(path)
    if end is None:
        end = datetime.date.today()
    end = pandas.Timestamp(end)
    df_dict = pandas.read_excel(
        path, names=['日期', None, None, "D", "收货数", "发货数", "其他出货"],
        header=9,
        index_col="日期",
        usecols=["日期", "D", "收货数", "发货数", "其他出货"],
        sheet_name=None,
    )
    result = {}
    for sheet_name, df in df_dict.items():
        df = df[df.index.notnull()]
        df = df[~pandas.to_datetime(df.index, errors="coerce").isnull()]
        _type = sheet_name_type[sheet_name]
        result[_type] = df[df.index < end].to_dict(orient="index")
    return result


def get_fengtong_file(path):
    result = glob(path, "丰通日报")
    logger.info("找到文件: {result}")
    return result
