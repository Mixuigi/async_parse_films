import asyncio
import httpx

from bs4 import BeautifulSoup

URL = 'https://torrentskino.info/filmy/page/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}


async def get_films(current_page):
    async with httpx.AsyncClient() as client:
        html = await client.get(URL + str(current_page) + '/', headers=HEADERS)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            tags = soup.find_all('h2', class_='zagolovki')
            for tag in tags:
                print(tag.find('a').get_text(strip=True), tag.find('a').get('href'))
        else:
            print('error')


async def main():
    page_count = int(input('Введите количество страниц: '))
    current_page = 0
    task_list = []

    while current_page < page_count:
        current_page += 1
        task = asyncio.create_task(get_films(current_page))
        task_list.append(task)
    await asyncio.gather(*task_list, return_exceptions=True)
    print('done!')


asyncio.run(main())
