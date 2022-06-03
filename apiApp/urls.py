from unicodedata import name
from django.urls import path,include
from . import views


urlpatterns = [
    path('filterRegion',views.filterRegion,name='filterRegion'),
    path('filterClinic',views.filterClinic,name='filterClinic'),
    path('userLogin',views.userLogin,name='userLogin'),
    path('netPromoterScore',views.netPromoterScore,name='netPromoterScore'),
    path('netSentimentScore',views.netSentimentScore,name='netSentimentScore'),
    path('totalCards',views.totalCards,name='totalCards'),
    path('groupcheck',views.groupcheck,name='groupcheck'),
    path('npsOverTime',views.npscheck,name='npscheck'),
    path('totalComments',views.totalComments,name='totalComments'),
    path('alertComments',views.alertComments,name='alertComments')




]