# 라이브러리 불러오기
import pandas as pd

# 백테스팅 함수 정의
def backtest(data, initial_balance=1000000, fee_rate=0.001):
    """
    주어진 데이터와 투자 전략을 기반으로 백테스팅 실행
    - data: Pandas DataFrame (필수 열: 'Close', 'Signal')
    - initial_balance: 초기 자본 (기본값: 100,000 원)
    - fee_rate: 매매 수수료 비율 (기본값: 0.1%)
    """
    balance = initial_balance  # 초기 현금 잔고
    shares = 0  # 초기 주식 보유 수
    portfolio_values = []  # 각 시점에서의 포트폴리오 전체 가치 기록

    # 백테스팅 실행
    for i in range(len(data)):
        current_close = data['Close'].iloc[i]  # 현재 종가
        current_signal = data['Signal'].iloc[i]  # 현재 매수/매도 신호

        # 매수 조건: Signal이 1로 변하고 현재 주식이 없는 경우
        if current_signal == 1 and shares == 0:
            shares = balance / current_close  # 전액 주식 매수
            balance = balance * (1 - fee_rate)  # 수수료 차감

        # 매도 조건: Signal이 -1로 변하고 현재 주식이 있는 경우
        elif current_signal == -1 and shares > 0:
            balance += shares * current_close * (1 - fee_rate)  # 전량 매도 후 현금화
            shares = 0  # 주식 보유 개수 초기화

        # 현재 포트폴리오 가치 계산: (현금 + 보유 주식 평가 금액)
        portfolio_value = balance + (shares * current_close) #if shares > 0 else balance
        portfolio_values.append(portfolio_value)

    # 최종 결과 계산
    final_portfolio_value = portfolio_values[-1]
    roi = (final_portfolio_value - initial_balance) / initial_balance * 100  # ROI (%)

    # 포트폴리오와 백테스트 결과 반환
    data['Portfolio Value'] = portfolio_values
    return final_portfolio_value, roi, data

# 사용 예시 (데이터프레임 입력 방식)
# 'data'는 필수로 'Close'와 'Signal' 컬럼이 있어야 합니다.
# backtest_strategy(data)