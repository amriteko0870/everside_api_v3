import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import math 


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

def prob_func(df):
    

    #df_engagement_client_data = pd.read_csv(file_name)
    df_engagement_client_data = df

    
    df_us_census_data = pd.read_csv('us_census_data.csv')

    df_engagement_model_data = df_engagement_client_data.merge(df_us_census_data, on = 'zip', how = 'left')


    df_engagement_model_data = df_engagement_model_data.rename(columns = {'__Black_or_African_American_alone':'per_black',
                                                                        '__Asian':'per_asian',
                                                                        '__With_a_disability':'per_with_disability',
                                                                        '__Worked_full-time,_year_round':'per_worked_ft',
                                                                        '__Worked_less_than_full-time,_year_round':'per_worked_lt_ft',
                                                                        '__household_population!!Below_$25,000':'hinc_below_25k',
                                                                        '__household_population!!$25,000_to_$49,999':'hinc_25k_to_50k',
                                                                        '__household_population!!$50,000_to_$74,999':'hinc_50k_to_75k',
                                                                        'Estimate__Percent_Insured_19_to':'per_ins_19_64',
                                                                        'Percent_Insured_AGE_55_to_64_yea':'per_ins_age_55_to_64',
                                                                        'Percent_Insured_Worked_full_time':'per_ins_worked_ft',
                                                                        'Insured__19_to_64_years!!Worked_less_than_full-time':'per_ins_19_64_worked_lt_ft',
                                                                        'Percent_Uninsured_19_to_25_years':'per_unins_19_25',
                                                                        'Percent_Uninsured_AGE_26_to_34_y':'per_unins_26_34',
                                                                        'Percent_Uninsured_AGE__45_to_54':'per_unins_45_54',
                                                                        'Percent_UninsuredAGE__55_to_64_y':'per_unins_55_64',
                                                                        'Percent_UninsuredAGE__19_to_64_y':'per_unins_19_64',
                                                                        'Percent_Uninsured_19_to_64_years':'per_unins_19_64_worked_lt_ft',
                                                                        '__Not_in_labor_force':'per_not_in_labor_force'})


    #Data Preparation

    df_engagement_model_data['per_not_in_labor_force'] = np.where(df_engagement_model_data.per_not_in_labor_force >=50,50,
                                                                np.where((df_engagement_model_data.per_not_in_labor_force >=30) & (df_engagement_model_data.per_not_in_labor_force <=50),30,df_engagement_model_data.per_not_in_labor_force))

    df_engagement_model_data['per_with_disability'] = np.where(df_engagement_model_data.per_with_disability >=30,30
                                                            ,df_engagement_model_data.per_with_disability)

    df_engagement_model_data['hinc_25k_to_50k'] = np.where(df_engagement_model_data.hinc_25k_to_50k >=40,40
                                                            ,df_engagement_model_data.hinc_25k_to_50k)

    df_engagement_model_data['hinc_50k_to_75k'] = np.where(df_engagement_model_data.hinc_50k_to_75k >=40,40
                                                            ,df_engagement_model_data.hinc_50k_to_75k)

    df_engagement_model_data['hinc_below_25k'] = np.where(df_engagement_model_data.hinc_below_25k >=40,40
                                                            ,df_engagement_model_data.hinc_below_25k)


    #State preparation

    df_engagement_model_data['d1_STATE'] = df_engagement_model_data[df_engagement_model_data.STATE_ZIP == 'IN'].STATE_ZIP
    df_engagement_model_data['d1_STATE'] = np.where(df_engagement_model_data['d1_STATE'].isna(),0,1)

    df_engagement_model_data['d2_STATE'] = df_engagement_model_data[df_engagement_model_data.STATE_ZIP.isin(['CO','OH'])].STATE_ZIP
    df_engagement_model_data['d2_STATE'] = np.where(df_engagement_model_data['d2_STATE'].isna(),0,1)

    df_engagement_model_data['d3_STATE'] = df_engagement_model_data[df_engagement_model_data.STATE_ZIP == 'MO'].STATE_ZIP
    df_engagement_model_data['d3_STATE'] = np.where(df_engagement_model_data['d3_STATE'].isna(),0,1)

    df_engagement_model_data['d4_STATE'] = df_engagement_model_data[df_engagement_model_data.STATE_ZIP == 'NV'].STATE_ZIP
    df_engagement_model_data['d4_STATE'] = np.where(df_engagement_model_data['d4_STATE'].isna(),0,1)

    #Region Preparation

    df_engagement_model_data['d2_REGION'] = df_engagement_model_data[df_engagement_model_data.REGION_ZIP == 'Northeast'].REGION_ZIP
    df_engagement_model_data['d2_REGION'] = np.where(df_engagement_model_data['d2_REGION'].isna(),0,1)

    df_engagement_model_data['d3_REGION'] = df_engagement_model_data[df_engagement_model_data.REGION_ZIP == 'South'].REGION_ZIP
    df_engagement_model_data['d3_REGION'] = np.where(df_engagement_model_data['d3_REGION'].isna(),0,1)

    #Age Data Preparation

    df_engagement_model_data['d1_AGE_O'] = df_engagement_model_data[df_engagement_model_data.age <= 28].age
    df_engagement_model_data['d1_AGE_O'] = np.where(df_engagement_model_data['d1_AGE_O'].isna(),0,1)

    df_engagement_model_data['d2_AGE_O'] = df_engagement_model_data[(df_engagement_model_data.age > 28) & (df_engagement_model_data.age <= 47)].age
    df_engagement_model_data['d2_AGE_O'] = np.where(df_engagement_model_data['d2_AGE_O'].isna(),0,1)

    df_engagement_model_data['d3_AGE_O'] = df_engagement_model_data[(df_engagement_model_data.age > 47) & (df_engagement_model_data.age <= 59)].age
    df_engagement_model_data['d3_AGE_O'] = np.where(df_engagement_model_data['d3_AGE_O'].isna(),0,1)

    #Black and Asian Data Preparation

    df_engagement_model_data['d2_PER_BLACK'] = df_engagement_model_data[(df_engagement_model_data.per_black > 0.47) & (df_engagement_model_data.per_black <= 1.4)].per_black
    df_engagement_model_data['d2_PER_BLACK'] = np.where(df_engagement_model_data['d2_PER_BLACK'].isna(),0,1)

    df_engagement_model_data['d3_PER_ASIAN'] = df_engagement_model_data[(df_engagement_model_data.per_asian > 1.12) & (df_engagement_model_data.per_asian <= 3.03)].per_asian
    df_engagement_model_data['d3_PER_ASIAN'] = np.where(df_engagement_model_data['d3_PER_ASIAN'].isna(),0,1)


    #Estimated Population

    df_engagement_model_data['d3_Estimate'] = df_engagement_model_data[(df_engagement_model_data.Estimate__population > 16396) & (df_engagement_model_data.Estimate__population <= 30646)].Estimate__population
    df_engagement_model_data['d3_Estimate'] = np.where(df_engagement_model_data['d3_Estimate'].isna(),0,1)

    df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE'] = df_engagement_model_data[(df_engagement_model_data.per_not_in_labor_force <= 17.22)].per_not_in_labor_force
    df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE'] = np.where(df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE'].isna(),0,1)


    df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT'] = df_engagement_model_data[(df_engagement_model_data.per_ins_19_64_worked_lt_ft <= 80.5)].per_ins_19_64_worked_lt_ft
    df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT'] = np.where(df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT'].isna(),0,1)

    df_engagement_model_data['d1_PER_WORKED_FT'] = df_engagement_model_data[(df_engagement_model_data.per_worked_ft <= 58.96)].per_worked_ft
    df_engagement_model_data['d1_PER_WORKED_FT'] = np.where(df_engagement_model_data['d1_PER_WORKED_FT'].isna(),0,1)

    df_engagement_model_data['d1_PER_WITH_DISABILITY'] = df_engagement_model_data[(df_engagement_model_data.per_with_disability <= 9.28)].per_with_disability
    df_engagement_model_data['d1_PER_WITH_DISABILITY'] = np.where(df_engagement_model_data['d1_PER_WITH_DISABILITY'].isna(),0,1)

    #Household Inome data Preparation

    df_engagement_model_data['d1_HHINC_25K_TO_50K'] = df_engagement_model_data[(df_engagement_model_data.hinc_25k_to_50k <= 9.86)].hinc_25k_to_50k
    df_engagement_model_data['d1_HHINC_25K_TO_50K'] = np.where(df_engagement_model_data['d1_HHINC_25K_TO_50K'].isna(),0,1)

    df_engagement_model_data['d2_HHINC_25K_TO_50K'] = df_engagement_model_data[(df_engagement_model_data.hinc_25k_to_50k > 9.86) & (df_engagement_model_data.hinc_25k_to_50k <= 17.16)].hinc_25k_to_50k
    df_engagement_model_data['d2_HHINC_25K_TO_50K'] = np.where(df_engagement_model_data['d2_HHINC_25K_TO_50K'].isna(),0,1)

    df_engagement_model_data['d3_HHINC_25K_TO_50K'] = df_engagement_model_data[(df_engagement_model_data.hinc_25k_to_50k > 17.16) & (df_engagement_model_data.hinc_25k_to_50k <= 22.96)].hinc_25k_to_50k
    df_engagement_model_data['d3_HHINC_25K_TO_50K'] = np.where(df_engagement_model_data['d3_HHINC_25K_TO_50K'].isna(),0,1)

    df_engagement_model_data['d2_HHINC_50_TO_75K'] = df_engagement_model_data[(df_engagement_model_data.hinc_50k_to_75k > 12.32) & (df_engagement_model_data.hinc_50k_to_75k <= 17.74)].hinc_50k_to_75k
    df_engagement_model_data['d2_HHINC_50_TO_75K'] = np.where(df_engagement_model_data['d2_HHINC_50_TO_75K'].isna(),0,1)

    df_engagement_model_data['d3_HHINC_50_TO_75K'] = df_engagement_model_data[(df_engagement_model_data.hinc_50k_to_75k > 17.74) & (df_engagement_model_data.hinc_50k_to_75k <= 24.25)].hinc_50k_to_75k
    df_engagement_model_data['d3_HHINC_50_TO_75K'] = np.where(df_engagement_model_data['d3_HHINC_50_TO_75K'].isna(),0,1)

    df_engagement_model_data['d1_HHINC_BELOW_25K'] = df_engagement_model_data[(df_engagement_model_data.hinc_below_25k <= 4.91)].hinc_below_25k
    df_engagement_model_data['d1_HHINC_BELOW_25K'] = np.where(df_engagement_model_data['d1_HHINC_BELOW_25K'].isna(),0,1)

    df_engagement_model_data['d2_HHINC_BELOW_25K'] = df_engagement_model_data[(df_engagement_model_data.hinc_below_25k > 4.91) & (df_engagement_model_data.hinc_below_25k <= 11.48)].hinc_below_25k
    df_engagement_model_data['d2_HHINC_BELOW_25K'] = np.where(df_engagement_model_data['d2_HHINC_BELOW_25K'].isna(),0,1)


    Contract_Type = 'FF & Near Site'

    if Contract_Type == 'FF & Near Site':
        df_engagement_model_data['d1_Contract_Type'] = 1
        df_engagement_model_data['d2_Contract_Type'] = 0
        df_engagement_model_data['d4_Contract_Type'] = 0
        df_engagement_model_data['score'] = -0.6923-0.1696*df_engagement_model_data['d1_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-1.1351*df_engagement_model_data['d2_REGION']+0.2374*df_engagement_model_data['d3_REGION']-0.4876*df_engagement_model_data['d1_AGE_O']+0.2411*df_engagement_model_data['d2_AGE_O']+0.2971*df_engagement_model_data['d3_AGE_O']-0.117*df_engagement_model_data['d2_PER_BLACK']-0.1393*df_engagement_model_data['d3_PER_ASIAN']+0.0638*df_engagement_model_data['d3_Estimate']+0.2138*df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE']-0.1564*df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT']-0.3065*df_engagement_model_data['d1_PER_WORKED_FT']-0.1627*df_engagement_model_data['d1_PER_WITH_DISABILITY']-0.1854*df_engagement_model_data['d1_HHINC_25K_TO_50K']-0.1286*df_engagement_model_data['d2_HHINC_25K_TO_50K']-0.068*df_engagement_model_data['d3_HHINC_25K_TO_50K']+0.1218*df_engagement_model_data['d2_HHINC_50_TO_75K']+0.2493*df_engagement_model_data['d3_HHINC_50_TO_75K']+0.2997*df_engagement_model_data['d1_HHINC_BELOW_25K']+0.134*df_engagement_model_data['d2_HHINC_BELOW_25K']--0.4972*df_engagement_model_data['d1_Contract_Type']+0.3927*df_engagement_model_data['d2_Contract_Type']+0.335*df_engagement_model_data['d4_Contract_Type']
    elif Contract_Type == 'FF & On Site':
        df_engagement_model_data['d1_Contract_Type'] = 0
        df_engagement_model_data['d2_Contract_Type'] = 1
        df_engagement_model_data['d4_Contract_Type'] = 0
        df_engagement_model_data['score'] = -0.6923-0.1696*df_engagement_model_data['d1_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-1.1351*df_engagement_model_data['d2_REGION']+0.2374*df_engagement_model_data['d3_REGION']-0.4876*df_engagement_model_data['d1_AGE_O']+0.2411*df_engagement_model_data['d2_AGE_O']+0.2971*df_engagement_model_data['d3_AGE_O']-0.117*df_engagement_model_data['d2_PER_BLACK']-0.1393*df_engagement_model_data['d3_PER_ASIAN']+0.0638*df_engagement_model_data['d3_Estimate']+0.2138*df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE']-0.1564*df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT']-0.3065*df_engagement_model_data['d1_PER_WORKED_FT']-0.1627*df_engagement_model_data['d1_PER_WITH_DISABILITY']-0.1854*df_engagement_model_data['d1_HHINC_25K_TO_50K']-0.1286*df_engagement_model_data['d2_HHINC_25K_TO_50K']-0.068*df_engagement_model_data['d3_HHINC_25K_TO_50K']+0.1218*df_engagement_model_data['d2_HHINC_50_TO_75K']+0.2493*df_engagement_model_data['d3_HHINC_50_TO_75K']+0.2997*df_engagement_model_data['d1_HHINC_BELOW_25K']+0.134*df_engagement_model_data['d2_HHINC_BELOW_25K']--0.4972*df_engagement_model_data['d1_Contract_Type']+0.3927*df_engagement_model_data['d2_Contract_Type']+0.335*df_engagement_model_data['d4_Contract_Type']
    elif Contract_Type == 'PEPM & On Site':
        df_engagement_model_data['d1_Contract_Type'] = 0
        df_engagement_model_data['d2_Contract_Type'] = 0
        df_engagement_model_data['d4_Contract_Type'] = 1
        df_engagement_model_data['score'] = -0.6923-0.1696*df_engagement_model_data['d1_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-1.1351*df_engagement_model_data['d2_REGION']+0.2374*df_engagement_model_data['d3_REGION']-0.4876*df_engagement_model_data['d1_AGE_O']+0.2411*df_engagement_model_data['d2_AGE_O']+0.2971*df_engagement_model_data['d3_AGE_O']-0.117*df_engagement_model_data['d2_PER_BLACK']-0.1393*df_engagement_model_data['d3_PER_ASIAN']+0.0638*df_engagement_model_data['d3_Estimate']+0.2138*df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE']-0.1564*df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT']-0.3065*df_engagement_model_data['d1_PER_WORKED_FT']-0.1627*df_engagement_model_data['d1_PER_WITH_DISABILITY']-0.1854*df_engagement_model_data['d1_HHINC_25K_TO_50K']-0.1286*df_engagement_model_data['d2_HHINC_25K_TO_50K']-0.068*df_engagement_model_data['d3_HHINC_25K_TO_50K']+0.1218*df_engagement_model_data['d2_HHINC_50_TO_75K']+0.2493*df_engagement_model_data['d3_HHINC_50_TO_75K']+0.2997*df_engagement_model_data['d1_HHINC_BELOW_25K']+0.134*df_engagement_model_data['d2_HHINC_BELOW_25K']--0.4972*df_engagement_model_data['d1_Contract_Type']+0.3927*df_engagement_model_data['d2_Contract_Type']+0.335*df_engagement_model_data['d4_Contract_Type']
    else:
        df_engagement_model_data['d1_Contract_Type'] = 0
        df_engagement_model_data['d2_Contract_Type'] = 0
        df_engagement_model_data['d4_Contract_Type'] = 0
        df_engagement_model_data['score'] = -0.6923-0.1696*df_engagement_model_data['d1_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-1.1351*df_engagement_model_data['d2_REGION']+0.2374*df_engagement_model_data['d3_REGION']-0.4876*df_engagement_model_data['d1_AGE_O']+0.2411*df_engagement_model_data['d2_AGE_O']+0.2971*df_engagement_model_data['d3_AGE_O']-0.117*df_engagement_model_data['d2_PER_BLACK']-0.1393*df_engagement_model_data['d3_PER_ASIAN']+0.0638*df_engagement_model_data['d3_Estimate']+0.2138*df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE']-0.1564*df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT']-0.3065*df_engagement_model_data['d1_PER_WORKED_FT']-0.1627*df_engagement_model_data['d1_PER_WITH_DISABILITY']-0.1854*df_engagement_model_data['d1_HHINC_25K_TO_50K']-0.1286*df_engagement_model_data['d2_HHINC_25K_TO_50K']-0.068*df_engagement_model_data['d3_HHINC_25K_TO_50K']+0.1218*df_engagement_model_data['d2_HHINC_50_TO_75K']+0.2493*df_engagement_model_data['d3_HHINC_50_TO_75K']+0.2997*df_engagement_model_data['d1_HHINC_BELOW_25K']+0.134*df_engagement_model_data['d2_HHINC_BELOW_25K']--0.4972*df_engagement_model_data['d1_Contract_Type']+0.3927*df_engagement_model_data['d2_Contract_Type']+0.335*df_engagement_model_data['d4_Contract_Type']



    #-0.4972*df_engagement_model_data['d1_Contract_Type']+0.3927*df_engagement_model_data['d2_Contract_Type']+0.335*df_engagement_model_data['d4_Contract_Type']


    probab = []

    scores = df_engagement_model_data['score']

    for s in scores:
        probb = math.exp(-s)/(1+math.exp(-s))
        probab.append(probb)


    df_engagement_model_data['probability_eng'] = probab

    return(df_engagement_model_data)


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
#     df = pd.read_csv('NPS_SF_June2022_final.csv')
#     # for i in range(1,df.shape[0]):
#     #     REVIEW_ID = list(df['ID'])[i],
#     #     MEMBER_ID = list(df['MEMBER_ID'])[i],
#     #     NPSCLINIC = list(df['NPSCLINIC__C'])[i],
#     #     SURVEYDATE = list(df['SURVEYDATE__C'])[i],
#     #     SURVEY_MONTH = list(df['SURVEY_MONTH'])[i],
#     #     SURVEY_YEAR = list(df['SURVEY_YEAR'])[i],
#     #     SURVEYNUMBER = list(df['SURVEYNUMBER__C'])[i],
#     #     NPS = list(df['NPS'])[i],
#     #     REASONNPSSCORE = list(df['REASONNPSSCORE__C'])[i],
#     #     WHATDIDWELLWITHAPP = list(df['WHATDIDWELLWITHAPP__C'])[i],
#     #     WHATDIDNOTWELLWITHAPP = list(df['WHATDIDNOTWELLWITHAPP__C'])[i],
#     #     HOUSEHOLD_ID = list(df['HOUSEHOLD_ID'])[i],
#     #     MEMBER_CITY = list(df['MEMBER_CITY'])[i],
#     #     MEMBER_STATE = list(df['MEMBER_STATE'])[i],
#     #     MEMBER_ZIP = list(df['MEMBER_ZIP'])[i],
#     #     CLINIC_ID = list(df['CLINIC_ID'])[i],
#     #     CLINIC_STREET = list(df['CLINIC_STREET'])[i],
#     #     CLINIC_CITY = list(df['CLINIC_CITY'])[i],
#     #     CLINIC_STATE = list(df['CLINIC_STATE'])[i],
#     #     CLINIC_ZIP = list(df['CLINIC_ZIP'])[i],
#     #     CLINIC_TYPE = list(df['CLINIC_TYPE'])[i],
#     #     PROVIDER_NAME = list(df['PROVIDER_NAME'])[i],
#     #     PROVIDERTYPE = list(df['PROVIDERTYPE__C'])[i],
#     #     PROVIDER_CATEGORY = list(df['PROVIDER_CATEGORY__C'])[i],
#     #     CLIENT_ID = list(df['CLIENT_ID'])[i],
#     #     CLIENT_NAICS = list(df['CLIENT_NAICS'])[i],
#     #     sentiment_label = list(df['sentiment_label'])[i],
#     #     nps_label = list(df['nps_label'])[i],
#     #     CLIENT_NAME = list(df['CLIENT NAME'])[i],
#     #     PARENT_CLIENT_NAME = list(df['PARENT CLIENT NAME'])[i],
#     #     PARENT_CLIENT_ID = list(df['PARENT_CLIENT_ID'])[i],
#     #     TIMESTAMP = time.mktime(datetime.datetime.strptime(list(df['SURVEYDATE__C'])[i],"%d-%m-%Y").timetuple())
#     c = 0
#     for i in range(0,df.shape[0]):
#         print(i)
#         try:
#             everside_nps.objects.get(REVIEW_ID = list(df['ID'])[i])
#         except:
#             c = c + 1
#             data = everside_nps(
#             REVIEW_ID = list(df['ID'])[i],
#             MEMBER_ID = list(df['MEMBER_ID'])[i],
#             NPSCLINIC = list(df['NPSCLINIC__C'])[i],
#             SURVEYDATE = list(df['SURVEYDATE__C'])[i],
#             SURVEY_MONTH = list(df['SURVEY_MONTH'])[i],
#             SURVEY_YEAR = list(df['SURVEY_YEAR'])[i],
#             SURVEYNUMBER = list(df['SURVEYNUMBER__C'])[i],
#             NPS = list(df['NPS'])[i],
#             REASONNPSSCORE = list(df['REASONNPSSCORE__C'])[i],
#             WHATDIDWELLWITHAPP = list(df['WHATDIDWELLWITHAPP__C'])[i],
#             WHATDIDNOTWELLWITHAPP = list(df['WHATDIDNOTWELLWITHAPP__C'])[i],
#             HOUSEHOLD_ID = list(df['HOUSEHOLD_ID'])[i],
#             MEMBER_CITY = list(df['MEMBER_CITY'])[i],
#             MEMBER_STATE = list(df['MEMBER_STATE'])[i],
#             MEMBER_ZIP = list(df['MEMBER_ZIP'])[i],
#             CLINIC_ID = list(df['CLINIC_ID'])[i],
#             CLINIC_STREET = list(df['CLINIC_STREET'])[i],
#             CLINIC_CITY = list(df['CLINIC_CITY'])[i],
#             CLINIC_STATE = list(df['CLINIC_STATE'])[i],
#             CLINIC_ZIP = list(df['CLINIC_ZIP'])[i],
#             CLINIC_TYPE = list(df['CLINIC_TYPE'])[i],
#             PROVIDER_NAME = list(df['PROVIDER_NAME'])[i],
#             PROVIDERTYPE = list(df['PROVIDERTYPE__C'])[i],
#             PROVIDER_CATEGORY = list(df['PROVIDER_CATEGORY__C'])[i],
#             CLIENT_ID = list(df['CLIENT_ID'])[i],
#             CLIENT_NAICS = list(df['CLIENT_NAICS'])[i],
#             sentiment_label = list(df['sentiment_label'])[i],
#             nps_label = list(df['nps_label'])[i],
#             CLIENT_NAME = list(df['CLIENT NAME'])[i],
#             PARENT_CLIENT_NAME = list(df['PARENT CLIENT NAME'])[i],
#             PARENT_CLIENT_ID = list(df['PARENT_CLIENT_ID'])[i],
#             TIMESTAMP = time.mktime(datetime.datetime.strptime(list(df['SURVEYDATE__C'])[i],"%d-%m-%Y").timetuple())
#             )
#             data.save()
#         # print('REVIEW_ID : ',REVIEW_ID[0],'\n',
#         # 'MEMBER_ID : ',MEMBER_ID[0],'\n',
#         # 'NPSCLINIC : ',NPSCLINIC[0],'\n',
#         # 'SURVEYDATE : ',SURVEYDATE[0],'\n',
#         # 'SURVEY_MONTH : ',SURVEY_MONTH[0],'\n',
#         # 'SURVEY_YEAR : ',SURVEY_YEAR[0],'\n',
#         # 'SURVEYNUMBER : ',SURVEYNUMBER[0],'\n',
#         # 'NPS : ',NPS[0],'\n',
#         # 'REASONNPSSCORE : ',REASONNPSSCORE[0],'\n',
#         # 'WHATDIDWELLWITHAPP : ',WHATDIDWELLWITHAPP[0],'\n',
#         # 'WHATDIDNOTWELLWITHAPP : ',WHATDIDNOTWELLWITHAPP[0],'\n',
#         # 'HOUSEHOLD_ID : ',HOUSEHOLD_ID[0],'\n',
#         # 'MEMBER_CITY : ',MEMBER_CITY[0],'\n',
#         # 'MEMBER_STATE : ',MEMBER_STATE[0],'\n',
#         # 'MEMBER_ZIP : ',MEMBER_ZIP[0],'\n',
#         # 'CLINIC_ID : ',CLINIC_ID[0],'\n',
#         # 'CLINIC_STREET : ',CLINIC_STREET[0],'\n',
#         # 'CLINIC_CITY : ',CLINIC_CITY[0],'\n',
#         # 'CLINIC_STATE : ',CLINIC_STATE[0],'\n',
#         # 'CLINIC_ZIP : ',CLINIC_ZIP[0],'\n',
#         # 'CLINIC_TYPE : ',CLINIC_TYPE[0],'\n',
#         # 'PROVIDER_NAME : ',PROVIDER_NAME[0],'\n',
#         # 'PROVIDERTYPE : ',PROVIDERTYPE[0],'\n',
#         # 'PROVIDER_CATEGORY : ',PROVIDER_CATEGORY[0],'\n',
#         # 'CLIENT_ID : ',CLIENT_ID[0],'\n',
#         # 'CLIENT_NAICS : ',CLIENT_NAICS[0],'\n',
#         # 'sentiment_label : ',sentiment_label[0],'\n',
#         # 'nps_label : ',nps_label[0],'\n',
#         # 'CLIENT_NAME : ',CLIENT_NAME[0],'\n',
#         # 'PARENT_CLIENT_NAME : ',PARENT_CLIENT_NAME[0],'\n',
#         # 'PARENT_CLIENT_ID : ',PARENT_CLIENT_ID[0],'\n',
#         # 'TIMESTAMP : ',TIMESTAMP)
#         # print(i)
#         # break
#     print('\n',c,'\n')
#     df = pd.read_csv('regionState.csv')
#     df = df.dropna(subset=['State'])
#     df.drop(df[df['State'] == 'Unknown'].index, inplace = True)
#     print('\nshape :',df.shape[0])
#     for i in range(df.shape[0]):
#         print(i)
#         everside_nps.objects.filter(CLINIC_STATE=list(df['State'])[i]).update(REGION=list(df['Region'])[i])
#     everside_nps.objects.filter(REGION = ' ').update(REGION = 'nan')
#     everside_nps.objects.filter(REGION = 'nan').update(REGION = 'unknown')
#     everside_nps.objects.filter(REGION = 'West  ').update(REGION = 'West')
#     return HttpResponse('Hello')




