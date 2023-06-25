# SeeclOudseA
북한산 운해 예측 프로젝트

# *프로젝트 목적*

<img width="375" alt="image" src="https://github.com/LeeHyeonHo-127/seaCloudSea/assets/84439622/6d4bcd74-bfda-4005-b7c1-d3ad41f84b26">

구름바다라 불리고 구름위에 솟은 산꼭대기가 바다에 떠있는 섬처럼 보이는 것을 의미하는 운해는 많은 등산객이 보길 원하는 풍경 중 하나이다. 그래서 운해 명소로 손꼽히는 장소에선 운해가 잘 보이는 일출 시간에 사람들이 몰리는 진풍경을 볼 수 있다. 이러한 운해는 특정한 계절과 시간, 그리고 기상 조건에서만 볼 수 있다. 보통 상공 2km 부근에 대기보다 지표면에 기온이 더 낮아 대류현상이 일어나지 않는) 역전층이 존재할 때 발생하는데 이른바 ‘운해 사냥’을 다니는 등산객들이 말하는 역전층이 있는 조건으론 다음이 있다.

- 일교차가 큰 계절(섭씨 10도 이상)
- 일출 시간
- 풍속 1-2m/s 이하
- 습도 90%이상
- 맑은 날씨

위 조건을 모두 만족하는 경우 높은 확률로 운해를 볼 수 있지만, 이는 경험에서 나온 정보로서 공식적인 기준이라고 부르기는 애매하다. 그래서 대표적인 등산 커뮤니티에서는 운해를 예상하고 갔지만 운해를 못 보고 이른바 ‘곰탕’만 보는 게시글을 간혹 볼 수 있다.

<img width="315" alt="image" src="https://github.com/LeeHyeonHo-127/seaCloudSea/assets/84439622/3412a912-7129-437c-84a9-eb98deb0327c">
<img width="175" alt="image" src="https://github.com/LeeHyeonHo-127/seaCloudSea/assets/84439622/2cfbf74b-1062-4e04-8ac0-64bf784e61bc">


이번 프로젝트에서 기상청에서 제공하는 기상관측자료를 통해 기상 정보를 불러오고 등산 카페 게시글을 크롤링해 운해 여부를 확인하며 운해의 더 정확한 조건을 파악 및 정의하고 사용자가 원하는 날짜에 운해를 볼 수 있는 확률을 제공하는데 목적을 둔다.

# **수집할 데이터 자료**

운해가 발생한 날. 발생하지 않은 날에 대한 기상정보 데이터를 사용해 분류모델을 학습시킨다.

훈련시킨 분류모델에 기상청에서 제공하는 기상 예측 데이터를 사용해 운해 발생 여부를 예측한다.

### **운해 발생 여부에 관한 날짜 데이터**

- 운해가 발생한 날의 날짜
- 운해가 발생하지 않은 날의 날짜

### **운해가 발생할 수 있는 기상 조건 데이터**

- 상공 2Km에 역전층이 발생 조건
    - 기압 데이터
    - 풍속 데이터
    - 습도 데이터
- 일교차 데이터
- 이슬점 데이터
- 날씨 데이터
- 대기 온도 데이터
- 

### **기상 예측 데이터**

- 상공 2Km에 역전층이 발생 예측
    - 기압 데이터
    - 풍속 데이터
    - 습도 데이터
- 일교차 데이터
- 이슬점 데이터
- 날씨 데이터
- 대기 온도 데이터

# **데이터 수집 방법**

### **3.1. 데이터 Collection**

1. **오픈 데이터셋을 통해서 수집한 데이터**

기상청 기상자료개발포털 오픈 데이터 셋에서 API를 통해 기상 데이터를 수집한다.

학습을 위한 날짜별 기상데이터와, 예측을 위한 기상데이터를 수집한다.

날짜별 기압, 풍속, 습도, 날씨, 기온 데이터 :

- > 기상청 지상 시간 자료 조회서비스 openAPI

날짜별 일교차 데이터:

- > 기상청 지상 일 자료 조회서비스 openAPI

기상 예측 데이터:

- > OpenWeather Hourly Forecast 4 days (기압 예측 데이터)

데이터는 Labeled Data로서 Labeling 작업은 필요없다

1. **데이터 크롤링을 통해 추출한 데이터**

“운해" 키워드로 웹 크롤링을 통해 네이버 등산카페 ‘고윈클럽’에서 운해 사진이 있는 게시물 URL과 날짜를 추출한다.

“일출" 키워드로 웹 크롤링을 통해 네이버 등산 카페 ‘고윈클럽'에서 일출 사진이 있는 게시물 URL과 날짜를 추출한다.

