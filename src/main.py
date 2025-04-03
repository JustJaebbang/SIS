import yfinance as yf # Yahoo Finance 데이터 사용
import pandas as pd
from backtest2 import backtest3

# 삼성전자 주식 데이터 가져오기 (KS:005930.KS for South Korea stock)
ticker = "005930.KS"
data = yf.download(ticker, start="2023-01-01", end="2024-01-01")

# 이동 평균 계산 (50일, 200일)
data['SMA50'] = data['Close'].rolling(window=50).mean()
data['SMA200'] = data['Close'].rolling(window=200).mean()

# 간단한 매수/매도 조건
data['Signal'] = 0
data.loc[data['SMA50'] > data['SMA200'], 'Signal'] = 1 # 매수 신호
data.loc[data['SMA50'] <= data['SMA200'], 'Signal'] = -1 # 매도 신호

# 결과 출력
print(data[['Close', 'SMA50', 'SMA200', 'Signal']])

# 결과와 백테스트 동시 실행
print(backtest3(data))