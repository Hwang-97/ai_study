from myapp.models import Stock

def run():
    stock1 = Stock.objects.create(
        company_name="Apple Inc.",
        ticker_symbol="AAPL",
        market_price=170.20,
        market_cap=2800000000000
    )

    stock2 = Stock.objects.create(
        company_name="Tesla, Inc.",
        ticker_symbol="TSLA",
        market_price=250.75,
        market_cap=750000000000
    )

    print(stock1)
    print(stock2)
