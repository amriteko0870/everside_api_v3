
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models import Avg,Count,Case, When, IntegerField,Sum,FloatField,CharField
from django.db.models import F,Func
from django.db.models import Value as V
from django.db.models.functions import Concat,Cast,Substr
import pandas as pd
import time
from datetime import datetime as dt
import datetime
import re
from itertools import chain
from operator import itemgetter     



#----------------------------restAPI--------------------------------------------------
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser,FormParser

#--------------------------Models-----------------------------------------------------
from apiApp.models import everside_nps

#--------------------------extra libs------------------------------------------------
from apiApp.extra_vars import region_names
# Create your views here.

#-------------- Global Variable-------------------------------------------------------
timestamp_sub = 86400 #-19800
#--------------------------- Filters---------------------------------------------------
class roundRating(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 1)'
class twoDecimal(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'

@api_view(['GET'])
def filterRegion(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub         
            frame = region_names() 
            region = []
            obj = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).exclude(CLINIC_STATE__isnull=True).exclude(CLINIC_STATE__exact='nan').values_list('CLINIC_STATE',flat=True).distinct()       
            for i in obj:
                region.append(str(frame[i])+','+str(i))
                
            region.sort()
        return Response({'Message':'TRUE','region':region})
    except:
        return Response({'Message':'FALSE'})

@api_view(['GET'])
def filterClinic(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = request.GET.get('region')
            region = re.split(r"-|,", region)
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub  
            obj = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values_list('NPSCLINIC',flat=True).distinct()    
            if '' not in region:
                obj = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).filter(CLINIC_STATE__in=region).values_list('NPSCLINIC',flat=True).distinct()
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
        
            if username == 'everside_user' or username == 'user@everside.com':
                if password == 'Test@1234':
                    return Response({'Message':'TRUE'})
                else:
                    return Response({'Message':'FALSE'})
            elif username=='a':
                if password=='a':
                    return Response({'Message':'TRUE'})
                else:
                    return Response({'Message':'FALSE'})
            else:
                return Response({'Message':'FALSE'})
        except:
            return Response({'Message':'FALSE'})
            
#---------------------For Dashboards--------------------------------------------------
@api_view(['GET'])
def netPromoterScore(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)       
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
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
                total_count = total_count.filter(CLINIC_STATE__in = state)
                promoters_count = promoters_count.filter(CLINIC_STATE__in = state)
                passive_count = passive_count.filter(CLINIC_STATE__in = state)
                detractors_count = detractors_count.filter(CLINIC_STATE__in = state)
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


@api_view(['GET'])
def netSentimentScore(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
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
                total_count = total_count.filter(CLINIC_STATE__in = state)
                positive_count = positive_count.filter(CLINIC_STATE__in = state)
                negative_count = negative_count.filter(CLINIC_STATE__in = state)
                extreme_count = extreme_count.filter(CLINIC_STATE__in = state)
            
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


@api_view(['GET'])
def totalCards(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub 
            survey_comments = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values_list('REVIEW_ID').distinct()
            alert_comments1 = everside_nps.objects.filter(TIMESTAMP__gte=startDate)\
                                                .filter(TIMESTAMP__lte=endDate)\
                                                .filter(sentiment_label = 'Extreme').values('id')\
                                                .filter(REASONNPSSCORE__length__gt=1)\
                                                .exclude(REASONNPSSCORE__in = ['N/A','nan','na','n/a','Na','N/a','','-'])\
                                                .exclude(REASONNPSSCORE__isnull = True)\
                                                .annotate(
                                                            review = F('REASONNPSSCORE'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            clinic = F('NPSCLINIC'),
                                                            time = F('TIMESTAMP'),
                                                            CLINIC_STATE = F('CLINIC_STATE'),
                                                            NPSCLINIC = F('NPSCLINIC'),
                                                            question_type = V('REASONNPSSCORE', output_field=CharField())

                                                )
            alert_comments2 = everside_nps.objects.filter(TIMESTAMP__gte=startDate)\
                                                .filter(TIMESTAMP__lte=endDate)\
                                                .filter(sentiment_label = 'Extreme').values('id')\
                                                .filter(WHATDIDNOTWELLWITHAPP__length__gt=1)\
                                                .exclude(WHATDIDNOTWELLWITHAPP__in = ['N/A','nan','na','n/a','Na','N/a','','-'])\
                                                .exclude(WHATDIDNOTWELLWITHAPP__isnull = True)\
                                                .annotate(
                                                            review = F('WHATDIDNOTWELLWITHAPP'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            clinic = F('NPSCLINIC'),
                                                            time = F('TIMESTAMP'),
                                                            CLINIC_STATE = F('CLINIC_STATE'),
                                                            NPSCLINIC = F('NPSCLINIC'),
                                                            question_type = V('WHATDIDNOTWELLWITHAPP', output_field=CharField())
                                                )
            clinics = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values_list('NPSCLINIC').distinct()
            doctors = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).exclude(PROVIDER_NAME__isnull=True).exclude(PROVIDER_NAME__exact='nan').values_list('PROVIDER_NAME').distinct()
            clients = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).exclude(CLIENT_NAME__isnull=True).exclude(CLIENT_NAME__exact='nan').values_list('CLIENT_ID').distinct()
            state = region
            if '' not in region:
                survey_comments = survey_comments.filter(CLINIC_STATE__in = state)
                alert_comments1 = alert_comments1.filter(CLINIC_STATE__in = state)
                alert_comments2 = alert_comments2.filter(CLINIC_STATE__in = state)
                clinics = clinics.filter(CLINIC_STATE__in = state)
                doctors = doctors.filter(CLINIC_STATE__in = state)
                clients = clients.filter(CLINIC_STATE__in = state)

            if '' not in clinic:
                survey_comments = survey_comments.filter(NPSCLINIC__in = clinic)
                alert_comments1 = alert_comments1.filter(NPSCLINIC__in = clinic)
                alert_comments2 = alert_comments2.filter(NPSCLINIC__in = clinic)
                clinics = clinics.filter(NPSCLINIC__in = clinic)
                doctors = doctors.filter(NPSCLINIC__in = clinic)
                clients = clients.filter(NPSCLINIC__in = clinic)
            card_data = {
                            'survey':len(survey_comments),
                            'comments': len(survey_comments),
                            'alerts': len(alert_comments1)+len(alert_comments2),
                            'clinic': len(clinics),
                            'doctors':len(doctors),
                            'clients':len(clients),
                    }
        return Response({'Message':'TRUE','card_data':card_data})
    
    except:
        return Response({'Message':'FALSE'}) 

@api_view(['GET'])
def totalComments(request,format=None):
    try:
        if request.method == 'GET':     
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub 
            
            all_comments1 = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()
            all_comments2 = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()
            all_comments3 = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()

            state = region
            if '' not in region:
                all_comments1 = all_comments1.filter(CLINIC_STATE__in = state)
                all_comments2 = all_comments2.filter(CLINIC_STATE__in = state)
                all_comments3 = all_comments3.filter(CLINIC_STATE__in = state)
                

            if '' not in clinic:
                all_comments1 = all_comments1.filter(NPSCLINIC__in = clinic)
                all_comments2 = all_comments2.filter(NPSCLINIC__in = clinic)
                all_comments2 = all_comments3.filter(NPSCLINIC__in = clinic)
                

            
            all_comments1 = all_comments1.filter(REASONNPSSCORE__length__gt=1)\
            .exclude(REASONNPSSCORE__in = ['N/A','nan','na','n/a','Na','N/a','','-'])\
            .exclude(REASONNPSSCORE__isnull = True).values('id')\
            .annotate(
                                                            review = F('REASONNPSSCORE'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            time = F('TIMESTAMP'),
                                                            question_type = V('REASONNPSSCORE', output_field=CharField())
                                                            
                                                )

            all_comments2 = all_comments2.filter(WHATDIDWELLWITHAPP__length__gt=1)\
            .exclude(WHATDIDWELLWITHAPP__in = ['N/A','nan','na','n/a','Na','N/a','','-'])\
            .exclude(WHATDIDWELLWITHAPP__isnull = True).values('id')\
            .annotate(
                                                            review = F('WHATDIDWELLWITHAPP'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            time = F('TIMESTAMP'),
                                                            question_type = V('WHATDIDWELLWITHAPP', output_field=CharField())

                                                )

            all_comments3 = all_comments3.filter(WHATDIDNOTWELLWITHAPP__length__gt=1)\
            .exclude(WHATDIDNOTWELLWITHAPP__in = ['N/A','nan','na','n/a','Na','N/a','','-'])\
            .exclude(WHATDIDNOTWELLWITHAPP__isnull = True).values('id').values('id')\
            .annotate(
                                                            review = F('WHATDIDNOTWELLWITHAPP'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            time = F('TIMESTAMP'),
                                                            question_type = V('WHATDIDNOTWELLWITHAPP', output_field=CharField())

                                                )
            all_comments =  list(all_comments1) + list(all_comments2) + list(all_comments3)
            all_comments = sorted(all_comments, key=itemgetter('time'),reverse=True)     

        return Response({'Message':'True','data':all_comments})
    except:
        return Response({'Message':'FALSE'}) 


@api_view(['GET'])
def alertComments(request,format=None):
    try:
        if request.method == 'GET':     
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub 
            
            alert_comments1 = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()
            alert_comments2 = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()

            state = region
            if '' not in region:
                alert_comments1 = alert_comments1.filter(CLINIC_STATE__in = state)
                alert_comments2 = alert_comments2.filter(CLINIC_STATE__in = state)
                

            if '' not in clinic:
                alert_comments1 = alert_comments1.filter(NPSCLINIC__in = clinic)
                alert_comments2 = alert_comments2.filter(NPSCLINIC__in = clinic)
                

            alert_comments1 = alert_comments1.filter(sentiment_label = 'Extreme').values('id')\
                                                .filter(REASONNPSSCORE__length__gt=1)\
                                                .exclude(REASONNPSSCORE__in = ['N/A','nan','na','n/a','Na','N/a','','-'])\
                                                .exclude(REASONNPSSCORE__isnull = True)\
                                                .annotate(
                                                            review = F('REASONNPSSCORE'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            clinic = F('NPSCLINIC'),
                                                            time = F('TIMESTAMP'),
                                                            question_type = V('REASONNPSSCORE', output_field=CharField())

                                                )

            alert_comments2 = alert_comments2.filter(sentiment_label = 'Extreme').values('id')\
                                                .filter(WHATDIDNOTWELLWITHAPP__length__gt=1)\
                                                .exclude(WHATDIDNOTWELLWITHAPP__in = ['N/A','nan','na','n/a','Na','N/a','','-'])\
                                                .exclude(WHATDIDNOTWELLWITHAPP__isnull = True)\
                                                .annotate(
                                                            review = F('WHATDIDNOTWELLWITHAPP'),
                                                            label = F('sentiment_label'),
                                                            timestamp = F('SURVEY_MONTH'), 
                                                            clinic = F('NPSCLINIC'),
                                                            time = F('TIMESTAMP'),
                                                            question_type = V('WHATDIDNOTWELLWITHAPP', output_field=CharField())

                                                )
            alert_comments=  list(alert_comments1) + list(alert_comments2)
            alert_comments= sorted(alert_comments ,key=itemgetter('time'),reverse=True)    
        return Response({'Message':'True','data':alert_comments})
    except:
        return Response({'Message':'FALSE'}) 







@api_view(['GET'])
def groupcheck(request,format=None):
    clinic = everside_nps.objects.annotate(clinic=F('NPSCLINIC'))\
                                 .values('clinic')\
                                 .annotate(
                                        average_nps=twoDecimal(Avg('NPS')),
                                        rating = roundRating(Avg('NPS')/2),
                                        address = Concat('CLINIC_CITY', V(', '), 'CLINIC_STATE'),
                                          )\
                                 .order_by('-average_nps')
    return Response(clinic)

@api_view(['GET'])
def npscheck(request,format=None):
    # try:
        if request.method == 'GET':     
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - timestamp_sub
        nps = everside_nps.objects.filter(TIMESTAMP__gte=startDate).filter(TIMESTAMP__lte=endDate).values()
        
        state = region
        if '' not in region:
            nps = nps.filter(CLINIC_STATE__in = state)
            

        if '' not in clinic:
            nps = nps.filter(NPSCLINIC__in = clinic)
        
        nps = nps.values('SURVEY_MONTH' ).annotate(
                                                promoter = twoDecimal((Cast(Sum(Case(
                                                            When(nps_label='Promoter',then=1),
                                                            default=0,
                                                            output_field=IntegerField()
                                                            )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),\
                                                passive =  twoDecimal((Cast(Sum(Case(
                                                            When(nps_label='Passive',then=1),
                                                            default=0,
                                                            output_field=IntegerField()
                                                            )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),\
                                                detractor = twoDecimal((Cast(Sum(Case(
                                                            When(nps_label='Detractor',then=1),
                                                            default=0,
                                                            output_field=IntegerField()
                                                            )),FloatField())/Cast(Count('REVIEW_ID'),FloatField()))*100),\
                                                month = Substr(F('SURVEY_MONTH'),1,3),\
                                                year = Cast(F('SURVEY_YEAR'),IntegerField()),
                                                nps = twoDecimal(F('promoter')-F('detractor'))
                                            )\
                                         .order_by('SURVEY_MONTH')
        
        nps = list(nps)
        nps.sort(key = lambda x: dt.strptime(x['SURVEY_MONTH'], '%b-%y')) 
        return Response({'Message':'True','nps_over_time':nps})

#---------------------For Database upload----------------------------------------------

# def index(request):
#     df = pd.read_csv('01_final_2018_2020.csv')
#     for i in range(1,df.shape[0]):
#         data = everside_nps(
#         REVIEW_ID = list(df['ID'])[i],
#         MEMBER_ID = list(df['MEMBER_ID'])[i],
#         NPSCLINIC = list(df['NPSCLINIC__C'])[i],
#         SURVEYDATE = list(df['SURVEYDATE__C'])[i],
#         SURVEY_MONTH = list(df['SURVEY_MONTH'])[i],
#         SURVEY_YEAR = list(df['SURVEY_YEAR'])[i],
#         SURVEYNUMBER = list(df['SURVEYNUMBER__C'])[i],
#         NPS = list(df['NPS'])[i],
#         REASONNPSSCORE = list(df['REASONNPSSCORE__C'])[i],
#         WHATDIDWELLWITHAPP = list(df['WHATDIDWELLWITHAPP__C'])[i],
#         WHATDIDNOTWELLWITHAPP = list(df['WHATDIDNOTWELLWITHAPP__C'])[i],
#         HOUSEHOLD_ID = list(df['HOUSEHOLD_ID'])[i],
#         MEMBER_CITY = list(df['MEMBER_CITY'])[i],
#         MEMBER_STATE = list(df['MEMBER_STATE'])[i],
#         MEMBER_ZIP = list(df['MEMBER_ZIP'])[i],
#         CLINIC_ID = list(df['CLINIC_ID'])[i],
#         CLINIC_STREET = list(df['CLINIC_STREET'])[i],
#         CLINIC_CITY = list(df['CLINIC_CITY'])[i],
#         CLINIC_STATE = list(df['CLINIC_STATE'])[i],
#         CLINIC_ZIP = list(df['CLINIC_ZIP'])[i],
#         CLINIC_TYPE = list(df['CLINIC_TYPE'])[i],
#         PROVIDER_NAME = list(df['PROVIDER_NAME'])[i],
#         PROVIDERTYPE = list(df['PROVIDERTYPE__C'])[i],
#         PROVIDER_CATEGORY = list(df['PROVIDER_CATEGORY__C'])[i],
#         CLIENT_ID = list(df['CLIENT_ID'])[i],
#         CLIENT_NAICS = list(df['CLIENT_NAICS'])[i],
#         sentiment_label = list(df['sentiment_label'])[i],
#         nps_label = list(df['nps_label'])[i],
#         CLIENT_NAME = list(df['CLIENT NAME'])[i],
#         PARENT_CLIENT_NAME = list(df['PARENT CLIENT NAME'])[i],
#         PARENT_CLIENT_ID = list(df['PARENT_CLIENT_ID'])[i],
#         TIMESTAMP = time.mktime(datetime.datetime.strptime(list(df['SURVEYDATE__C'])[i],"%m/%d/%Y").timetuple())
#         )
#         data.save()
#         # print(ID,'\n',
#         #         MEMBER_ID,'\n',
#         #         NPSCLINIC,'\n',
#         #         SURVEYDATE,'\n',
#         #         SURVEY_MONTH,'\n',
#         #         SURVEY_YEAR,'\n',
#         #         SURVEYNUMBER,'\n',
#         #         NPS,'\n',
#         #         REASONNPSSCORE,'\n',
#         #         WHATDIDWELLWITHAPP,'\n',
#         #         WHATDIDNOTWELLWITHAPP,'\n',
#         #         HOUSEHOLD_ID,'\n',
#         #         MEMBER_CITY,'\n',
#         #         MEMBER_STATE,'\n',
#         #         MEMBER_ZIP,'\n',
#         #         CLINIC_ID,'\n',
#         #         CLINIC_STREET,'\n',
#         #         CLINIC_CITY,'\n',
#         #         CLINIC_STATE,'\n',
#         #         CLINIC_ZIP,'\n',
#         #         CLINIC_TYPE,'\n',
#         #         PROVIDER_NAME,'\n',
#         #         PROVIDERTYPE,'\n',
#         #         PROVIDER_CATEGORY,'\n',
#         #         CLIENT_ID,'\n',
#         #         CLIENT_NAICS,'\n',
#         #         sentiment_label,'\n',
#         #         nps_label,'\n',
#         #         CLIENT_NAME,'\n',
#         #         PARENT_CLIENT_NAME,'\n',
#         #         PARENT_CLIENT_ID,)
#         print(i)

#     return HttpResponse('Hello')