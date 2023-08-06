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


def get_fengtong_base(ws, _type, name):
    """
    找到收货数放在哪一行
    找E列存在丰通的行
    Parameters:
        workshee
        _type
    Returns:
        row: 2248
        column: I
    """
    logger.info(f"准备把{_type}数据填写到: ")
    result = {"column": "I"}
    e_index = column_index_from_string('E') - 1
    _type_index = column_index_from_string('D') - 1
    column_index = column_index_from_string('G') - 1
    for index, row in enumerate(ws.rows, 1):
        e_value = row[e_index].value
        if e_value \
                and "四川成都" in e_value \
                and "丰通" in e_value \
                and row[_type_index].value == _type \
                and row[column_index].value == name:
            result["row"] = index
            break
    else:
        raise Exception("没有找到合适的位置")
    logger.info(result)
    return result


def get_fengtong(ws, _type):
    """
    找到发货数放在哪一行
    找E列存在丰通的行
    Parameters:
        workshee
        _type
    Returns:
        row: 2248
        column: I
    """
    return get_fengtong_base(ws, _type, "收货数")


def get_fengtong_send(ws, _type):
    return get_fengtong_base(ws, _type, "发货数MP")


def get_fengtong_other_send(ws, _type):
    return get_fengtong_base(ws, _type, "其他出货")


def paste_convert(input_path, output, directory):
    input_path = Path(input_path)
    directory = Path(directory)
    assert directory.exists(), f"{directory}不存在"
    assert input_path.exists(), f"{input_path}不存在"
    wb = openpyxl.load_workbook(input_path)
    ws = wb.active
    # 处理丰通
    data = parse_data(get_fengtong_file(directory))
    # 收货数
    for _type, _type_data in data.items():
        index = get_fengtong(ws, _type)
        for date, value in _type_data.items():
            column = get_column_letter(
                column_index_from_string(index["column"]) + date.day - 1
            )
            row = index["row"]
            if value["收货数"]:
                logger.info(f"修改{column}{row}为{value['收货数']}")
                ws[f"{column}{row}"].value = value["收货数"]
    # 发货数
    for _type, _type_data in data.items():
        index = get_fengtong_send(ws, _type)
        for date, value in _type_data.items():
            column = get_column_letter(
                column_index_from_string(index["column"]) + date.day - 1
            )
            row = index["row"]
            if value["发货数"]:
                logger.info(f"修改{column}{row}为{value['发货数']}")
                ws[f"{column}{row}"].value = value["发货数"]
    # 其他出货
    for _type, _type_data in data.items():
        index = get_fengtong_send(ws, _type)
        for date, value in _type_data.items():
            column = get_column_letter(
                column_index_from_string(index["column"]) + date.day - 1
            )
            row = index["row"]
            if value["其他出货"]:
                logger.info(f"修改{column}{row}为{value['其他出货']}")
                ws[f"{column}{row}"].value = value["其他出货"]
    wb.save(output)
