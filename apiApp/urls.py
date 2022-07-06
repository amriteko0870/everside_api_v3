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
    path('totalComments',views.totalComments,name='totalComments'),
    path('positiveComments',views.positiveComments,name='positiveComments'),
    path('negativeComments',views.negativeComments,name='negativeComments'),
    path('neutralComments',views.neutralComments,name='neutralComments'),
    path('extremeComments',views.extremeComments,name='extremeComments'),
    path('alertComments',views.alertComments,name='alertComments'),
    path('npsOverTime',views.npsOverTime,name='npsOverTime'),
    path('nssOverTime',views.nssOverTime,name='nssOverTime'),
    path('npsVsSentiments',views.npsVsSentiments,name='npsVsSentiments'),
    path('providersData',views.providersData,name='providersData'),
    path('clinicData',views.clinicData,name='clinicData'),
    path('clientData',views.clientData,name='clientData'),
 
    
    #------------------Engagement------------------------------
    path('egMemberPercentile',views.egMemberPercentile,name='egMemberPercentile'),
    path('fileDownload',views.fileDownload,name='fileDownload'),


    #------------------ Download files -----------------------------
    path('averageTableDownload',views.averageTableDownload,name='averageTableDownload'),
    path('totalCommentsDownload',views.totalCommentsDownload,name='totalCommentsDownload'),
    path('alertCommentsDownload',views.alertCommentsDownload,name='alertCommentsDownload'),
    
    #------------------ Files Delete -------------------------------------
    path('logout',views.logout,name='logout'),
    

    #------------------- Users ----------------------------------------------
    path('resetPassword',views.resetPassword,name='resetPassword'),
    path('createUser',views.createUser,name='createUser'),
    path('userList',views.userList,name='userList'),
    path('deleteUser',views.deleteUser,name='deleteUser'),


    
    

    
    


    path('',views.index,name='index'),   
]