import requests
from django.conf import settings
from datetime import datetime, timedelta
from newsapi import NewsApiClient

def get_news_api(company_name):
    news_articles = []
    # 오늘 날짜와 7일 전 날짜 계산
    today = datetime.today().strftime('%Y-%m-%d')
    seven_days_ago = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    # NewsAPI 호출
    try:
        newsapi = NewsApiClient(api_key=settings.NEWSAPI_KEY)
        # /v2/everything
        all_articles = newsapi.get_everything(q=company_name,
                                            # sources='bbc-news,the-verge',
                                            # domains='bbc.co.uk,techcrunch.com',
                                            from_param=seven_days_ago,
                                            to=today,
                                            # language='en',
                                            sort_by='popularity',)

        if all_articles.get('status') == 'ok':
            articles = all_articles.get('articles')
            if len(articles) > 0:
                news_articles.extend(articles)
            if len(news_articles) >= 10:
                return news_articles
        else:
            raise Exception("NewsAPI에서 데이터를 가져오는 데 실패했습니다.")
    except Exception as e:
        print(f"NewsAPI 호출 오류: {e}")
    
    # NewsAPI에서 결과가 부족하면 ThenNewsAPI 호출
    try:
        thenewsapi_url = f'https://api.thenewsapi.com/v1/news/top?api_token={settings.THENEWSAPI_KEY}&language=en&published_before={today}&published_after={seven_days_ago}&search={company_name}&sort=published_on&limit=10'
        response = requests.get(thenewsapi_url)
        if response.status_code == 200:
            articles = response.json().get('data', [])
            if len(articles) > 0:
                news_articles.extend(articles)
            if len(news_articles) >= 1:
                return news_articles[:10]
        else:
            raise Exception("ThenNewsAPI에서 데이터를 가져오는 데 실패했습니다.")
    except Exception as e:
        print(f"ThenNewsAPI 호출 오류: {e}")
    
    # 만약 두 API에서 모두 데이터를 가져올 수 없거나, 기사가 하나도 없다면 오류를 던짐
    if not news_articles:
        raise Exception(f"{company_name}에 대한 기사를 찾을 수 없습니다. 두 API 모두에서 실패했습니다.")
    
    return news_articles[:10]  # 최대 10개의 기사 반환
