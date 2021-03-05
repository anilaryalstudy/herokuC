import scrapy
import re
from webscraping.items import DemoProjectItem

from urllib.parse import urljoin
import time



class ProductsSpider(scrapy.Spider):
    name = "Yukon"

    def start_requests(self):
        url='https://www.yukonu.ca/programs/all'    
        yield scrapy.Request(url=url, callback=self.parse1)

    def parse1(self, response):
        x=response.xpath("//div[@class='view-content']//a/@href").extract()
        for p in x:
            url = urljoin(response.url, p)
            yield scrapy.Request(url, callback=self.parse_link1)
    
    
    def parse_link1(self, response):

        item = DemoProjectItem()
        item['CourseWebsite']=response.url
        item['CourseTitle']=response.xpath("//h1/span/text()").extract_first()
        if item['CourseTitle'] is None:
            item['CourseTitle']=response.xpath("//h2/span/text()").extract_first()

        try:
            IM=" ".join(response.xpath("//h3[contains(text(),'Start')]/following-sibling::*[1]/text()").extract()).lower()
            IM1=re.findall('september|october|march|january|february|april|may|june|july|august|november|december',str(IM))
            if IM1:
                item['IntakeMonth']=','.join(map(str.capitalize,set(IM1)))
        except:
            pass
        try:
            D=" ".join(response.xpath("//h3[contains(text(),'Program length')]/following-sibling::*[1]/text()").extract()).lower()

            durationinformation=D.replace("-"," - ").replace("one",'1').replace("two",'2').replace("four",'4').replace("three",'3').replace('five','5').replace(" - ",'-').replace(" to ",'-').replace(" or ",'-').replace("-"," ")
            durationdigits = re.findall(r'[\d]+ |[\d]+-[\d]+',str(durationinformation))[0].strip()
            durationterm = re.findall(durationdigits+" ([a-z]+)",durationinformation)[0]

            item['Duration']=durationdigits
            item['DurationTerm']=durationterm
        except:
            pass

        try:
            D=" ".join(response.xpath("//h3[contains(text(),'Start')]/parent::*[1]").extract()).lower()
            item['StudyLoad']="Both" if D.find("part")!=-1 and D.find("full")!=-1 else ("Full Time" if D.find("full")!=-1 else ("Part Time" if D.find("part")!=-1 else ("Both" if D.find("flexible")!=-1 else "")))
        except:
            pass



        item['Career']=response.xpath("//*[contains(text(),'Career opportunities ')]/following::*[1]").extract()
        item['CourseDescription']=response.xpath("//*[contains(text(),'Program description')]/following::*[1]").extract()
        item['OtherRequirement']=response.xpath("//*[contains(text(),'Admission requirements')]/following::*[1]").extract()
        item['CourseStructure']=response.xpath("//h2[contains(text(),'Courses')]/following::*[1]").extract()


        return item