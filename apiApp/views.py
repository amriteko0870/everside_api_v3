from genericpath import getsize
from pyexpat import model
import numpy as np
import pandas as pd
import time
from datetime import datetime as dt
import datetime
import re
from operator import itemgetter 
import os
#-------------------------Django Modules---------------------------------------------
from django.http import HttpResponse, JsonResponse,FileResponse
from django.shortcuts import render
from django.db.models import Avg,Count,Case, When, IntegerField,Sum,FloatField,CharField
from django.db.models import F,Func
from django.db.models import Value as V
from django.db.models.functions import Concat,Cast,Substr
from django.contrib.auth.hashers import make_password,check_password
#----------------------------restAPI--------------------------------------------------
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser,FormParser
#--------------------------Models-----------------------------------------------------
from apiApp.models import engagement_file_data, everside_nps, user_data
#--------------------------extra libs------------------------------------------------
from apiApp.extra_vars import region_names,prob_func
# Create your views here.
#-------------- Global Variable--------------------------------------------------------
timestamp_sub = 86400 +19800
timestamp_start = 0+19800
#----------------------------Annotation Functions--------------------------------------
class roundRating(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 1)'
class twoDecimal(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'
class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 0)'
#--------------------------- Filters---------------------------------------------------
@api_view(['POST'])
def filterRegion(request,format=None):
    try:
        if request.method == 'POST':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            check_token = user_data.objects.get(USERNAME = (request.data)['username'])
            if(check_token.TOKEN != (request.headers)['Authorization']):
                return Response({'Message':'FALSE'})
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub         
            obj = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).exclude(CLINIC_STATE__isnull=True).exclude(CLINIC_STATE__exact='nan').values_list('REGION',flat=True).distinct()
            region = list(obj)
            region.sort()
        return Response({'Message':'TRUE','region':region})
    except:
        return Response({'Message':'FALSE'})

@api_view(['POST'])
def filterClinic(request,format=None):
    try:
        if request.method == 'POST':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = request.GET.get('region')
            region = re.split(r"-|,", region)
            check_token = user_data.objects.get(USERNAME = (request.data)['username'])
            if(check_token.TOKEN != (request.headers)['Authorization']):
                return Response({'Message':'FALSE'})
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub  
            obj = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values_list('NPSCLINIC',flat=True).distinct()    
            if '' not in region:
                obj = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).filter(REGION__in=region).values_list('NPSCLINIC',flat=True).distinct()
            data = list(obj)
            data.sort()
        return Response({'Message':'TRUE','clinic':data,})
    except:
        return Response({'Message':'FALSE'})  

#-------------------- for Login -----------------------------------------------------
@api_view(['POST'])
def userLogin(request,format=None):
    if request.method == 'POST':
        try:
            data = request.data
            username = str(data['username'])
            password = str(data['password'])
            data = user_data.objects.filter(USERNAME = username).values()
            if (check_password(password,data[0]['PASSWORD'])):
                token = data[0]['TOKEN']
                u_name = data[0]['USERNAME']
                return Response({'Message':'TRUE','username':u_name,'token':token})
        except:
                return Response({'Message':'FALSE'})

           
            
#---------------------For Dashboards--------------------------------------------------
@api_view(['POST'])
def netPromoterScore(request,format=None):
    try:
        if request.method == 'POST':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            # print('###################################################################################')
            # print((request.data)['username'],(request.headers)['Authorization'])
            # print('###################################################################################')

            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                print((request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})
            except:
                return Response({'Message':'FALSE'})

            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)       
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub
            total_count = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()
            promoters_count = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).filter(nps_label = 'Promoter').values()
            passive_count = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).filter(nps_label = 'Passive').values()
            detractors_count = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).filter(nps_label = 'Detractor').values()
            state = region
            if '' not in state:
                total_count = total_count.filter(REGION__in = state)
                promoters_count = promoters_count.filter(REGION__in = state)
                passive_count = passive_count.filter(REGION__in = state)
                detractors_count = detractors_count.filter(REGION__in = state)
            if '' not in clinic:
                total_count = total_count.filter(NPSCLINIC__in = clinic)
                promoters_count = promoters_count.filter(NPSCLINIC__in = clinic)
                passive_count = passive_count.filter(NPSCLINIC__in = clinic)
                detractors_count = detractors_count.filter(NPSCLINIC__in = clinic)
            
            if(len(promoters_count)>0):
                    promoters = round(len(promoters_count)/len(total_count)*100)
                    if promoters == 0:
                        promoters = round(len(promoters_count)/len(total_count)*100,2)
            else:
                promoters = 0     

            if(len(passive_count)>0):
                    passive = round(len(passive_count)/len(total_count)*100)
                    if passive == 0:
                        passive = round(len(passive_count)/len(total_count)*100,2)
            else:
                passive = 0      

            if(len(detractors_count)>0):
                    detractors = round(len(detractors_count)/len(total_count)*100)
                    if detractors == 0:
                        detractors = round(len(detractors_count)/len(total_count)*100,2)
            else:
                detractors = 0      
            
            nps ={
                    "nps_score":(promoters-detractors),
                    "promoters":promoters,
                    "total_promoters":len(promoters_count),
                    "passive":passive,
                    "total_passive":len(passive_count),
                    "detractors":detractors,
                    "total_detractors":len(detractors_count),
                }

            nps_pie = [{
                            "label":"Promoters",
                            "percentage":promoters,
                            "color":"#00AC69",
                        },
                        {
                            "label":"Passives",
                            "percentage":passive,
                            "color":"#939799",
                        },
                        {
                            "label":"Detractors",
                            "percentage":detractors,
                            "color":"#DB2B39",
                        }]

            return Response({'Message':'TRUE',
                                'nps':nps,
                                        'nps_pie':nps_pie})
    except:
        return Response({'Message':'FALSE'})


