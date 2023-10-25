import time
import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

BASE_URL = "https://movie.douban.com/top250"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Cookie": 'll="108288"; bid=xzmUtmcx194; douban-fav-remind=1; dbcl2="275441449:okJOkxtmNNg"; push_noty_num=0; push_doumail_num=0; __utma=30149280.1921362768.1698071996.1698131979.1698141127.3; __utmb=30149280.0.10.1698141127; __utmc=30149280; __utmz=30149280.1698141127.3.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; frodotk_db="45fff8bb15ea2796d1ffea3141be76c2"; ck=hxPY'
}
def get_movie_links_and_titles():
    """获取所有电影的链接和中文名字"""
    movie_links = []
    movie_titles = []
    for start in range(0, 250, 25):
        url = f"{BASE_URL}?start={start}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.select('div.hd a')]
        titles = [div.select_one('span.title').text for div in soup.select('div.hd')]
        movie_links.extend(links)
        movie_titles.extend(titles)
        time.sleep(2)
    return movie_links, movie_titles


def get_movie_details(url, title):
    """获取单个电影的详细信息"""
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    date_element = soup.select_one('span[property="v:initialReleaseDate"]')
    date = date_element.text if date_element else "Unknown Date"
    date = date.split('(')[0].strip()

    director_element = soup.select_one('a[rel="v:directedBy"]')
    director = director_element.text if director_element else "Unknown Director"

    actors = [actor.text for actor in soup.select('a[rel="v:starring"]')]
    genre = [g.text for g in soup.select('span[property="v:genre"]') if g]

    # 首先尝试从 span[property="v:summary"] 中提取
    summary_element = soup.select_one('span[property="v:summary"]')
    # 如果没有找到，则尝试从 span.all.hidden 中提取
    if not summary_element:
        summary_element = soup.select_one('span.all.hidden')
    # 提取文本并清理
    summary = summary_element.text.strip() if summary_element else "Unknown Summary"
    summary = summary.replace('\n', '').replace('\r', '').replace('　', '').strip()  # 将剧情简介转换为一行并移除全角空格

    details = [
        (title, "上映时间", date),
        (title, "导演", director)
    ]
    for actor in actors:
        details.append((title, "主演", actor))
    for g in genre:
        details.append((title, "类型", g))
    details.append((title, "剧情简介", summary))

    return details


def main():
    movie_links, movie_titles = get_movie_links_and_titles()
    with open('douban_topmovies.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for link, title in tqdm(zip(movie_links, movie_titles), total=len(movie_links), desc="Fetching movie details"):
            details = get_movie_details(link, title)
            writer.writerows(details)


if __name__ == "__main__":
    main()
