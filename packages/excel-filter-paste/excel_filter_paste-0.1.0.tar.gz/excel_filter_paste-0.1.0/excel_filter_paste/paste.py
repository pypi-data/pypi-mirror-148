#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime
import logging
from pathlib import Path


import openpyxl
from openpyxl.utils import column_index_from_string, get_column_letter

import pandas


logger = logging.getLogger(__name__)


def parse_data(path, end=None):
    """
    Parameters:
        path: 文件路径
    Returns:
        {
            TimeStamp("2022-04-01"): {
                "D": 1,
                "E": 2,
                "F": 3,
                "G": 4,
            }
        }
    """
    if end is None:
        end = str(datetime.date.today())
    df = pandas.read_excel(
        path, names=['日期', None, None, "D", "E", "F", "G"],
        header=9,
        index_col="日期",
        usecols=["日期", "D", "E", "F", "G"],
    )
    return df[df.index < end].to_dict(orient="index")


def get_fengtong(ws):
    """
    Parameters:
        workshee
    Returns:
        row: 2248
        column: 1(对应A)
    """
    result = {}
    column_index = column_index_from_string('G') - 1
    for index, row in enumerate(ws.rows):
        if row[column_index].value:
            if "天津丰通（一工厂）" in row[column_index].value:
                if "row" in result:
                    raise Exception(f"{result['row']}, {index}两行同时符合")
                result["row"] = index + 1
    assert "row" in result, "没找到天津丰通（一工厂）"
    result["column"] = column_index_from_string("I")
    logger.info(f"起始位置: {result}")
    return result


def paste_convert(input_path, output, directory):
    input_path = Path(input_path)
    directory = Path(directory)
    assert directory.exists(), f"{directory}不存在"
    assert input_path.exists(), f"{input_path}不存在"
    wb = openpyxl.load_workbook(input_path)
    ws = wb.active
    for i in directory.iterdir():
        if "丰通日报" in i.name:
            data = parse_data(i)
            index = get_fengtong(ws)
            for date, value in data.items():
                column = get_column_letter(
                    index["column"] + date.day - 1)
                row = index["row"]
                logger.info(f"修改{column}{row}为{value['D']}")
                ws[f"{column}{row}"].value = value["D"]
    wb.save(output)
