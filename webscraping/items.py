# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
import unicodedata
from scrapy import Field, Item
from scrapy.loader.processors import MapCompose, Compose, TakeFirst, Join
from w3lib.html import remove_tags
import unicodedata

def remove_nt(value):
    return value.replace("\n",'').replace(":",'')

def filter_num(value):
    if value.isdigit():
        return value

def remove_text(value):
    return re.sub('For further information, please visit:', ' ',value)

class ShareItem(scrapy.Item):
    CompanyName = scrapy.Field()   
    Sector = scrapy.Field()
    SharesOutstanding	 = scrapy.Field()
    MarketPrice = scrapy.Field()
    PriceChange = scrapy.Field()
    EPS = scrapy.Field()
    PERatio = scrapy.Field()
    BookValue = scrapy.Field()
    CashDividend = scrapy.Field()
    BonusDividend = scrapy.Field()


class DemoProjectItem(scrapy.Item):
    
    CourseTitle = scrapy.Field()   
    
    Category = scrapy.Field()
    
    CourseWebsite = scrapy.Field()
    Duration = scrapy.Field()
    DurationTerm = scrapy.Field()
    
    DegreeLevel = scrapy.Field()
    IntakeDay = scrapy.Field()
    IntakeMonth = scrapy.Field()
    ApplyDay = scrapy.Field()
    ApplyMonth = scrapy.Field()
    City = scrapy.Field()
    InternationalFee = scrapy.Field()
    DomesticFee = scrapy.Field()
    FeeTerm = scrapy.Field()
    FeeYear = scrapy.Field()
    
    
    DomesticOnly = scrapy.Field()
    Currency = scrapy.Field()
    StudyMode = scrapy.Field()
    
    
    StudyLoad = scrapy.Field()
    
    IELTS_Listening = scrapy.Field()
    IELTS_Speaking = scrapy.Field()
    IELTS_Writing = scrapy.Field()
    IELTS_Reading = scrapy.Field()
    IELTS_Overall = scrapy.Field()
    
    PTE_Listening = scrapy.Field()
    PTE_Speaking = scrapy.Field()
    PTE_Writing = scrapy.Field()
    PTE_Reading = scrapy.Field()
    PTE_Overall = scrapy.Field()

    TOEFL_Listening = scrapy.Field()
    TOEFL_Speaking = scrapy.Field()
    TOEFL_Writing = scrapy.Field()
    TOEFL_Reading = scrapy.Field()   
    TOEFL_Overall = scrapy.Field()
    
    AcademicLevel = scrapy.Field()
    AcademicScore = scrapy.Field()
    ScoreType = scrapy.Field()
    AcademicCountry = scrapy.Field()
    OtherTest = scrapy.Field()
    Score = scrapy.Field()
    OtherRequirement = scrapy.Field()
    CourseDescription = scrapy.Field()
    CourseStructure = scrapy.Field()
    Career = scrapy.Field()
    
  
    
  
    