#------------------------------------------
# def index(request):
#     df = pd.read_csv('regionState.csv')
#     df = df.dropna(subset=['State'])
#     df.drop(df[df['State'] == 'Unknown'].index, inplace = True)
#     for i in range(df.shape[0]):
#         print(i)
#         everside_nps.objects.filter(CLINIC_STATE=list(df['State'])[i]).update(REGION=list(df['Region'])[i])
#     return HttpResponse('Hello')
#-------------------------------------------------------

 


# def index(request):
#     everside_nps.objects.filter(REGION = ' ').update(REGION = 'nan')
#     return HttpResponse('hello')

#---------------------------------------------------


# def index(request):
#     FIRST_NAME = 'Tabitha'
#     LAST_NAME = 'Rizzio'
#     USERNAME = 'tabithaeko'
#     EMAIL = 'tabitha.rizzio@eversidehealth.com'
#     PASS = '12345678'
#     USER_TYPE = '0'
    
#     PASSWORD = make_password(PASS)
#     TOKEN = make_password(USERNAME+PASS)
#     data = user_data(
#                     FIRST_NAME = FIRST_NAME,
#                     LAST_NAME = LAST_NAME,
#                     USERNAME = USERNAME,
#                     EMAIL = EMAIL,
#                     USER_TYPE = USER_TYPE,
#                     PASSWORD = PASSWORD,
#                     TOKEN    = TOKEN,
#     )
#     data.save()   
#     return HttpResponse('Hello')



