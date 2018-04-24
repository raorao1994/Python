#!/usr/bin/evn python
# coding=utf-8

import unittest
from common import string_helper


class StringHelperTest(unittest.TestCase):
    """字符串操作包测试类"""

    def setUp(self):
        """初始化测试环境"""
        print('------ini------')

    def tearDown(self):
        """清理测试环境"""
        print('------clear------')

    def test_is_email(self):
        self.assertEqual(string_helper.is_email('aaaaa'), False)
        self.assertEqual(string_helper.is_email('aaaa@xxx.com'), True)
        self.assertEqual(string_helper.is_email('xxx@xxx.com.xx'), True)

    def test_is_phone(self):
        self.assertEqual(string_helper.is_phone('aaaaa'), False)
        self.assertEqual(string_helper.is_phone('12345678'), False)
        self.assertEqual(string_helper.is_phone('01012345678'), True)
        self.assertEqual(string_helper.is_phone('010-123456'), False)
        self.assertEqual(string_helper.is_phone('010-12345678'), True)
        self.assertEqual(string_helper.is_phone('010 12345678'), True)
        self.assertEqual(string_helper.is_phone('0757 12345678'), True)

    def test_is_mobile(self):
        self.assertEqual(string_helper.is_mobile('aaaaa'), False)
        self.assertEqual(string_helper.is_mobile('123456789'), False)
        self.assertEqual(string_helper.is_mobile('13012345678'), True)
        self.assertEqual(string_helper.is_mobile('14012345678'), False)

    def test_is_letters(self):
        self.assertEqual(string_helper.is_letters('123456'), False)
        self.assertEqual(string_helper.is_letters('1ds2f12sdf'), False)
        self.assertEqual(string_helper.is_letters('absbdsf'), True)
        self.assertEqual(string_helper.is_letters('ADdfFSds'), True)

    def test_is_idcard(self):
        self.assertEqual(string_helper.is_idcard('123456789'), False)
        self.assertEqual(string_helper.is_idcard('aaaaaaaaa'), False)
        self.assertEqual(string_helper.is_idcard('340223190008210470'), False)
        self.assertEqual(string_helper.is_idcard('34022319000821047X'), True)

    def test_filter_str(self):
        print(string_helper.filter_str('aaa'))
        print(string_helper.filter_str('aaa<>&\''))
        print(string_helper.filter_str('aaa<|>|&|%|~|^|;|\''))

    def test_filter_tags(self):
        print(string_helper.filter_tags('<html><body><b>aaa</b></body></html>'))

    def test_string(self):
        print(string_helper.string(-1))
        print(string_helper.string({'test': 'abc'}))
        print(string_helper.string(''))
        print(string_helper.string('aaa'))
        print(string_helper.string('', True))

    def test_cut_str(self):
        print(string_helper.cut_str('', 5))
        print(string_helper.cut_str('aaa', 5))
        print(string_helper.cut_str('将字符串截取指定长度', 5))
        print(string_helper.cut_str('aa将字符串截取指定长度', 5))


if __name__ == '__main__':
    unittest.main()
