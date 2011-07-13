from django.conf import settings
from vendors.models import MarketSeason

def get_google_api_key(request):
    if settings.GOOGLE_API_KEY:
        return {'google_api_key': settings.GOOGLE_API_KEY}
    else:
        return {}

def get_current_market_season(request):
    try:
        season=MarketSeason.objects.get(active=True)
    except:
        season=None 
    return {'current_season': season}