# @api_view(['POST'])
# @parser_classes([MultiPartParser,FormParser])
# def egMemberPercentile_old(request,format=None):    
#     try:
#         try:
#             file_name = str((request.data)['username'])+'.csv'
#             name = 'uploads/engagement_files/'+file_name
#         except:
#             return Response({'Message':'FALSE','Error':'Username Invalid'})
#         file_list = os.listdir('uploads/engagement_files')
#         if file_name in file_list:
#             try:
#                 up_file = request.FILES.getlist('file')
#                 df = pd.read_csv(up_file[0])
#                 df['ZIP'] =  pd.to_numeric(df['ZIP'],errors='coerce')
#                 zip_df = pd.read_csv('zip_lat_long.csv')
#                 df = pd.merge(df,zip_df,on='ZIP',how='left')
#                 if 'probability' in list(df.columns):
#                     return Response({'Message':'FALSE','Error':'Invalid File1'})
#                 prob_func(df)
#                 try:
#                     prob_func(df)
#                 except:
#                     return Response({'Message':'FALSE','Error':'Invalid File2'})
#                 df.to_csv(name,index = False)
#                 engagement_file_data.objects.filter(USERNAME = str((request.data)['username'])).delete()
#                 data = engagement_file_data(USERNAME = str((request.data)['username']),
#                                             FILE_NAME = str(up_file[0]),
#                                             FILE_SIZE = (up_file[0]).size)
#                 data.save()
#             except:
#                 df = pd.read_csv(name) 
#                 df['ZIP'] =  pd.to_numeric(df['ZIP'],errors='coerce') 
#                 zip_df = pd.read_csv('zip_lat_long.csv')
#                 # df = pd.merge(df,zip_df,on='ZIP',how='left')
        
