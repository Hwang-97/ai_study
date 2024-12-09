# from django.shortcuts import render_to_response, render
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.template import RequestContext
from apps.core.models import Stock
from .utils import get_news_api

def page_not_found_page(request):
    # response = render_to_response('myapp/404.html', {}, context_instance=RequestContext(request))
    # response.status_code = 404
    # return response
    return render(request, "404.html", status=404)


def get_test(request):
    html = f"""<h1>Hello~</h1>
    <div>{request.GET.get('str')}</div>"""
    return HttpResponse(html)


def get_stock_data(request):
    stocks = Stock.objects.all().values(
        "company_name", "ticker_symbol", "market_price", "market_cap"
    )
    stock_list = list(stocks)
    return JsonResponse({"stocks": stock_list})


def add_stock(request):
    if request.method == "POST":
        company_name = request.POST.get("company_name")
        ticker_symbol = request.POST.get("ticker_symbol")
        market_price = request.POST.get("market_price")
        market_cap = request.POST.get("market_cap")

        stock = Stock.objects.create(
            company_name=company_name,
            ticker_symbol=ticker_symbol,
            market_price=market_price,
            market_cap=market_cap,
        )
        return JsonResponse(
            {"message": "Stock added successfully", "stock_id": stock.id}
        )
    
def chat_page(request):
    return render(request, 'chat.html')

def get_news(request):
    """기업 이름을 받아서 뉴스 기사를 가져옵니다."""
    company_name = request.GET.get("company_name")
    
    if not company_name:
        return JsonResponse({"error": "기업 이름을 작성해주세요."}, status=400)
    
    try:
        articles = get_news_api(company_name)
        return JsonResponse({"company_name": company_name, "articles": articles}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