@api_view(['POST'])
def netSentimentScore(request,format=None):
    try:
        if request.method == 'POST':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})  
            except:
                return Response({'Message':'FALSE'})
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub
            total_count = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()
            positive_count = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).filter(sentiment_label='Positive').values()
            negative_count = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).filter(sentiment_label='Negative').values()
            extreme_count = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).filter(sentiment_label='Extreme').values()

            state = region
            if '' not in region:
                total_count = total_count.filter(REGION__in = state)
                positive_count = positive_count.filter(REGION__in = state)
                negative_count = negative_count.filter(REGION__in = state)
                extreme_count = extreme_count.filter(REGION__in = state)
            
            if '' not in clinic:
                total_count = total_count.filter(NPSCLINIC__in = clinic)
                positive_count = positive_count.filter(NPSCLINIC__in = clinic)
                negative_count = negative_count.filter(NPSCLINIC__in = clinic)
                extreme_count = extreme_count.filter(NPSCLINIC__in = clinic)
            
            if(len(positive_count)!=0):
                positive = round(len(positive_count)/len(total_count)*100)
                if positive == 0:
                    positive = round(len(positive_count)/len(total_count)*100,2)
            else:
                positive = 0
            
            if(len(negative_count)!=0):
                negative = round(len(negative_count)/len(total_count)*100)
                if negative == 0:
                    negative = round(len(negative_count)/len(total_count)*100,2)
            else:
                negative = 0
            
            if(len(extreme_count)!=0):
                extreme = round(len(extreme_count)/len(total_count)*100)
                if extreme == 0:
                    extreme = round(len(extreme_count)/len(total_count)*100,2)
            else:
                extreme = 0

            nss ={
                    "nss_score":round(positive-negative-extreme),
                    "total": len(total_count),
                    "positive":positive,
                    "total_positive":len(positive_count),
                    "negative":negative,
                    "total_negative":len(negative_count),
                    "extreme":extreme,
                    "total_extreme":len(extreme_count),
                    "total_neutral": len(total_count) - len(positive_count) - len(negative_count) - len(extreme_count)
                }
                
            nss_pie = [{
                        "label":"Positive",
                        "percentage":positive,
                        "color":"#00AC69",
                    },
                    {
                        "label":"Negative",
                        "percentage":negative,
                        "color":"#EE6123",
                    },
                    {
                        "label":"Extreme",
                        "percentage":extreme,
                        "color":"#DB2B39",
                    }]
            return Response({'Message':'TRUE',
                             'nss':nss,
                             'nss_pie':nss_pie})
    except:
        return Response({'Message':'FALSE'})


@api_view(['POST'])
def totalCards(request,format=None):
    try:
        if request.method == 'POST':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})    
            except:
                return Response({'Message':'FALSE'})
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub 
            survey_comments = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values_list('REVIEW_ID').distinct()
            alert_comments = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).filter(sentiment_label = 'Extreme')
            clinics = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values_list('NPSCLINIC').distinct()
            doctors = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).exclude(PROVIDER_NAME__isnull=True).exclude(PROVIDER_NAME__exact='nan').values_list('PROVIDER_NAME').distinct()
            clients = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).exclude(CLIENT_NAME__isnull=True).exclude(CLIENT_NAME__exact='nan').values_list('CLIENT_ID').distinct()
            state = region
            if '' not in region:
                survey_comments = survey_comments.filter(REGION__in = state)
                alert_comments = alert_comments.filter(REGION__in = state)
                clinics = clinics.filter(REGION__in = state)
                doctors = doctors.filter(REGION__in = state)
                clients = clients.filter(REGION__in = state)

            if '' not in clinic:
                survey_comments = survey_comments.filter(NPSCLINIC__in = clinic)
                alert_comments = alert_comments.filter(NPSCLINIC__in = clinic)
                clinics = clinics.filter(NPSCLINIC__in = clinic)
                doctors = doctors.filter(NPSCLINIC__in = clinic)
                clients = clients.filter(NPSCLINIC__in = clinic)
            card_data = {
                            'survey':len(survey_comments),
                            'comments': len(survey_comments),
                            'alerts': len(alert_comments),
                            'clinic': len(clinics),
                            'doctors':len(doctors),
                            'clients':len(clients),
                    }
        return Response({'Message':'TRUE','card_data':card_data})
    
    except:
        return Response({'Message':'FALSE'}) 

