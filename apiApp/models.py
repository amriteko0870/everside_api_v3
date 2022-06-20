from ast import mod
from django.db import models

# Create your models here.

class everside_nps(models.Model):
    REVIEW_ID = models.CharField(max_length=100)
    MEMBER_ID = models.CharField(max_length=100)
    NPSCLINIC = models.CharField(max_length=100)
    SURVEYDATE = models.CharField(max_length=100)
    SURVEY_MONTH = models.CharField(max_length=100)
    SURVEY_YEAR = models.CharField(max_length=100)
    SURVEYNUMBER = models.CharField(max_length=100)
    NPS = models.IntegerField()
    REASONNPSSCORE = models.CharField(max_length=100)
    WHATDIDWELLWITHAPP = models.CharField(max_length=100)
    WHATDIDNOTWELLWITHAPP = models.CharField(max_length=100)
    HOUSEHOLD_ID = models.CharField(max_length=100)
    MEMBER_CITY = models.CharField(max_length=100)
    MEMBER_STATE = models.CharField(max_length=100)
    MEMBER_ZIP = models.CharField(max_length=100)
    CLINIC_ID = models.CharField(max_length=100)
    CLINIC_STREET = models.CharField(max_length=100)
    CLINIC_CITY = models.CharField(max_length=100)
    CLINIC_STATE = models.CharField(max_length=100)
    CLINIC_ZIP = models.CharField(max_length=100)
    CLINIC_TYPE = models.CharField(max_length=100)
    PROVIDER_NAME = models.CharField(max_length=100)
    PROVIDERTYPE = models.CharField(max_length=100)
    PROVIDER_CATEGORY = models.CharField(max_length=100)
    CLIENT_ID = models.CharField(max_length=100)
    CLIENT_NAICS = models.CharField(max_length=100)
    sentiment_label = models.CharField(max_length=100)
    nps_label = models.CharField(max_length=100)
    CLIENT_NAME = models.CharField(max_length=100)
    PARENT_CLIENT_NAME = models.CharField(max_length=100)
    PARENT_CLIENT_ID = models.CharField(max_length=100)
    REGION = models.CharField(max_length=100,default=' ')
    TIMESTAMP = models.BigIntegerField()


class user_data(models.Model):
    FIRST_NAME = models.CharField(max_length=100)
    LAST_NAME = models.CharField(max_length=100)
    USERNAME = models.CharField(max_length=100,unique=True,null=False)
    EMAIL = models.EmailField(unique=True,null=False)
    PASSWORD = models.CharField(max_length=250)
    USER_TYPE = models.CharField(max_length=3)
    TOKEN = models.CharField(max_length=300,default='0')


class engagement_file_data(models.Model):
    USERNAME = models.CharField(max_length=100)
    FILE_NAME = models.CharField(max_length=100)
    FILE_SIZE = models.BigIntegerField()
