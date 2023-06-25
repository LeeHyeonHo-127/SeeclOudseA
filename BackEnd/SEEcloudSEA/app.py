from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
import json
from datetime import datetime, timezone, timedelta
import joblib


# 스태킹 모델에 사용할 알고리즘 - KNN, 랜덤포레스트, AdaBoost, 의사결정나무, 로지스틱회귀
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello WORLD!"

@app.route("/model", methods = ['GET'])
def predict():
    if request.method == 'GET':
        # 개별 ML 모델 객체 생성 (기반모델)
        knn_clf = KNeighborsClassifier()
        rf_clf = RandomForestClassifier()
        dt_clf = DecisionTreeClassifier()
        ada_clf = AdaBoostClassifier()

        # 메타모델(스태킹으로 만들어진 데이터 학습 및 예측)
        lr_final = LogisticRegression(C=10)

        appid = "dd067a9aa888d5941ce0662190c0a2f4"
        geo = {"함양": [35.52, 127.75], "서울": [37.6387, 127.0370], "인제": [38.06, 128.17], "합천": [35.50, 128.16],
               "제천": [37.13, 128.19], "울산": [35.53, 129.31], "부산": [35.17, 129.07], "강진": [34.80, 126.69],
               "양평": [37.21, 127.18], "광주": [35.15, 126.85], "금산": [36.03, 127.48], "태백": [37.16, 128.98],
               "충주": [36.99, 127.92], "대구": [35.87, 128.60], "파주": [37.75, 126.78], "수원": [37.26, 127.02]}
        url = "http://api.openweathermap.org/data/2.5/forecast?lat=" + str(geo["서울"][0]) + "&lon=" + str(
            geo["서울"][1]) + "&appid=" + appid + "&units=metric"

        response = requests.get(url)
        json_data = response.json()
        s1 = json.dumps(json_data)
        json_object = json.loads(s1)
        forecast_list = json_object['list']

        days = []

        KST = timezone(timedelta(hours=9))
        now = datetime.now(KST)
        days.append(now.strftime('%Y-%m-%d'))
        for i in range(1, 5):
            day = now + timedelta(days=i)
            days.append(day.strftime('%Y-%m-%d'))
        midnight = "00:00:00"
        sunrise = "06:00:00"

        df = pd.DataFrame(index=[1])
        pre_temp = 0

        for forecast in forecast_list:

            # API 결과 값에서 나오는 시간은 UTC(영국) 기준이기 때문에 9시간을 더해줘야 함
            datetime_format = "%Y-%m-%d %H:%M:%S"
            datetime_string = forecast['dt_txt']
            datetime_result = datetime.strptime(datetime_string, datetime_format)
            datetime_result += timedelta(hours=9)
            day = datetime_result.strftime('%Y-%m-%d')
            dayTime = datetime_result.strftime('%H:%M:%S')

            if day == days[1]:  # 임시로
                if dayTime == midnight:
                    newColumns = ['Previous Temperature', 'Previous Precipitation', 'Previous Humidity',
                                  'Previous Pressure']
                    pre_temp = float(forecast['main']['temp'])
                    rain = 0
                    humidity = forecast['main']['humidity']
                    pressure = forecast['main']['pressure']
                    if forecast['weather'][0]['main'] == 'Rain':
                        rain = forecast['rain']['3h']
                    df[newColumns] = pd.Series([pre_temp, rain, humidity, pressure])
                    continue
                if dayTime == sunrise:
                    newColumns = ['Sunrise Temperature', 'Sunrise Wind Speed', 'Sunrise Humidity', 'Sunrise Pressure',
                                  'Sunrise Cloud Coverage', 'Diurnal Temperature Range']
                    temp = forecast['main']['temp']
                    wind = forecast['wind']['speed']
                    humidity = forecast['main']['humidity']
                    pressure = forecast['main']['pressure']
                    clouds = float(forecast['clouds']['all']) / 10
                    temp_range = float(temp) - pre_temp
                    df[newColumns] = pd.Series([temp, wind, humidity, pressure, clouds, temp_range])
                    continue

        knn_clf = joblib.load("/Users/ihyeonho/Desktop/workspace/flaskProjects/SEEcloudSEA/knn.pkl")
        rf_clf = joblib.load("/Users/ihyeonho/Desktop/workspace/flaskProjects/SEEcloudSEA/rf.pkl")
        dt_clf = joblib.load("/Users/ihyeonho/Desktop/workspace/flaskProjects/SEEcloudSEA/dt.pkl")
        ada_clf = joblib.load("/Users/ihyeonho/Desktop/workspace/flaskProjects/SEEcloudSEA/ada.pkl")
        lr_clf = joblib.load("/Users/ihyeonho/Desktop/workspace/flaskProjects/SEEcloudSEA/lr.pkl")
        xgbc_final = joblib.load("/Users/ihyeonho/Desktop/workspace/flaskProjects/SEEcloudSEA/xgbc.pkl")

        knn = knn_clf.predict(df)
        rf = rf_clf.predict(df)
        dt = dt_clf.predict(df)
        ada = ada_clf.predict(df)
        lr = lr_clf.predict(df)

        stacked = np.array([knn, rf, dt, ada, lr])
        stacked = np.transpose(stacked)

        final_pred = xgbc_final.predict(stacked)

        print(final_pred[0])
        predict_result = str(final_pred[0])

    return jsonify(predict_result), 200

