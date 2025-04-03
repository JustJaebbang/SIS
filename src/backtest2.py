# 라이브러리 불러오기
import pandas as pd

# 백테스팅 함수 정의
def backtest3(data, initial_balance=100000, fee_rate=0.001):
    """
    주어진 데이터와 투자 전략을 기반으로 백테스팅 실행
    - data: Pandas DataFrame (필수 열: 'Close', 'Signal')
    - initial_balance: 초기 자본 (기본값: 100,000 원)
    - fee_rate: 매매 수수료 비율 (기본값: 0.1%)
    """

    # 초기 변수 설정
    balance = initial_balance  # 초기 현금 잔고
    shares = 0  # 초기 주식 보유 수 (항상 0으로 초기화)
    portfolio_values = []  # 각 시점에서의 포트폴리오 가치를 기록

    # Null 값 제거 (Close와 Signal에 NaN이 없는지 확인)
    data = data.dropna(subset=['Close', 'Signal'])

    # 백테스팅 실행 루프
    for i in range(len(data)):
        current_close = data['Close'].iloc[i]  # 현재 종가
        current_signal = data['Signal'].iloc[i]  # 현재 매수/매도 신호

        # 매수 조건: Signal이 1로 변하고 주식이 없는 경우
        if current_signal == 1 and shares == 0:
            shares = balance / current_close  # 전액 주식 매수
            balance = balance * (1 - fee_rate)  # 수수료 차감

        # 매도 조건: Signal이 -1로 변하고 주식이 있는 경우
        elif current_signal == -1 and shares > 0:
            balance += shares * current_close * (1 - fee_rate)  # 전량 매도 후 현금화
            shares = 0  # 주식 보유 개수 초기화

        # 현재 포트폴리오 가치 계산
        portfolio_value = balance + (shares * current_close if shares > 0 else 0)
        portfolio_values.append(portfolio_value)  # 포트폴리오 가치를 기록

    # 최종 결과 계산
    final_portfolio_value = portfolio_values[-1] if portfolio_values else initial_balance
    roi = (final_portfolio_value - initial_balance) / initial_balance * 100  # 총 수익률

    # 결과 반환: 최종 가치, ROI, 포트폴리오 가치 기록 추가 데이터프레임
    data['Portfolio Value'] = portfolio_values
    return final_portfolio_value, roi, data

