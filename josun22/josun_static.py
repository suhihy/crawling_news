import requests
import json
import csv

base_url = 'https://media.naver.com/j/moreArticles/926cd70a-5f0b-4f5e-82a2-9f3a3c4bded1?cursor=77106054&offset='

all_articles = []
offset = 0
target_date = "2024.01.01."
target_reached = False

while not target_reached:
    url = base_url + str(offset)
    res = requests.get(url)
    
    if res.status_code != 200:
        print(f"Failed to retrieve data: {res.status_code}")
        break

    data = res.json()
    
    if 'result' not in data or not data['result']:
        print("No articles found.")
        break

    articles = data['result']

    for article in articles:
        title = article.get('title')
        link_url = article.get('linkUrl')
        service_time = article.get('serviceTimeForCardList')
        
        if title and link_url and service_time:
            article_info = {
                'title': title,
                'linkUrl': link_url,
                'serviceTimeForCardList': service_time
            }
            all_articles.append(article_info)
            
            if service_time == target_date:
                target_reached = True
                break
    
    offset += 1

# 수집한 모든 기사 정보를 JSON 형식으로 저장
json_path = 'articles.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)

print('기사 정보가 articles.json 파일에 저장되었습니다.')

# 수집한 모든 기사 정보를 CSV 형식으로 저장
csv_path = 'articles.csv'
with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['title', 'linkUrl', 'serviceTimeForCardList'])  # CSV 파일 헤더
    for article in all_articles:
        writer.writerow([article['title'], article['linkUrl'], article['serviceTimeForCardList']])

print('기사 정보가 articles.csv 파일에 저장되었습니다.')