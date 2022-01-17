from telethon.sync import TelegramClient
from telethon import utils
import asyncio
import configparser
import csv
import re
from collections import OrderedDict
# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.


class FormatText:

    def __init__(self, text):
        self.text = text

    def format_one_tiker(self):
        # pipeline
        self.delete_tikers()
        self.delete_start_dot()
        self.delete_double_stars()
        self.delete_spec_symbols()
        self.delete_links()
        self.delete_round_brackets()
        self.delete_footer()
        self.delete_new_lines()
        self.delete_colon()
        self.delete_square_brackets()

        return self.text

    def format_many_tikers(self):
        # pipeline
        self.delete_start_dot()
        self.delete_double_stars()
        self.delete_spec_symbols()
        self.delete_links()
        self.delete_round_brackets()
        self.delete_footer()
        self.delete_colon()

        return self.text

    def delete_tikers(self):
        reg_tikers = re.compile(r'\[[A-Z]*\]')
        self.text = reg_tikers.sub(r'', self.text)

    def delete_start_dot(self):
        self.text = self.text.replace('•', '')

    def delete_double_stars(self):
        self.text = self.text.replace('**', '')

    def delete_spec_symbols(self):
        emoj = re.compile("["
                          u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          u"\U00002500-\U00002BEF"  # chinese char
                          u"\U00002702-\U000027B0"
                          u"\U00002702-\U000027B0"
                          u"\U000024C2-\U0001F251"
                          u"\U0001f926-\U0001f937"
                          u"\U00010000-\U0010ffff"
                          u"\u2640-\u2642"
                          u"\u2600-\u2B55"
                          u"\u200d"
                          u"\u23cf"
                          u"\u23e9"
                          u"\u231a"
                          u"\ufe0f"  # dingbats
                          u"\u3030"
                          "]+", re.UNICODE)
        self.text = emoj.sub(r'', self.text)

    def delete_links(self):
        reg_link = r'((http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]))'
        # print(re.findall(reg_link, res))
        self.text = re.sub(reg_link, '', self.text)

    def delete_round_brackets(self):
        self.text = self.text.replace('(', '').replace(')', '')

    def delete_footer(self):
        reg_footer = r'([#|@][\S|\d]*)'
        # print(re.findall(reg_footer, res))
        self.text = re.sub(reg_footer, '', self.text)

    def delete_new_lines(self):
        self.text = self.text.replace('\n', ' ')

    def delete_colon(self):
        self.text = self.text.replace(':', ' ')

    def delete_square_brackets(self):
        self.text = self.text.replace('[', '').replace(']', '')


def delete_tikers(text):
    reg_tikers = re.compile(r'\[[A-Z]*\]')
    return reg_tikers.sub(r'', text)


def delete_square_brackets(text):
    return text.replace('[', '').replace(']', '')


def tikers_to_str(tikers):
    res = ''
    for tiker in tikers:
        res += tiker[1:-1] + ' '
    # remove last space
    return res[:-1]


def find_tikers(text):
    reg_tikers = r'\[[A-Z]*\]'
    return re.findall(reg_tikers, text)


async def get_channel(client, channel_name):
    channel = await client.get_entity(channel_name)
    return channel


async def perform(api_id, api_hash):

    client = await TelegramClient('session1', api_id, api_hash).start()

    channel_name = 'https://t.me/AK47pfl'
    # channel = await get_channel(client, channel_name)

    with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile, open('old_data.csv', 'w', newline='', encoding='utf-8') as old_csvfile:
        datawriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

        old_datawriter = csv.writer(old_csvfile, quoting=csv.QUOTE_MINIMAL)
        old_datawriter.writerow(['date', 'content', 'tikers'])

        # write header
        datawriter.writerow(['date', 'content', 'tikers'])

        async for message in client.iter_messages(channel_name, limit=10000):
            print(message.id)

            old_datawriter.writerow([message.date, message.text])

            try:
                tikers_list = find_tikers(message.text)
            except:
                continue

            # exclude duplicates
            tikers_list = list(OrderedDict.fromkeys(tikers_list))

            if len(tikers_list) == 1:
                ftext = FormatText(message.text)

                datawriter.writerow(
                    [message.date, ftext.format_one_tiker(), tikers_to_str(tikers_list)])

            elif len(tikers_list) > 1:
                ftext = FormatText(message.text)
                sentences = ftext.format_many_tikers().split('\n')

                # Идет проверка по каждому предложению
                tikers_dict = {}

                for sentence in sentences:
                    for tiker in tikers_list:
                        if tiker in sentence:
                            tikers_dict[tiker] = sentence

                for tiker in tikers_list:
                    sentence = delete_tikers(tikers_dict[tiker])
                    datawriter.writerow(
                        [message.date, delete_square_brackets(sentence), tikers_to_str([tiker])])


def main():
    # Считываем учетные данные
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Присваиваем значения внутренним переменным
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']

    loop = asyncio.get_event_loop()
    loop.run_until_complete(perform(api_id, api_hash))


if __name__ == '__main__':
    main()