@api_view(['POST'])
def totalComments(request,format=None):
    try:
        if request.method == 'POST':     
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})    
            except:
                return Response({'Message':'FALSE'})
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub 
            
            all_comments = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()

            state = region
            if '' not in region:
                all_comments = all_comments.filter(REGION__in = state)
                

            if '' not in clinic:
                all_comments = all_comments.filter(NPSCLINIC__in = clinic)
    
            all_comments = all_comments.values('id')\
            .annotate(
                                                            review = Func(
                                                                Concat(F('REASONNPSSCORE'),V(' '),F('WHATDIDWELLWITHAPP'),V(' '),F('WHATDIDNOTWELLWITHAPP')),
                                                                V('nan'), V(''),
                                                                function='replace'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            time = F('TIMESTAMP'),
                                                            clinic = F('NPSCLINIC'),
                                                            question_type = V('REASONNPSSCORE', output_field=CharField())
                                                            
                                                )
            all_comments = all_comments.exclude(review = '  ')
            all_comments = sorted(all_comments, key=itemgetter('time'),reverse=True)
        return Response({'Message':'True','data':all_comments})
    except:
        return Response({'Message':'FALSE'}) 

@api_view(['POST'])
def positiveComments(request,format=None):
    try:
        if request.method == 'POST':     
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})    
            except:
                return Response({'Message':'FALSE'})  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub 
            
            positive_comments = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()

            state = region
            if '' not in region:
                positive_comments = positive_comments.filter(REGION__in = state)                

            if '' not in clinic:
                positive_comments = positive_comments.filter(NPSCLINIC__in = clinic)
                

            positive_comments = positive_comments.filter(sentiment_label = 'Positive').values('id')\
                                                .annotate(
                                                            review = Func(
                                                                Concat(F('REASONNPSSCORE'),V(' '),F('WHATDIDWELLWITHAPP'),V(' '),F('WHATDIDNOTWELLWITHAPP')),
                                                                V('nan'), V(''),
                                                                function='replace'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            clinic = F('NPSCLINIC'),
                                                            time = F('TIMESTAMP'),
                                                            question_type = V('REASONNPSSCORE', output_field=CharField())

                                                )
            positive_comments = positive_comments.exclude(review = '  ')
            positive_comments= sorted(positive_comments ,key=itemgetter('time'),reverse=True)    
        return Response({'Message':'True','count':len(positive_comments),'data':positive_comments})
    except:
        return Response({'Message':'FALSE'}) 


@api_view(['POST'])
def negativeComments(request,format=None):
    try:
        if request.method == 'POST':     
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})    
            except:
                return Response({'Message':'FALSE'})  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub 
            
            negative_comments = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()

            state = region
            if '' not in region:
                negative_comments = negative_comments.filter(REGION__in = state)                

            if '' not in clinic:
                negative_comments = negative_comments.filter(NPSCLINIC__in = clinic)
                

            negative_comments = negative_comments.filter(sentiment_label = 'Negative').values('id')\
                                                .annotate(
                                                            review = Func(
                                                                Concat(F('REASONNPSSCORE'),V(' '),F('WHATDIDWELLWITHAPP'),V(' '),F('WHATDIDNOTWELLWITHAPP')),
                                                                V('nan'), V(''),
                                                                function='replace'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            clinic = F('NPSCLINIC'),
                                                            time = F('TIMESTAMP'),
                                                            question_type = V('REASONNPSSCORE', output_field=CharField())

                                                )
            negative_comments = negative_comments.exclude(review = '  ')
            negative_comments= sorted(negative_comments ,key=itemgetter('time'),reverse=True)    
        return Response({'Message':'True','count':len(negative_comments),'data':negative_comments})
    except:
        return Response({'Message':'FALSE'}) 

@api_view(['POST'])
def neutralComments(request,format=None):
    try:
        if request.method == 'POST':     
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})    
            except:
                return Response({'Message':'FALSE'})  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub 
            
            neutral_comments = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()

            state = region
            if '' not in region:
                neutral_comments = neutral_comments.filter(REGION__in = state)                

            if '' not in clinic:
                neutral_comments = neutral_comments.filter(NPSCLINIC__in = clinic)
                

            neutral_comments = neutral_comments.filter(sentiment_label = 'Neutral').values('id')\
                                                .annotate(
                                                            review = Func(
                                                                Concat(F('REASONNPSSCORE'),V(' '),F('WHATDIDWELLWITHAPP'),V(' '),F('WHATDIDNOTWELLWITHAPP')),
                                                                V('nan'), V(''),
                                                                function='replace'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            clinic = F('NPSCLINIC'),
                                                            time = F('TIMESTAMP'),
                                                            question_type = V('REASONNPSSCORE', output_field=CharField())

                                                )
            neutral_comments = neutral_comments.exclude(review = '  ')
            neutral_comments= sorted(neutral_comments ,key=itemgetter('time'),reverse=True)    
        return Response({'Message':'True','count':len(neutral_comments),'data':neutral_comments})
    except:
        return Response({'Message':'FALSE'}) 

@api_view(['POST'])
def extremeComments(request,format=None):
    try:
        if request.method == 'POST':     
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})    
            except:
                return Response({'Message':'FALSE'})  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub 
            
            extreme_comments = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()

            state = region
            if '' not in region:
                extreme_comments = extreme_comments.filter(REGION__in = state)                

            if '' not in clinic:
                extreme_comments = extreme_comments.filter(NPSCLINIC__in = clinic)
                

            extreme_comments = extreme_comments.filter(sentiment_label = 'Extreme').values('id')\
                                                .annotate(
                                                            review = Func(
                                                                Concat(F('REASONNPSSCORE'),V(' '),F('WHATDIDWELLWITHAPP'),V(' '),F('WHATDIDNOTWELLWITHAPP')),
                                                                V('nan'), V(''),
                                                                function='replace'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            clinic = F('NPSCLINIC'),
                                                            time = F('TIMESTAMP'),
                                                            question_type = V('REASONNPSSCORE', output_field=CharField())

                                                )
            extreme_comments = extreme_comments.exclude(review = '  ')
            extreme_comments= sorted(extreme_comments ,key=itemgetter('time'),reverse=True)    
        return Response({'Message':'True','count':len(extreme_comments),'data':extreme_comments})
    except:
        return Response({'Message':'FALSE'})

@api_view(['POST'])
def alertComments(request,format=None):
    try:
        if request.method == 'POST':     
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})    
            except:
                return Response({'Message':'FALSE'})  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub 
            
            alert_comments = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()

            state = region
            if '' not in region:
                alert_comments = alert_comments.filter(REGION__in = state)                

            if '' not in clinic:
                alert_comments = alert_comments.filter(NPSCLINIC__in = clinic)
                

            alert_comments = alert_comments.filter(sentiment_label = 'Extreme').values('id')\
                                                .annotate(
                                                            review = Func(
                                                                Concat(F('REASONNPSSCORE'),V(' '),F('WHATDIDWELLWITHAPP'),V(' '),F('WHATDIDNOTWELLWITHAPP')),
                                                                V('nan'), V(''),
                                                                function='replace'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            clinic = F('NPSCLINIC'),
                                                            time = F('TIMESTAMP'),
                                                            question_type = V('REASONNPSSCORE', output_field=CharField())

                                                )
            alert_comments = alert_comments.exclude(review = '  ')
            alert_comments= sorted(alert_comments ,key=itemgetter('time'),reverse=True)    
        return Response({'Message':'True','data':alert_comments})
    except:
        return Response({'Message':'FALSE'}) 


@api_view(['POST'])
def npsOverTime(request,format=None):
    try:
        if request.method == 'POST':     
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})    
            except:
                return Response({'Message':'FALSE'})  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub
            nps = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()
            
            state = region
            if '' not in region:
                nps = nps.filter(REGION__in = state)
                

            if '' not in clinic:
                nps = nps.filter(NPSCLINIC__in = clinic)
            
            nps = nps.values('SURVEY_MONTH' ).annotate(
                                                    count = Count(F('REVIEW_ID')),
                                                    # promoter = twoDecimal((Cast(Sum(Case(
                                                    #             When(nps_label='Promoter',then=1),
                                                    #             default=0,
                                                    #             output_field=IntegerField()
                                                    #             )),FloatField())/F('count'))*100),\
                                                    # passive =  twoDecimal((Cast(Sum(Case(
                                                    #             When(nps_label='Passive',then=1),
                                                    #             default=0,
                                                    #             output_field=IntegerField()
                                                    #             )),FloatField())/F('count'))*100),\
                                                    # detractor = twoDecimal((Cast(Sum(Case(
                                                    #             When(nps_label='Detractor',then=1),
                                                    #             default=0,
                                                    #             output_field=IntegerField()
                                                    #             )),FloatField())/F('count'))*100),\
                                                    promoter = twoDecimal((Cast(Sum(Case(
                                                                When(nps_label='Promoter',then=1),
                                                                default=0,
                                                                output_field=IntegerField()
                                                                )),FloatField()))),\
                                                    passive =  twoDecimal((Cast(Sum(Case(
                                                                When(nps_label='Passive',then=1),
                                                                default=0,
                                                                output_field=IntegerField()
                                                                )),FloatField()))),\
                                                    detractor = twoDecimal((Cast(Sum(Case(
                                                                When(nps_label='Detractor',then=1),
                                                                default=0,
                                                                output_field=IntegerField()
                                                                )),FloatField()))),\
                                                    month = Substr(F('SURVEY_MONTH'),1,3),\
                                                    year = Cast(F('SURVEY_YEAR'),IntegerField()),
                                                    nps_abs = twoDecimal(
                                                        ((F('promoter')-F('detractor'))/(F('promoter')+F('passive')+F('detractor')))*100),
                                                    NPS = Case(
                                                            When(
                                                                nps_abs__lt = 0,
                                                                then = 0    
                                                                ),
                                                                default=F('nps_abs'),
                                                                output_field=FloatField()
                                                              )
                                                )\
                                            .order_by('SURVEY_MONTH')
            
            nps = list(nps)
            nps.sort(key = lambda x: dt.strptime(x['SURVEY_MONTH'], '%b-%y')) 
        return Response({'Message':'True','nps_over_time':nps})
    except:
        return Response({'Message':'FALSE'})

