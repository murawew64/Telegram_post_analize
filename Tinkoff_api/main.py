import configparser
from openapi_client import openapi
import csv
import time
from datetime import date, datetime, timedelta


def get_company_info(client, tiker, date):
    '''
    В данной функции 2 запроса к API

    'c' - цена закрытия
    'o' - цена открытия
    'h' - максимальная цена торгов
    'l' - минимальная цена торгов
    '''
    # -! ЗАПРОС
    res = client.market.market_search_by_ticker_get(tiker)
    print(res)
    company_info = res.to_dict()
    figi = company_info['payload']['instruments'][0]['figi']
    print(figi)

    start_date = str(date).replace(' ', 'T')
    print(start_date)
    end_date = str(date + timedelta(days=31)).replace(' ', 'T')
    print(end_date)

    # -! ЗАПРОС
    market_info = client.market.market_candles_get(
        figi, start_date, end_date, 'week').to_dict()

    if market_info['status'] == 'Ok':
        return market_info['payload']['candles']
    else:
        print('Error')
        exit(1)


def write_row_to_csv(writer, old_row, company_info):
    new_row = []
    for info in company_info:
        new_row.append(info['c'])
        new_row.append(info['o'])
        new_row.append(info['h'])
        new_row.append(info['l'])

    old_row[1] = old_row[1].strip()
    old_row.extend(new_row)
    writer.writerow(old_row)


def create_header():
    week1_header = ['week1_close', 'week1_open', 'week1_high', 'week1_low']
    week2_header = ['week2_close', 'week2_open', 'week2_high', 'week2_low']
    week3_header = ['week3_close', 'week3_open', 'week3_high', 'week3_low']
    week4_header = ['week4_close', 'week4_open', 'week4_high', 'week4_low']
    header = ['date', 'content', 'tiker']
    header.extend(
        week1_header + week2_header + week3_header + week4_header)

    return header


def create_dataset(client, last_index, data_path):
    '''
    Скрипт точно знает на какой записи остановилась обработка.
    '''
    # create log file (логи пищутся в конец)
    log = open('log.log', 'a')
    log_err = open('log_err.log', 'a')

    # find valid date
    date_mounth_ago = date.today() - timedelta(days=31)

    with open(data_path, 'r', encoding='utf-8') as inp, open('data.csv', 'a', encoding='utf-8', newline='') as out:
        reader = csv.reader(inp, delimiter=',')
        writer = csv.writer(out, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        if last_index == 0:
            writer.writerow(create_header())

        # skip header
        reader.__next__()
        # --------
        INDEX = 75
        end_index = 0
        # --------
        for index, row in enumerate(reader):
            # дата публикации поста, требуется еще
            post_date = datetime.fromisoformat(row[0])

            if post_date.date() < date_mounth_ago and index > last_index:
                print(row)
                try:
                    company_info = get_company_info(client, row[2], post_date)
                except IndexError:
                    log_err.write(f'{index}\n')
                    continue
                except:
                    print('Too many request!!!')
                    return

                write_row_to_csv(writer, row, company_info)
                end_index += 1
                log.write(f'{index}\n')

            if end_index == INDEX:
                end_index = 0
                time.sleep(180)


def find_last_row(index_file_path):
    try:
        with open(index_file_path, 'r') as f:
            last_line = f.readlines()[-1]
    except FileNotFoundError:
        return 0

    return int(last_line)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    token = config['TOKEN']['api_token']
    client = openapi.api_client(token)

    last_index = find_last_row('log.log')

    create_dataset(
        client, last_index, r'D:\program1\Projects\Lemtuznicova news\collect_telegram_posts\data.csv')


if __name__ == '__main__':
    main()
