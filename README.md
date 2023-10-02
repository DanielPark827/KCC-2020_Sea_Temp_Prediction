# 저주파 통과 필터를 이용한 수온 예측과 K-평균 알고리즘을 활용한 수온 오측치 추정

+ 본 프로젝트는 논문으로 작성되어 신호처리학술대회 2020에 게재되었습니다.
+ 학습 데이터를 통해 미래의 수온을 예측하는 Time Series forecasting task.

### 💻 Technology
+ Pytorch <a href="" target="_blank"><img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=PyTorch&logoColor=white"/></a>

### Problem
+ 수온 데이터 취득 과정에서 기기 상의 문제로 인해 오측치(Anomaly data)가 발생하여 모델의 정확한 학습을 방해함.

### In this study
+ Low-pass filter로 노이즈에 해당하는 고주파 성분을 걸러내고, K-means 알고리즘을 통해 오측치를 제거한 후 전처리된 데이터를 모델에 학습시킴


