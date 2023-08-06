#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime
import logging
from pathlib import Path


import openpyxl
from openpyxl.utils import column_index_from_string, get_column_letter

import pandas

from .parse import get_sheet_type


logger = logging.getLogger(__name__)


class Convert:

    def __init__(self, input_path, output_path, directory):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.directory = Path(directory)
        self.check()

    def check(self):
        assert self.directory.exists(), f"{self.directory}不存在"
        assert self.input_path.exists(), f"{self.input_path}不存在"

    @classmethod
    def paste_convert(cls, input_path, output, directory):
        cls(input_path, output, directory).run()

    def run(self):
        self.load_data()
        SichuanConvert(
            sheet=self.sheet,
            directory=self.directory,
        ).run()
        TianjinConvert(
            sheet=self.sheet,
            directory=self.directory,
        ).run()
        self.wb.save(self.output_path)

    def load_data(self):
        self.wb = openpyxl.load_workbook(self.input_path)
        self.sheet = self.wb.active


class BaseConvert:
    FILE_PATTERN = None

    def __init__(self, sheet, directory):
        self.sheet = sheet
        self.directory = directory

    def run(self):
        self.data = self.get_data()
        self.paste()

    def get_file(self):
        name = self.FILE_PATTERN
        directory = self.directory
        if not name:
            raise NotImplementedError
        pattern = f"*{name}*.xlsx"
        files = list(directory.glob(pattern))
        if len(files) == 1:
            return files[0]
        if len(files) == 0:
            return f"{directory}里面不存在 {name} 的xlsx文件"
        return f"{directory}里面有不止1个{name}的xlsx文件"

    def get_data(self):
        data = self.parse_data(self.get_file())
        return data

    def paste(self):
        ws = self.sheet
        data = self.data
        # 收获数
        for _type, _type_data in data.items():
            position = self.get_position(_type)
            logger.info(f"数据粘贴位置： {position}")
            for date, value in _type_data.items():
                for key, number in value.items():
                    row = position[key]
                    column = get_column_letter(
                        column_index_from_string(position["column"]) + date.day - 1
                    )
                    if number:
                        logger.info(f"修改{column}{row}为{number}")
                        ws[f"{column}{row}"].value = number


class SichuanConvert(BaseConvert):
    FILE_PATTERN = "库存滚动日报表_2022"

    def parse_data(self, path, end=None):
        """
        解析四川一汽丰通的日报
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
            path, names=['日期', None, None, None, "收货数", "发货数MP", "其他出货"],
            header=9,
            index_col="日期",
            usecols=["日期", "收货数", "发货数MP", "其他出货"],
            sheet_name=list(sheet_name_type.keys()),
        )
        result = {}
        for sheet_name, df in df_dict.items():
            df = df[df.index.notnull()]
            df = df[~pandas.to_datetime(df.index, errors="coerce").isnull()]
            _type = sheet_name_type[sheet_name]
            result[_type] = df[df.index < end].to_dict(orient="index")
        return result

    def get_position(self, _type):
        """
        Parameters:
            _type: 部品番号 4265A-0N011
        Return:
            粘贴位置 {
                "收获数": 2248(row),
                "发货数": 2249(1 index row),
                "其他出货": 2250,
                "column": "I"
            }
        """
        ws = self.sheet
        result = {"column": "I"}
        e_index = column_index_from_string('E') - 1
        _type_index = column_index_from_string('D') - 1
        column_index = column_index_from_string('G') - 1
        for index, row in enumerate(ws.rows, 1):
            e_value = row[e_index].value
            if e_value \
                    and "四川成都" in e_value \
                    and "丰通" in e_value \
                    and row[_type_index].value == _type:
                if row[column_index].value in ["收货数", "发货数MP", "其他出货"]:
                    result[row[column_index].value] = index
        logger.info(result)
        return result


class TianjinConvert(BaseConvert):
    FILE_PATTERN = "在库表-YH 2022"

    def get_position(self, _type):
        """
        Parameters:
            _type: 部品番号 4265A-0N011
        Return:
            粘贴位置 {
                "收获数": 2248(row),
                "发货数": 2249(1 index row),
                "其他出货": 2250,
                "column": "I"
            }
        """
        ws = self.sheet
        result = {"column": "I"}
        e_index = column_index_from_string('E') - 1
        _type_index = column_index_from_string('D') - 1
        column_index = column_index_from_string('G') - 1
        for index, row in enumerate(ws.rows, 1):
            e_value = row[e_index].value
            if e_value \
                    and "一汽丰田" in e_value \
                    and "丰通" in e_value \
                    and row[_type_index].value == _type:
                if row[column_index].value in ["收货数", "发货数MP", "其他出货"]:
                    result[row[column_index].value] = index
        logger.info(result)
        return result

    def parse_data(self, path, end=None):
        """
        解析天津一汽丰通的日报
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
            path,
            names=[
                '日期', None, None, "D", "收货数",
                None, None, None, None, None,
                "发货数MP", "其他出货"],
            header=9,
            index_col="日期",
            usecols=["日期", "收货数", "发货数MP", "其他出货"],
            sheet_name=list(sheet_name_type.keys()),
        )
        result = {}
        for sheet_name, df in df_dict.items():
            df = df[df.index.notnull()]
            df = df[~pandas.to_datetime(df.index, errors="coerce").isnull()]
            _type = sheet_name_type[sheet_name]
            result[_type] = df[df.index < end].to_dict(orient="index")
        return result


paste_convert = Convert.paste_convert
