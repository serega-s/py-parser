import json

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}

REQUEST_URL = 'https://www.techcult.ru/'
ARTICLE_URLS_FILE = 'articles_urls.txt'


def get_articles_url(url):
    with requests.Session() as session:
        response = session.get(url=url, headers=HEADERS)

    soup = BeautifulSoup(response.text, 'lxml')
    pagination_count = int(soup.find('tr').find_all('a')[-2].text)

    articles_urls_list = []

    for page in range(1, pagination_count + 1):
        response = session.get(f'{REQUEST_URL}/page/{page}/', headers=HEADERS)
        soup = BeautifulSoup(response.text, 'lxml')

        articles_urls = soup.find(
            'div', class_='pads').find_all('a', class_='pad')

        for au in articles_urls:
            article_url = au.get('href')
            articles_urls_list.append(article_url)

        # time.sleep(randrange(2, 5))
        print(f'Proccessing {page}/{pagination_count}')

    with open(ARTICLE_URLS_FILE, 'w', encoding='utf8') as file:
        for url in articles_urls_list:
            file.write(f'{url}\n')

    return 'Data collection has been successfully done!'


def get_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        urls_list = [line.strip() for line in file.readlines()]

    urls_count = len(urls_list)
    result_data = []

    with requests.Session() as session:
        for i, url in enumerate(urls_list[:100]):
            response = session.get(url=url, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'lxml')

            article_title = soup.find('div', class_='title').find(
                'h1', class_='big').text.strip()
            article_date = soup.find(
                'div', class_='left_sign').find('meta')['content']
            article_img = f"{REQUEST_URL}{soup.find('div', class_='img_cont').find('img').get('src')}"
            article_desc = soup.find(
                'div', class_="text").find('div').find('p').text.strip()
            article_text = [
                at.text.replace('\n', '').replace('\r', '') for at in soup.find(
                    'div', class_="text").find_all('p')
            ]

            result_data.append(
                {
                    'original_url': url,
                    'article_title': article_title,
                    'article_desc': article_desc,
                    'article_text': article_text,
                    'article_date': article_date,
                    'article_img': article_img,
                }
            )

            print(f'Finished {i + 1}/{urls_count}')

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    # print(get_articles_url(REQUEST_URL))
    get_data(ARTICLE_URLS_FILE)


if __name__ == '__main__':
    main()
