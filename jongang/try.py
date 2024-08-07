import os
import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 현재 폴더와 chromedriver 경로 설정
current_folder = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(current_folder, 'chromedriver.exe')

# Chrome 드라이버 설정
options = Options()
options.add_argument("--start-maximized")
options.page_load_strategy = 'eager'  # 페이지 로드 전략 설정 (eager)
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

contents = []
publish_dates = []

# 중앙articles.json에서 링크를 읽어오기
with open('jongang_articles.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    link_urls = [article['linkUrl'] for article in data]

# 페이지 로드 대기 및 콘텐츠 추출
for link_url in link_urls:
    driver.get(link_url)
    
    # 내용 추출
    content_found = False
    for _ in range(10):  # 최대 10번 시도
        content_elements = driver.find_elements(By.CSS_SELECTOR, '.go_trans._article_content')
        if content_elements:
            contents.append(content_elements[0].text.strip())
            content_found = True
            break
        time.sleep(1)  # 1초 대기 후 다시 시도
    
    if not content_found:
        contents.append('')  # 내용을 찾지 못한 경우 빈 문자열 추가

    # 발행 날짜 추출
    date_found = False
    for _ in range(10):  # 최대 10번 시도
        date_elements = driver.find_elements(By.CSS_SELECTOR, 'span.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME')
        if date_elements:
            publish_dates.append(date_elements[0].text.strip())
            date_found = True
            break
        time.sleep(1)  # 1초 대기 후 다시 시도
    
    if not date_found:
        publish_dates.append('')

driver.quit()

# 기사 내용과 발행 날짜를 합쳐서 CSV 파일로 저장
csv_path = 'jongang_articles2.csv'
with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['content', 'publish_date'])
    for content, date in zip(contents, publish_dates):
        writer.writerow([content, date])

# 기사 내용과 발행 날짜를 합쳐서 JSON 파일로 저장
json_path = 'jongang_articles2.json'
with open(json_path, mode='w', encoding='utf-8') as file:
    articles = [{'content': content, 'publish_date': date} for content, date in zip(contents, publish_dates)]
    json.dump({'articles': articles}, file, ensure_ascii=False, indent=4)

print("기사 내용과 발행 날짜 및 시간이 CSV와 JSON 파일로 저장되었습니다.")
