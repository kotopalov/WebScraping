from lxml import html
import requests
import time
from fake_headers import Headers


header = Headers(headers=True).generate()
info = []


def get_mail_ru_news(info):
    url = 'https://news.mail.ru/society/'

    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)

    # to_search = "/html/body/div[6]"
    to_search = "/html/body/div[7]/div[2]/div[3]/div/div/div/div/div/div[3]/div/div[1]"
    page = root.xpath(to_search)

    link_format = '//*[@class="newsitem__title link-holder"]/@href'
    text_format = '//*[@class="newsitem__title-inner"]/text()'
    time_filter = '//*[@class="newsitem__param js-ago"]/@datetime'


    for el in page:
        links = [ul for ul in el.xpath(link_format)]
        texts = [ul for ul in el.xpath(text_format)]
        times = [ul for ul in el.xpath(time_filter)]

        for i, lnk in enumerate(times):
            info.append({'src': 'mail.ru',
                         'text': texts[i],
                         'link': links[i],
                         'time': lnk})

    return info


def get_lenta_ru_news(info):
    url = 'https://lenta.ru/'

    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)


    # to_search = "/html/body/div[3]/section[2]/div/div/div[1]/div[4]"
    to_search = "/html/body/div[3]/section[2]"
    page = root.xpath(to_search)

    link_format = '//*[@class="titles"]/@href'
    text_format = '//*[@class="card-title"]/text()'
    time_filter = '//*[@class="time"]/text()'
    for el in page:
        links = [ul for ul in el.xpath(link_format)]
        texts = [ul for ul in el.xpath(text_format)]
        times = [ul for ul in el.xpath(time_filter)]

        for i, lnk in enumerate(times):
            info.append({'src': 'lenta.ru',
                         'text': texts[i],
                         'link': links[i],
                         'time': lnk})

    return info


def get_yandex_news(info):
    url = 'https://yandex.com/news'

    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)

    # mg - grid__row
    # mg-grid__row_gap_8
    # mg - top - rubric - flexible - stories
    # news - app__top


    # to_search = "/html/body/div[6]"
    to_search = "/html/body/div[3]/div/div[2]/div/div[1]"
    page = root.xpath(to_search)

    link_format = '//*[@class="mg-card__link"]/@href'
    text_format = '//*[@class="mg-card__annotation"]/text()'
    time_filter = '//*[@class="mg-card-source__time"]/text()'
    src_filter = '//*[@class="mg-card__source-link"]/text()'

    for el in page:
        links = [ul for ul in el.xpath(link_format)]
        texts = [ul for ul in el.xpath(text_format)]
        times = [ul for ul in el.xpath(time_filter)]
        srcs = [ul for ul in el.xpath(src_filter)]

        for i, lnk in enumerate(times):
            info.append({'src': srcs[i],
                         'text': texts[i],
                         'link': links[i],
                         'time': lnk})

    return info


# info = get_mail_ru_news(info)
# info = get_lenta_ru_news(info)
info = get_yandex_news(info)
print(info)
