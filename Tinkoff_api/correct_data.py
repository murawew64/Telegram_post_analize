import csv
from os import write


def main():
    '''
    По некоторым компаниям собрались результаты больше чем за 4 недели (больше 16 значений)
    '''
    with open(r'D:\program1\Projects\Lemtuznicova news\Tinkoff_api\data.csv', 'r', encoding='utf-8') as f_in, open(r'corr_data.csv', 'w', encoding='utf-8', newline='') as f_out:
        reader = csv.reader(f_in, delimiter=',')
        writer = csv.writer(f_out,  delimiter=',', quoting=csv.QUOTE_MINIMAL)

        for index, row in enumerate(reader):
            if len(row) > 19:
                print(index)
                row = row[:19]
            writer.writerow(row)


if __name__ == '__main__':
    main()
