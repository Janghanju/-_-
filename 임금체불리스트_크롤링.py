import requests
from bs4 import BeautifulSoup
import pandas as pd

# 베이스 URL
base_url = "https://www.moel.go.kr/info/defaulter/defaulterList.do?pageIndex={}"
pages = range(1, 85)  # 1부터 84까지의 페이지
data = []

# 각 페이지 데이터 가져오기
for page in pages:
    url = base_url.format(page)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 테이블 데이터 추출 (HTML 구조에 따라 수정 필요)
        table = soup.find('table')  # table 태그 확인
        if table:
            rows = table.find_all('tr')  # 각 행
            for row in rows:
                cols = row.find_all('td')  # 각 열
                cols = [col.text.strip() for col in cols]
                if cols:  # 데이터가 있는 행만 추가
                    data.append(cols)
    else:
        print(f"페이지 {page}를 가져오지 못했습니다.")

# DataFrame 생성 및 Excel 저장
if data:
    df = pd.DataFrame(data)
    df.to_excel('defaulter_data.xlsx', index=False, header=False)
    print("데이터를 Excel 파일로 저장했습니다.")
else:
    print("추출된 데이터가 없습니다.")