#         else:
#             up_file = request.FILES.getlist('file')
#             df = pd.read_csv(up_file[0])
#             df['ZIP'] =  pd.to_numeric(df['ZIP'],errors='coerce')
#             zip_df = pd.read_csv('zip_lat_long.csv')
#             df = pd.merge(df,zip_df,on='ZIP',how='left')
#             ndf = df[['GENDER','AGE','CLIENT_ID','MEMBER_ID','CLIENT_ENROLL_CONTRACT_TYP']]
#             if 'probability' in list(df.columns):
#                 return Response({'Message':'FALSE','Error':'Invalid File'})
#             try:
#                 prob_func(df)
#             except:
#                 return Response({'Message':'FALSE','Error':'except'})
#             df.to_csv(name,index = False)
#             engagement_file_data.objects.filter(USERNAME = str((request.data)['username'])).delete()
#             data = engagement_file_data(USERNAME = str((request.data)['username']),
#                                         FILE_NAME = str(up_file[0]),
#                                         FILE_SIZE = (up_file[0]).size)
#             data.save()
#         out = prob_func(df)
#         out_prob = list(out['probability'])
#         low = 0 # n < 0.5
#         med = 0 # 0.5 < n < 0.75
#         high = 0 # 0.75 < n
#         graph = [] 
#         p_values = [0,1,25,33,50,66,75,95,99,100]
#         for i in p_values:
#             p = np.percentile(out_prob,i)
#             percentile_name = "P"+str(i)
#             percentile_value = round(p,3)
#             member_score = out_prob.count(p)
#             if p < 0.5:
#                 low = low + 1
#             elif 0.5 <= p < 0.75:
#                 med = med + 1
#             else:
#                 high = high + 1