url과 날짜 추출 후 해당 게시물의 날짜가 유의미한 날짜 데이터인지를 파악 후 데이터를 수집한다.

**3.2. 데이터 Labeling**

데이터 라벨링은 in-house labeling 방법으로 팀 내에서 각 크롤링한 게시물의 사진의 운해 여부를 파악해 게시물의 날짜의 운해 여부를 라벨링한다.

분류는 운해有, 운해無 로 총 2 개 이다.

**3.3. 데이터 Validation**

****데이터는 기상청과 OpenWeather API 와 ‘고윈 클럽' 의 게시물을 데이터 수집 대상으로 하며 오픈 데이터셋을 이용할 때는 이용신청을 한다.

크롤링을 통해 수집한 데이터에 대해서는 원본 URL을 명시하는 페이지를 만들어 출처를 표기한다.

수집한 모든 데이터는 교육 목적의 프로젝트 진행에만 쓴다.

**3.4. 데이터 Verification**

운해 조건을 위한 기상데이터( 기압, 풍속, 습도, 온도, 날씨 )를 기상청 에서 API를 통해 수집한다.

각 데이터는 기상청에서 ASOS, AWS 를 통해 수집한 데이터이다.

팀 내에서 직접 수집한 운해 발생 날짜 데이터는 다음과 같은 기준으로 검증한다.

- 날짜 데이터는 일출 사진의 날짜 데이터이다.
- 클래스간 데이터 수는 1:1 비율로 맞춘다(추후 변경 가능)

**데이터 분석 방법**

**로지스틱 회귀 모델**

로지스틱 회귀 모델을 사용하여 카테고리를 분류한다. 로지스틱 회귀 모델은 입력 변수와 가중치의 선형 결합을 구한 후 로지스틱 함수를 적용하여 예측 값을 구한다.

해당 프로젝트에서는 300여개의 상대적으로 적은 데이터를 이용할 것이기 때문에 과적합을 방지할 수 있는 로지스틱 회귀 모델을 선택하였다. 해당 모델은 모델의 복잡도를 조절할 수 있어 과적합을 방지할 수 있다.

손실 함수는 일반적으로 이진 분류에서 사용하는 binary cross-entorpy 함수를 사용한다.

일반적으로 많이 사용되는 MSE의 경우 실제값 간의 차이를 제곱한 값의 평균을 구하는 손실 함수로서 이진 분류 에서는 잔차가 크더라도 높은 손실 값을 반환할 수 있다. 때문에 MSE가 아닌 Binary cross-entropy 함수를 사용한다.

추후 예측 정확도를 바탕으로 서포트 벡터 머신, 의사 결정 나무 모델과 비교하여 모델 교환 가능성이 있다.

**모델 적합**

X_data 에는 7개의 feature 데이터를, y_data에는 x_data의 날짜에 대해 운해가 있었는지 여부(True==1), (False==0) 에 대한 데이터를 가지고 있는다.

학습 데이터와 검증 데이터의 비율은 7:3으로 나누어 사용한다.

7개의 feature

- 기압
- 풍속
- 습도
- 일교차
- 이슬점
- 날씨
- 대기 온도

경사하강법을 사용하여 오차를 최소화하는 파라미터를 찾아서 분류의 정확도를 높인다.

**예측**

기상청에서 제공하는 기상 데이터를 사용하여 해당 날짜에 운해 여부를 예측한다.

**예상 결과**

openWeatherApi를 통해 예보를 제공하는 기간의 날짜를 선택할 경우 해당 기간의 운해 확률을 제공한다. 운해 확률이 80% 이상일 경우 운해 사냥을 권하는 문구를 출력하고 80% 미만인 경우 운해를 보지 못할 확률이 높다는 문구를 출력하게 된다. 이러한 문구는 Django 프레임워크를 이용해 웹 서비스로 제공하며 날짜와 지역을 선택하면 해당 지역의 운해 확률을 제공한다. 이에 대한 대략적인 UI는 아래와 같다.

우리나라 연간 국립공원 탐방객 수는 약 3500만명에 달하고 우리나라 국민들이 가장 좋아하는 운동으로 등산을 선택할 만큼 등산은 꾸준하게 인기를 끌고 있는 스포츠다. 이에 아웃도어 브랜드의 매출은 꾸준히 성장하고 있고 알레, 디그디그 액티비티, 산타 등 다양한 아웃도어 관련 서비스가 출시되고 성장하고 있다.

이러한 상황에서 운해 예측 서비스를 제작해 제공한다면 고정된 사용자층을 확보할 수 있을 뿐만 아니라 신규 사용자 유입도 꾸준히 일으키는 안정된 수입을 가지는 서비스를 운영할 수 있다.

