import requests
import os
import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# 현재 폴더와 chromedriver 경로 설정
current_folder = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(current_folder, 'chromedriver.exe')

service = Service(driver_path)
driver = webdriver.Chrome(service=service)

URL = 'https://media.naver.com/journalist/020/78665'

driver.get(URL)
time.sleep(1)


# 발행 날짜 저장할 리스트
publish_dates = []
titles = []
contents = []
image_urls = []

# 각 기사 링크 클릭하고 발행 날짜 추출
for i in range(10):  # 최대 10개 기사로 제한
    news_links = driver.find_elements(By.CSS_SELECTOR, 'li.press_edit_news_item')

    news_links[i].click()
    time.sleep(1) 

    date_info = driver.find_element(By.CSS_SELECTOR, 'span.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME')
    print(date_info.text)
    if date_info:
        publish_dates.append(date_info.text.strip())

    title_info = driver.find_element(By.CSS_SELECTOR, '.media_end_head_title')
    print(title_info.text)
    if title_info:
        titles.append(title_info.text.strip())

    content_info = driver.find_element(By.CSS_SELECTOR, '.go_trans._article_content')
    print(content_info.text)
    if content_info:
        contents.append(content_info.text.strip())

    #이미지 추출
    try:
        # 이미지 URL 추출
        images = driver.find_elements(By.CSS_SELECTOR, '._LAZY_LOADING._LAZY_LOADING_INIT_HIDE')
        for img in images:
            src = img.get_attribute('src')
            if src and src.startswith('http'):
                image_urls.append(src)
    except Exception as e:
        print(f"이미지 URL을 찾을 수 없습니다: {e}")


    # 이전 페이지로 돌아가기
    driver.back()
    time.sleep(1)  # 페이지 로드 대기

# 브라우저 닫기
driver.quit()

# 발행날짜 CSV 파일로 저장
csv_path = 'publish_dates.csv'
with open('publish_dates.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['publish_date'])
    for date in publish_dates:
        writer.writerow([date])

# 발행날짜 JSON 파일로 저장
json_path = 'publish_dates.json'
with open('publish_dates.json', mode='w', encoding='utf-8') as file:
    json.dump({'publish_dates': publish_dates}, file, ensure_ascii=False, indent=4)


# 기사제목 CSV 파일로 저장
csv_path_titles = 'titles.csv'
with open(csv_path_titles, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['title'])
    for title in titles:
        writer.writerow([title])

# 기사 제목 JSON 파일로 저장
json_path_titles = 'titles.json'
with open(json_path_titles, mode='w', encoding='utf-8') as file:
    json.dump({'titles': titles}, file, ensure_ascii=False, indent=4)

# 기사 내용 CSV 파일로 저장
csv_path_contents = 'contents.csv'
with open(csv_path_contents, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['content'])
    for content in contents:
        writer.writerow([content])

# 기사 내용 JSON 파일로 저장
json_path_contents = 'contents.json'
with open(json_path_contents, mode='w', encoding='utf-8') as file:
    json.dump({'contents': contents}, file, ensure_ascii=False, indent=4)

# 이미지 URL CSV 파일로 저장
csv_path_images = 'image_urls.csv'
with open(csv_path_images, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['image_url'])
    for img_url in image_urls:
        writer.writerow([img_url])

# 이미지 URL JSON 파일로 저장
json_path_images = 'image_urls.json'
with open(json_path_images, mode='w', encoding='utf-8') as file:
    json.dump({'image_urls': image_urls}, file, ensure_ascii=False, indent=4)


print("CSV와 JSON 파일로 저장되었습니다.")