@api_view(['POST'])
def nssOverTime(request,format=None):
    try:
        if request.method == 'POST':     
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})    
            except:
                return Response({'Message':'FALSE'})  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub
            nss = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()
            
            state = region
            if '' not in region:
                nss = nss.filter(REGION__in = state)
                

            if '' not in clinic:
                nss = nss.filter(NPSCLINIC__in = clinic)
            nss = nss.values('SURVEY_MONTH' ).annotate(
                                                    positive = twoDecimal((Cast(Sum(Case(
                                                                When(sentiment_label='Positive',then=1),
                                                                default=0,
                                                                output_field=IntegerField()
                                                                )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),\
                                                    negative = twoDecimal((Cast(Sum(Case(
                                                                When(sentiment_label='Negative',then=1),
                                                                default=0,
                                                                output_field=IntegerField()
                                                                )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),\
                                                    extreme = twoDecimal((Cast(Sum(Case(
                                                                When(sentiment_label='Extreme',then=1),
                                                                default=0,
                                                                output_field=IntegerField()
                                                                )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),\
                                                    neutral = twoDecimal((Cast(Sum(Case(
                                                                When(sentiment_label='Neutral',then=1),
                                                                default=0,
                                                                output_field=IntegerField()
                                                                )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),\
                                                    month = Substr(F('SURVEY_MONTH'),1,3),\
                                                    year = Cast(F('SURVEY_YEAR'),IntegerField()),
                                                    nss_abs = twoDecimal(F('positive')-F('negative')-F('extreme')),
                                                    nss = Case(
                                                            When(
                                                                nss_abs__lt = 0,
                                                                then = 0    
                                                                ),
                                                                default=F('nss_abs'),
                                                                output_field=FloatField()
                                                              )
                                                            

            )   
            nss = list(nss)
            nss.sort(key = lambda x: dt.strptime(x['SURVEY_MONTH'], '%b-%y')) 
        return Response({'Message':'True','nss_over_time':nss})
    except:
        return Response({'Message':'FALSE'})
    
@api_view(['POST'])
def npsVsSentiments(request,format=None):
    try:
        if request.method == 'POST':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})    
            except:
                return Response({'Message':'FALSE'})  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub
        
            all_data = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()
            
            state = region
            if '' not in region:
                all_data = all_data.filter(REGION__in = state)
                

            if '' not in clinic:
                all_data = all_data.filter(NPSCLINIC__in = clinic)

            positive = all_data.values('sentiment_label').filter(sentiment_label = 'Positive')\
                                .annotate(
                                            promoter = twoDecimal((Cast(Sum(Case(
                                                        When(nps_label='Promoter',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),
                                            passive =  twoDecimal((Cast(Sum(Case(
                                                        When(nps_label='Passive',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),
                                            detractor = twoDecimal((Cast(Sum(Case(
                                                        When(nps_label='Detractor',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100)
                                        ).order_by('sentiment_label')

            negative = all_data.values('sentiment_label').filter(sentiment_label = 'Negative')\
                                .annotate(
                                            promoter = twoDecimal((Cast(Sum(Case(
                                                        When(nps_label='Promoter',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),
                                            passive =  twoDecimal((Cast(Sum(Case(
                                                        When(nps_label='Passive',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),
                                            detractor = twoDecimal((Cast(Sum(Case(
                                                        When(nps_label='Detractor',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100)
                                        ).order_by('sentiment_label')
            neutral = all_data.values('sentiment_label').filter(sentiment_label = 'Neutral')\
                                .annotate(
                                            promoter = twoDecimal((Cast(Sum(Case(
                                                        When(nps_label='Promoter',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),
                                            passive =  twoDecimal((Cast(Sum(Case(
                                                        When(nps_label='Passive',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),
                                            detractor = twoDecimal((Cast(Sum(Case(
                                                        When(nps_label='Detractor',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100)
                                        ).order_by('sentiment_label')
            extreme = all_data.values('sentiment_label').filter(sentiment_label = 'Extreme')\
                                .annotate(
                                            promoter = twoDecimal((Cast(Sum(Case(
                                                        When(nps_label='Promoter',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),
                                            passive =  twoDecimal((Cast(Sum(Case(
                                                        When(nps_label='Passive',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),
                                            detractor = twoDecimal((Cast(Sum(Case(
                                                        When(nps_label='Detractor',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100)
                                        ).order_by('sentiment_label')
            if(len(list(positive)) == 0):
                possitive = [{
                                "sentiment_label": "Positive",
                                "promoter": 0,
                                "passive": 0,
                                "detractor": 0
                            }]
            if(len(list(negative)) == 0):
                negative = [{
                                "sentiment_label": "negative",
                                "promoter": 0,
                                "passive": 0,
                                "detractor": 0
                            }]
            if(len(list(neutral)) == 0):
                neutral = [{
                                "sentiment_label": "neutral",
                                "promoter": 0,
                                "passive": 0,
                                "detractor": 0
                            }]
            if(len(list(extreme)) == 0):
                extreme = [{
                                "sentiment_label": "Extreme",
                                "promoter": 0,
                                "passive": 0,
                                "detractor": 0
                            }]
            final_data = list(positive)+list(negative)+list(neutral)+list(extreme)
        return Response({'Message':'TRUE','data':final_data})   
    except:
        return Response({'Message':'FALSE'})


@api_view(['POST'])
def providersData(request,format=None):
    try:
        if request.method == 'POST':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})  
            except:
                return Response({'Message':'FALSE'})  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub 
        
            providers = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()
            
            state = region
            if '' not in region:
                providers = providers.filter(REGION__in = state)
                

            if '' not in clinic:
                providers = providers.filter(NPSCLINIC__in = clinic)
            
            providers = providers.exclude(PROVIDER_NAME__in = ['nan']).annotate(provider_name = F('PROVIDER_NAME'))\
                                            .values('provider_name')\
                                            .annotate(
                                                    count = Count(F('REVIEW_ID')),
                                                    promoter = Sum(Case(
                                                        When(nps_label='Promoter',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),
                                                    detractor = Sum(Case(
                                                        When(nps_label='Detractor',then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),
                                                    average_nps=Cast(Round((Cast((F('promoter')-F('detractor')),FloatField())/F('count'))*100),IntegerField()),
                                                    provider_type = F('PROVIDERTYPE'),
                                                    provider_category = F('PROVIDER_CATEGORY'),
            ).order_by('provider_name')
            # providers = sorted(list(providers), key=itemgetter('average_nps'),reverse=True) 
        return Response({'Message':'True','data':providers})
    except:
        return Response({'Message':'FALSE'})

@api_view(['POST'])
def clinicData(request,format=None):
    # try:
        if request.method == 'POST':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})  
            except:
                return Response({'Message':'FALSE'})  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub 
            clinic_data = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()
            state = region
            if '' not in region:
                clinic_data = clinic_data.filter(REGION__in = state)
            if '' not in clinic:
                clinic_data = clinic_data.filter(NPSCLINIC__in = clinic)
            clinic_data = clinic_data.annotate(clinic=F('NPSCLINIC'))\
                                 .values('clinic')\
                                 .annotate(
                                        count = Count(F('REVIEW_ID')),
                                        promoter = Sum(Case(
                                            When(nps_label='Promoter',then=1),
                                            default=0,
                                            output_field=IntegerField()
                                            )),
                                        detractor = Sum(Case(
                                            When(nps_label='Detractor',then=1),
                                            default=0,
                                            output_field=IntegerField()
                                            )),
                                        average_nps=Cast(Round((Cast((F('promoter')-F('detractor')),FloatField())/F('count'))*100),IntegerField()),
                                        city = F('CLINIC_CITY'),
                                        state = F('CLINIC_STATE'),
                                        address = Concat('CLINIC_CITY', V(', '), 'CLINIC_STATE'),
                                        region = F('REGION')
                                          )\
                                 .order_by('clinic')
            # clinic_data = sorted(list(clinic_data), key=itemgetter('average_nps'),reverse=True)
        return Response({'Message':'True','data':clinic_data})
    # except:
    #     return Response({'Message':'FALSE'})

@api_view(['POST'])
def clientData(request,format=None):
    try:
        if request.method == 'POST':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)
            try:
                check_token = user_data.objects.get(USERNAME = (request.data)['username'])
                if(check_token.TOKEN != (request.headers)['Authorization']):
                    return Response({'Message':'FALSE'})  
            except:
                return Response({'Message':'FALSE'})  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple())) - timestamp_start
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub
            clients = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()
            state = region
            if '' not in region:
                clients = clients.filter(REGION__in = state)
            if '' not in clinic:
                clients = clients.filter(NPSCLINIC__in = clinic)
            parent_client_names = clients.values_list('PARENT_CLIENT_NAME',flat=True).distinct()
            parent_client_names = sorted(list(parent_client_names))
            clients = clients.annotate(client_name=F('CLIENT_NAME'))\
                                 .values('client_name')\
                                 .annotate(
                                        parent_client_name = F('PARENT_CLIENT_NAME'),
                                        count = Count(F('REVIEW_ID')),
                                        promoter = Sum(Case(
                                            When(nps_label='Promoter',then=1),
                                            default=0,
                                            output_field=IntegerField()
                                            )),
                                        detractor = Sum(Case(
                                            When(nps_label='Detractor',then=1),
                                            default=0,
                                            output_field=IntegerField()
                                            )),
                                        average_nps=Cast(Round((Cast((F('promoter')-F('detractor')),FloatField())/F('count'))*100),IntegerField()),
                                          )\
                                 .order_by('client_name')
            # clients = sorted(list(clients), key=itemgetter('average_nps'),reverse=True)
        return Response({'Message':'True','data':clients,'parent_client_names':parent_client_names})
    except:
        return Response({'Message':'FALSE'})

#------------------------------------------------------------------------------------------------------
# def index(request):
#     df = pd.read_csv('regionState.csv')
#     df = df.dropna(subset=['State'])
#     df.drop(df[df['State'] == 'Unknown'].index, inplace = True)
#     for i in range(df.shape[0]):
#         print(i)
#         everside_nps.objects.filter(CLINIC_STATE=list(df['State'])[i]).update(REGION=list(df['Region'])[i])
#     return HttpResponse('Hello')
#--------------------------------Enagement Moddel------------------------------------------------------

@api_view(['POST'])
@parser_classes([MultiPartParser,FormParser])
def egMemberPercentile(request,format=None):    
    try:
        try:
            file_name = str((request.data)['username'])+'.csv'
            name = 'uploads/engagement_files/'+file_name
        except:
            return Response({'Message':'FALSE','Error':'except'})
        file_list = os.listdir('uploads/engagement_files')
        if file_name in file_list:
            try:
                up_file = request.FILES.getlist('file')
                df = pd.read_csv(up_file[0])
                try:
                    prob_func(df)
                except:
                    return Response({'Message':'FALSE','Error':'except'})
                df.to_csv(name,index = False)
                engagement_file_data.objects.filter(USERNAME = str((request.data)['username'])).delete()
                data = engagement_file_data(USERNAME = str((request.data)['username']),
                                            FILE_NAME = str(up_file[0]),
                                            FILE_SIZE = (up_file[0]).size)
                data.save()
            except:
                df = pd.read_csv(name)  
        
        else:
            up_file = request.FILES.getlist('file')
            df = pd.read_csv(up_file[0])
            ndf = df[['GENDER','AGE','CLIENT_ID','MEMBER_ID','CLIENT_ENROLL_CONTRACT_TYP']]
            try:
                prob_func(df)
            except:
                return Response({'Message':'FALSE','Error':'except'})
            df.to_csv(name,index = False)
            engagement_file_data.objects.filter(USERNAME = str((request.data)['username'])).delete()
            data = engagement_file_data(USERNAME = str((request.data)['username']),
                                        FILE_NAME = str(up_file[0]),
                                        FILE_SIZE = (up_file[0]).size)
            data.save()
        out = prob_func(df)
        out_prob = list(out['probability'])
        low = 0 # n < 0.5
        med = 0 # 0.5 < n < 0.75
        high = 0 # 0.75 < n
        graph = [] 
        p_values = [0,1,25,33,50,66,75,95,99,100]
        for i in p_values:
            p = np.percentile(out_prob,i)
            percentile_name = "P"+str(i)
            percentile_value = round(p,3)
            member_score = out_prob.count(p)
            if p < 0.5:
                low = low + 1
            elif 0.5 <= p < 0.75:
                med = med + 1
            else:
                high = high + 1

            frame = {
                'percentile_name':percentile_name,
                'percentile_value':percentile_value,
                'member_score':member_score
            }
            graph.append(frame)
            percentage = {
                'low':str(low*10)+"%",
                'medium':str(low*10+med*10)+"%",
                'high':'100%',
            }
#--------------------------------------Card Data----------------------------------------------------
        rows = df.shape[0]
        columns = df.shape[1]
        client_count = len(set(list(df['CLIENT_ID'])))
        member_count = len(set(list(df['MEMBER_ID'])))
        try:
            opt_in = list(df['CLIENT_ENROLL_CONTRACT_TYP']).count('Opt In')
        except:
            opt_in = 0
        try:
            flat_fee = list(df['CLIENT_ENROLL_CONTRACT_TYP']).count('Flat Fee')
        except:
            flat_fee = 0
        try:
            all_in_eligible = list(df['CLIENT_ENROLL_CONTRACT_TYP']).count('All-In-Eligible')
        except:
            all_in_eligible = 0
        try:
            near_site = list(df['CLIENT_DEF_HC_TYPE']).count('Near Site')
        except:
            near_site = 0
        try:
            on_site = list(df['CLIENT_DEF_HC_TYPE']).count('On Site')
        except:
            on_site = 0
        cards_data = [
                {
                    'name':'Rows',
                    'value':rows
                },
                {
                    'name':'Columns',
                    'value':columns
                },
                {
                    'name':'Clients',
                    'value':client_count
                },
                {
                    'name':'Members',
                    'value':member_count
                },
                {
                    'name':'Opt In',
                    'value':opt_in
                },
                {
                    'name':'Flat Fee',
                    'value':flat_fee
                },
                {
                    'name':'All In Eligible',
                    'value':all_in_eligible
                },
                {
                    'name':'Near Site',
                    'value':near_site
                },
                {
                    'name':'On Site',
                    'value':on_site
                },
        ]
#-----------------------------------------Age Graph--------------------------------------------
        group_list = [(0,12),(13,19),(20,29),(30,39),(40,49),(50,59),(60,69),(70,79),(80,89),(90,1000)]
        age_list = list(df['AGE'])
        age_graph = []
        for i in group_list:
            if(i[1]<90):  
                age_graph.append(
                                {
                                    'groupName':str(i[0])+'-'+str(i[1]),
                                    'groupValue': sum(map(age_list.count, range(i[0],i[1]+1)))

                                }) 
            else:
                  age_graph.append(
                                {
                                    'groupName':str(i[0])+'+',
                                    'groupValue': sum(map(age_list.count, range(i[0],i[1]+1)))

                                })         

#---------------------------------------Gender Chart-----------------------------------------------------
        gender_list = list(df['GENDER'])
        gender_list = list(map(lambda x: x.lower(), gender_list))
        try:
            male_count = gender_list.count('male')
        except:
            male_count = 0
        try:
            female_count = gender_list.count('female')
        except:
            female_count = 0
        try:
            others_count = gender_list.count('others')
        except:
            others_count = 0
        gender = {
              'total_male':male_count,
              'male':round((male_count/len(gender_list))*100,2),
              'total_female':female_count,
              'female':round((female_count/len(gender_list))*100,2),
              'total_other':others_count,
              'other': round((others_count/len(gender_list))*100,2),  
        }
        gender_pie = [{
                        'label':'Male',
                        'percentage': round((male_count/len(gender_list))*100,2),
                        'color': '#39a0ed'
                    },
                    {
                        'label':'Female',
                        'percentage': round((female_count/len(gender_list))*100,2),
                        'color': '#13c4a3'
                    },
                    {
                        'label':'Other',
                        'percentage': round((others_count/len(gender_list))*100,2),
                        'color': '#d77a69'
                    }]

        #---------------------------------Map-------------------------------------------------------
        state_codes = region_names()
        zip_df = pd.read_csv('zip_codes.csv')
        ndf = df.drop_duplicates(subset='ZIP', keep="last")
        lat_long_df = pd.merge(ndf,zip_df,how='left',on=['ZIP'])
        state = list(lat_long_df['STATE'])
        region = list(lat_long_df['REGION'])
        long = list(lat_long_df['Y'])
        lat = list(lat_long_df['X'])
        zip = list(lat_long_df['ZIP'])
        map_data = []
        for i in range(lat_long_df.shape[0]):
            frame = {
                    'state':state_codes[state[i]],
                    'region':region[i],
                    'long':long[i],
                    'lat':lat[i],
                    'zip':zip[i],
                    'zip_count':(list(df['ZIP'])).count(zip[i])
            }
            map_data.append(frame)
        #---------------------------------File Name and Size-----------------------------------------
        f_obj = engagement_file_data.objects.filter(USERNAME = str((request.data)['username'])).values()
        #------------------------Response------------------------------------------------------------
        return Response({'Message':'TRUE',
                         'file_name':(f_obj[0])['FILE_NAME'],
                         'file_size':(f_obj[0])['FILE_SIZE'],
                         'graph':graph,
                         'percentage':percentage,
                         'cards_data':cards_data,
                         'age_graph':age_graph,
                         'gender':gender,
                         'gender_pie':gender_pie,
                         'map_data':map_data,
                         'lat_mid':sum(lat)/len(lat),
                         'long_mid':sum(long)/len(long)})
        
    except:
        return Response({'Message':"FALSE",'Error':'final except'})

@api_view(['GET'])
@parser_classes([MultiPartParser,FormParser])
def fileDownload(request,format=None):
    try:
        username = request.GET.get('username')
        # username = 'vivekeko'
        file_name = 'uploads/engagement_files/'+username+'.csv'
        f_obj = engagement_file_data.objects.filter(USERNAME = username).values()
        f_name = (f_obj[0])['FILE_NAME'][:-4]
        print(file_name)
        df = pd.read_csv(file_name)
        out = prob_func(df)
        a = 'uploads/engagement_files/'+f_name+'_'+username+'.csv'
        out.to_csv(a,index=False)
        response = FileResponse(open(a, 'rb'))
        return response
    except:
        return Response({'Message':'FALSE'})
