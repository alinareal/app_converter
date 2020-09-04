from argparse import ArgumentParser
from datetime import date, datetime
from decimal import Decimal, ROUND_UP, DecimalException
from typing import Tuple

import requests
from bs4 import BeautifulSoup

DATE_FORMAT = '%d/%m/%Y'
CROSS_CURRENCY = 'RUR'
ROUNDING = '.0001'
URL = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req={currency_date}'
PARSER = 'xml'

today = date.today()
current_date = today.strftime(DATE_FORMAT)


def get_args() -> ArgumentParser:
    args = ArgumentParser(prog='Currency Converter',
                          description='Currency converter. For example: to convert 100 USD to RUB '
                                      'on July 15th 2018, it would be 100 USD RUB 15/07/2018. '
                                      'If you do not specify date: 100 USD RUB, '
                                      'you will get amount according to current date.',
                          epilog='(c) Alina Laevskaya 2020.'
                          )

    args.add_argument('amount', type=str, help='Amount of currency to convert')
    args.add_argument('currency_in', type=str, help='Currency to convert')
    args.add_argument('currency_out', type=str, help='Currency to be converted into')

    args.add_argument('-d', '--currency_date', type=str, help='Currency date',
                      default=current_date)
    return args


def get_nominal_and_value(currency: str, soup: BeautifulSoup) -> Tuple[Decimal, Decimal]:
    try:
        currency_tag = soup.find('CharCode', text=currency)
        nominal = currency_tag.find_next_sibling().text
        value = currency_tag.find_next_sibling(name='Value').text.replace(',', '.')
    except AttributeError:
        raise ValueError('Incorrect currency char code: ' + currency)
    print(type(currency), type(soup))
    return Decimal(nominal), Decimal(value)


def check_date(date_: str) -> None:
    try:
        datetime.strptime(date_, DATE_FORMAT)
    except ValueError:
        raise ValueError('Incorrect date format! Should be {date_format}'.format(date_format=DATE_FORMAT))


def check_amount(number: str) -> None:
    try:
        Decimal(number)
    except DecimalException:
        raise ValueError('Amount should be a number!')
    if Decimal(number) <= 0:
        raise ValueError('Amount should be above zero!')


def convert(amount: str, currency_in: str, currency_out: str, currency_date: str = current_date) -> Decimal:
    check_date(currency_date)
    check_amount(amount)

    url = URL.format(currency_date=currency_date)

    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(markup=content, features=PARSER)

    if currency_in == currency_out:
        result = Decimal(amount)
    elif currency_in == CROSS_CURRENCY:
        nominal_out, value_out = get_nominal_and_value(currency_out, soup)
        result = Decimal(amount) / (Decimal(value_out) / Decimal(nominal_out))
    elif currency_out == CROSS_CURRENCY:
        nominal_in, value_in = get_nominal_and_value(currency_in, soup)
        result = Decimal(value_in) / Decimal(nominal_in) * Decimal(amount)
    else:
        nominal_in, value_in = get_nominal_and_value(currency_in, soup)
        nominal_out, value_out = get_nominal_and_value(currency_out, soup)
        result = (value_in / nominal_in) / (value_out / nominal_out) * Decimal(amount)

    result = result.quantize(Decimal(ROUNDING), rounding=ROUND_UP)
    return result


def main():
    args = get_args()
    namespace = args.parse_args()
    converted = convert(
        namespace.amount,
        namespace.currency_in,
        namespace.currency_out,
        namespace.currency_date
    )
    print(converted)


if __name__ == '__main__':
    main()