#             frame = {
#                 'percentile_name':percentile_name,
#                 'percentile_value':percentile_value,
#                 'member_score':member_score
#             }
#             graph.append(frame)
#             percentage = {
#                 'low':str(low*10)+"%",
#                 'medium':str(low*10+med*10)+"%",
#                 'high':'100%',
#             }
# #--------------------------------------Card Data----------------------------------------------------
#         rows = df.shape[0]
#         columns = df.shape[1]
#         client_count = len(set(list(df['CLIENT_ID'])))
#         member_count = len(set(list(df['MEMBER_ID'])))
#         try:
#             opt_in = list(df['CLIENT_ENROLL_CONTRACT_TYP']).count('Opt In')
#         except:
#             opt_in = 0
#         try:
#             flat_fee = list(df['CLIENT_ENROLL_CONTRACT_TYP']).count('Flat Fee')
#         except:
#             flat_fee = 0
#         try:
#             all_in_eligible = list(df['CLIENT_ENROLL_CONTRACT_TYP']).count('All-In-Eligible')
#         except:
#             all_in_eligible = 0
#         try:
#             near_site = list(df['CLIENT_DEF_HC_TYPE']).count('Near Site')
#         except:
#             near_site = 0
#         try:
#             on_site = list(df['CLIENT_DEF_HC_TYPE']).count('On Site')
#         except:
#             on_site = 0
#         cards_data = [
#                 {
#                     'name':'Rows',
#                     'value':rows
#                 },
#                 {
#                     'name':'Columns',
#                     'value':columns
#                 },
#                 {
#                     'name':'Clients',
#                     'value':client_count
#                 },
#                 {
#                     'name':'Members',
#                     'value':member_count
#                 },
#                 {
#                     'name':'Opt In',
#                     'value':opt_in
#                 },
#                 {
#                     'name':'Flat Fee',
#                     'value':flat_fee
#                 },
#                 {
#                     'name':'All In Eligible',
#                     'value':all_in_eligible
#                 },
#                 {
#                     'name':'Near Site',
#                     'value':near_site
#                 },
#                 {
#                     'name':'On Site',
#                     'value':on_site
#                 },
#         ]
# #-----------------------------------------Age Graph--------------------------------------------
#         group_list = [(0,12),(13,19),(20,29),(30,39),(40,49),(50,59),(60,69),(70,79),(80,89),(90,1000)]
#         age_list = list(df['AGE'])
#         age_graph = []
#         for i in group_list:
#             if(i[1]<90):  
#                 age_graph.append(
#                                 {
#                                     'groupName':str(i[0])+'-'+str(i[1]),
#                                     'groupValue': sum(map(age_list.count, range(i[0],i[1]+1)))

