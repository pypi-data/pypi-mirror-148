#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime
import logging
from pathlib import Path


import openpyxl
from openpyxl.utils import column_index_from_string, get_column_letter

import pandas

from .parse import parse_data, get_fengtong_file


logger = logging.getLogger(__name__)


def get_fengtong(ws):
    """
    Parameters:
        workshee
        找G列存在丰通的行
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
    # 处理丰通
    data = parse_data(get_fengtong_file(directory))
    index = get_fengtong(ws)
    for date, value in data.items():
        column = get_column_letter(
            index["column"] + date.day - 1)
        row = index["row"]
        logger.info(f"修改{column}{row}为{value['D']}")
        ws[f"{column}{row}"].value = value["D"]
    wb.save(output)
