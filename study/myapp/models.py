from django.db import models

class Stock(models.Model):
    company_name = models.CharField(max_length=100)  # 회사 이름
    ticker_symbol = models.CharField(max_length=10, unique=True)  # 티커 심볼
    market_price = models.DecimalField(max_digits=10, decimal_places=2)  # 주식 가격
    market_cap = models.BigIntegerField()  # 시가 총액
    created_at = models.DateTimeField(auto_now_add=True)  # 데이터 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 데이터 수정 시간

    def __str__(self):
        return f"{self.company_name} ({self.ticker_symbol})"