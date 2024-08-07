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
image_urls = []

# articles.json에서 링크를 읽어오기
with open('articles.json', 'r', encoding='utf-8') as f:
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

    # 이미지 추출
    image_elements = driver.find_elements(By.CSS_SELECTOR, '._LAZY_LOADING._LAZY_LOADING_INIT_HIDE')
    for img in image_elements:
        src = img.get_attribute('src')
        if src and src.startswith('http'):
            image_urls.append(src)

driver.quit()

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

print("기사 내용과 이미지 URL이 CSV 및 JSON 파일로 저장되었습니다.")
