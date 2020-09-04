import unittest
from decimal import Decimal

from currency_converter import convert

TEST_DATE_1 = '17/02/2005'
TEST_DATE_2 = '17/02/2015'
TEST_DATE_3 = '18/07/2001'
TEST_DATE_4 = '25/12/2018'


class TestParsing(unittest.TestCase):

    def test1(self):
        result = convert('500', 'AUD', 'EUR', TEST_DATE_1)
        expected = Decimal('300.8220')
        self.assertEqual(result, expected)

    def test2(self):
        result = convert('345', 'RUR', 'RUR', TEST_DATE_1)
        expected = Decimal('345')
        self.assertEqual(result, expected)

    def test3(self):
        result = convert('800', 'AMD', 'RUR', TEST_DATE_2)
        expected = Decimal('104.6568')
        self.assertEqual(result, expected)

    def test4(self):
        result = convert('700', 'RUR', 'EUR', TEST_DATE_2)
        expected = Decimal('9.7844')
        self.assertEqual(result, expected)

    def test5(self):
        result = convert('1000', 'BGN', 'BGN', TEST_DATE_2)
        expected = Decimal('1000')
        self.assertEqual(result, expected)

    def test6(self):
        result = convert('300', 'HUF', 'DKK', TEST_DATE_2)
        expected = Decimal('7.2884')
        self.assertEqual(result, expected)

    def test7(self):
        result = convert('550', 'DKK', 'INR', TEST_DATE_2)
        expected = Decimal('5246.9271')
        self.assertEqual(result, expected)

    def test8(self):
        result = convert('600', 'KZT', 'BRL', TEST_DATE_2)
        expected = Decimal('9.1832')
        self.assertEqual(result, expected)

    def test9(self):
        self.assertRaises(ValueError, convert, '-500', 'AUD', 'EUR', TEST_DATE_2)

    def test10(self):
        self.assertRaises(ValueError, convert, '500', 'AUD', 'EUR', '17.02.2005')

    def test11(self):
        result = convert('500', 'AUD', 'EUR')
        expected = Decimal('304.1995')
        self.assertEqual(result, expected)

    def test12(self):
        self.assertRaises(ValueError, convert, '600', 'bls', 'BRL', TEST_DATE_2)

    def test13(self):
        self.assertRaises(ValueError, convert, '600', 'BLR', 'dfd', TEST_DATE_2)

    def test14(self):
        self.assertRaises(ValueError, convert, '0', 'AUD', 'EUR', TEST_DATE_2)

    def test15(self):
        self.assertRaises(ValueError, convert, 'hello', 'AUD', 'EUR', TEST_DATE_2)
        
    def test16(self):
        result = convert('100', 'AUD', 'EUR', TEST_DATE_3)
        expected = Decimal('59.5095')
        self.assertEqual(result, expected)

    def test17(self):
        result = convert('671', 'EUR', 'AUD', TEST_DATE_3)
        expected = Decimal('1127.5521')
        self.assertEqual(result, expected)

    def test18(self):
        result = convert('6543', 'AUD', 'RUR', TEST_DATE_3)
        expected = Decimal('96836.4000')
        self.assertEqual(result, expected)

    def test19(self):
        result = convert('876', 'RUR', 'EUR', TEST_DATE_4)
        expected = Decimal('11.2469')
        self.assertEqual(result, expected)

    def test20(self):
        result = convert('2000', 'BGN', 'BGN', TEST_DATE_4)
        expected = Decimal('2000.0000')
        self.assertEqual(result, expected)

    def test21(self):
        result = convert('7654', 'HUF', 'DKK', TEST_DATE_4)
        expected = Decimal('177.6016')
        self.assertEqual(result, expected)
    

if __name__ == '__main__':
    unittest.main()
