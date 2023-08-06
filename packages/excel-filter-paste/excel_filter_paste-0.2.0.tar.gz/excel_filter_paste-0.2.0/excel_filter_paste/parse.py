#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime

import pandas


def glob(directory, name):
    pattern = f"*{name}*.xlsx"
    files = list(directory.glob(pattern))
    if len(files) == 1:
        return files[0]
    if len(files) == 0:
        return f"{directory}里面不存在 {name} 的xlsx文件"
    return f"{directory}里面有不止1个{name}的xlsx文件"


def parse_data(path, end=None):
    """
    解析丰通的日报
    Parameters:
        path: 文件路径
        end: datetime.date
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
        end = datetime.date.today()
    end = pandas.Timestamp(end)
    df = pandas.read_excel(
        path, names=['日期', None, None, "D", "E", "F", "G"],
        header=9,
        index_col="日期",
        usecols=["日期", "D", "E", "F", "G"],
    )
    df = df[df.index.notnull()]
    df = df[~pandas.to_datetime(df.index, errors="coerce").isnull()]
    result = df[df.index < end].to_dict(orient="index")
    return result


def get_fengtong_file(path):
    return glob(path, "丰通日报")