#                                 }) 
#             else:
#                   age_graph.append(
#                                 {
#                                     'groupName':str(i[0])+'+',
#                                     'groupValue': sum(map(age_list.count, range(i[0],i[1]+1)))

#                                 })         

# #---------------------------------------Gender Chart-----------------------------------------------------
#         gender_list = list(df['GENDER'])
#         gender_list = list(map(lambda x: x.lower(), gender_list))
#         try:
#             male_count = gender_list.count('male')
#         except:
#             male_count = 0
#         try:
#             female_count = gender_list.count('female')
#         except:
#             female_count = 0
#         try:
#             others_count = gender_list.count('others')
#         except:
#             others_count = 0
#         gender = {
#               'total_male':male_count,
#               'male':round((male_count/len(gender_list))*100,2),
#               'total_female':female_count,
#               'female':round((female_count/len(gender_list))*100,2),
#               'total_other':others_count,
#               'other': round((others_count/len(gender_list))*100,2),  
#         }
#         gender_pie = [{
#                         'label':'Male',
#                         'percentage': round((male_count/len(gender_list))*100,2),
#                         'color': '#39a0ed'
#                     },
#                     {
#                         'label':'Female',
#                         'percentage': round((female_count/len(gender_list))*100,2),
#                         'color': '#13c4a3'
#                     },
#                     {
#                         'label':'Other',
#                         'percentage': round((others_count/len(gender_list))*100,2),
#                         'color': '#d77a69'
#                     }]

