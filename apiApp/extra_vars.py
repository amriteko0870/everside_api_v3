def region_names():
    frame = {'AL': 'Alabama',
                    'AK': 'Alaska',
                    'AZ': 'Arizona',
                    'AR': 'Arkansas',
                    'CA': 'California',
                    'CO': 'Colorado',
                    'CT': 'Connecticut',
                    'DE': 'Delaware',
                    'FL': 'Florida',
                    'GA': 'Georgia',
                    'HI': 'Hawaii',
                    'ID': 'Idaho',
                    'IL': 'Illinois',
                    'IN': 'Indiana',
                    'IA': 'Iowa',
                    'KS': 'Kansas',
                    'KY': 'Kentucky',
                    'LA': 'Louisiana',
                    'ME': 'Maine',
                    'MD': 'Maryland',
                    'MA': 'Massachusetts',
                    'MI': 'Michigan',
                    'MN': 'Minnesota',
                    'MS': 'Mississippi',
                    'MO': 'Missouri',
                    'MT': 'Montana',
                    'NE': 'Nebraska',
                    'NV': 'Nevada',
                    'NH': 'New Hampshire',
                    'NJ': 'New Jersey',
                    'NM': 'New Mexico',
                    'NY': 'New York',
                    'NC': 'North Carolina',
                    'ND': 'North Dakota',
                    'OH': 'Ohio',
                    'OK': 'Oklahoma',
                    'OR': 'Oregon',
                    'PA': 'Pennsylvania',
                    'RI': 'Rhode Island',
                    'SC': 'South Carolina',
                    'SD': 'South Dakota',
                    'TN': 'Tennessee',
                    'TX': 'Texas',
                    'UT': 'Utah',
                    'VT': 'Vermont',
                    'VA': 'Virginia',
                    'WA': 'Washington',
                    'WV': 'West Virginia',
                    'WI': 'Wisconsin',
                    'WY': 'Wyoming'}
    return frame


# @api_view(['GET'])
# def groupcheck(request,format=None):
#     clinic = everside_nps.objects.annotate(clinic=F('NPSCLINIC'))\
#                                  .values('clinic')\
#                                  .annotate(
#                                         average_nps=twoDecimal(Avg('NPS')),
#                                         rating = roundRating(Avg('NPS')/2),
#                                           )\
#                                  .order_by('-average_nps')
#     return Response({'Message':'True','data':clinic})

                     
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



#------------------------------------------

 

# def index(request):
#     #everside_nps.objects.filter(WHATDIDWELLWITHAPP__length__lte = 2).update(WHATDIDWELLWITHAPP = 'nan')
#     return HttpResponse('hello')