#         #---------------------------------Map-------------------------------------------------------
#         state_codes = region_names()
#         zip_df = pd.read_csv('zip_lat_long.csv')
#         # ndf = df.drop_duplicates(subset='ZIP', keep="last")
#         # lat_long_df = pd.merge(ndf,zip_df,how='left',on=['ZIP'])
#         lat_long_df = df
#         lat_long_df['Y'] = lat_long_df['Y'].fillna(0)
#         lat_long_df['X'] = lat_long_df['X'].fillna(0)
#         lat_long_df['ZIP'] = lat_long_df['ZIP'].fillna(0)

#         state = list(lat_long_df['STATE_ZIP'])
#         long = list(lat_long_df['Y'])
#         lat = list(lat_long_df['X'])
#         zip = list(lat_long_df['ZIP'])


#         map_data = []
#         for i in range(lat_long_df.shape[0]):
#             try:
#                 state_data = state_codes[state[i]]
#             except:
#                 state_data = state[i]
#             frame = {
#                     'state':str(state_data),
#                     'long':long[i],
#                     'lat':lat[i],
#                     'zip':str(zip[i]),
#                     'zip_count':(list(df['ZIP'])).count(zip[i])
#             }
#             map_data.append(frame)        
#         #---------------------------------File Name and Size-----------------------------------------
#         f_obj = engagement_file_data.objects.filter(USERNAME = str((request.data)['username'])).values()
#         #--------------------------------------------------------------------------------------------
#         df['REGION_ZIP'] = df['REGION_ZIP'].fillna('unknown')
#         regions = list(set(list(df['REGION_ZIP'])))
#         average_table = []
#         us_census = pd.read_csv('us_census_data.csv')
#         average_df = pd.merge(df,us_census,on='ZIP',how='left')
#         for i in regions:
#             frame = {}

#             ndf = average_df.loc[df['REGION_ZIP'] == i]
#             try:
#                 frame = {
#                     'region':i,
#                     '__Ethnic_White':str(np.nansum(np.array(list(ndf['__Ethnic_White'])))/(ndf.shape)[0]),
#                     'per_black':str(np.nansum(np.array(list(ndf['__Black_or_African_American_alone'])))/(ndf.shape)[0]),
#                     'per_asian':str(np.nansum(np.array(list(ndf['__Asian'])))/(ndf.shape)[0]),
#                     '__Hispanic_or_Latino':str(np.nansum(np.array(list(ndf['__Hispanic_or_Latino_(of_any_race)'])))/(ndf.shape)[0]),
#                     'Percent_Insured':str(np.nansum(np.array(list(ndf['Percent_Insured'])))/(ndf.shape)[0]),
#                     'PCP_Avail':str(np.nansum(np.array(list(ndf['PCP_Avail'])))/(ndf.shape)[0]),
#                 }
#                 average_table.append(frame)
#             except:
#                 print(i)
#         #------------------------Response------------------------------------------------------------
#         return Response({'Message':'TRUE',
#                          'file_name':(f_obj[0])['FILE_NAME'],
#                          'file_size':(f_obj[0])['FILE_SIZE'],
#                          'graph':graph,
#                          'percentage':percentage,
#                          'cards_data':cards_data,
#                          'age_graph':age_graph,
#                          'gender':gender,
#                          'gender_pie':gender_pie,
#                          'map_data':map_data,
#                          'lat_mid':np.nansum(np.array(lat))/len(lat),
#                          'long_mid':np.nansum(np.array(long))/len(long),
#                          'average_table':average_table,
#                          })
#         #------------------------------------------------------------------------------------------------
#     except:
#         return Response({'Message':"FALSE",'Error':'Invalid File main'})



# def index(request):
#     password = '1234'
#     PASSWORD1 = make_password(password)
#     user_data.objects.update(PASSWORD=PASSWORD1)
#     return HttpResponse('Hello')