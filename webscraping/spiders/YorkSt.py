import scrapy
import re
from webscraping.items import DemoProjectItem

from urllib.parse import urljoin
import time



class ProductsSpider(scrapy.Spider):
    name = "YorkStJohnUniversity"

    def start_requests(self):
        url='https://www.yorksj.ac.uk/courses/'    
        yield scrapy.Request(url=url, callback=self.parse1)

    def parse1(self, response):
        x=response.xpath("//div[@class='fb-results clearfix']//h2/a/@href").extract()
        for p in x:
            url = urljoin(response.url, p)
            yield scrapy.Request(url, callback=self.parse_link1)
        
        next_page = response.xpath("//*[@rel='next']/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse1)
        

    def parse_link1(self, response):
        
        item = DemoProjectItem()

        if response.url.find("short-courses")!=-1:
            return None
        else:

            try:
                url=response.url
                if url.find("undergraduate")!=-1:
                    item['DegreeLevel']="Undergraduate"
                elif url.find("postgraduate")!=-1:
                    item['DegreeLevel']="Postgraduate"
                else:
                    item['DegreeLevel']=""
            except:
                pass

            item['CourseWebsite']=response.url

            item['CourseTitle']=response.xpath("//h1/*/text()").extract_first().strip()

            item['City']=response.xpath("//*[@class='location-marker']//span/text()").extract_first().replace("Online","")

            if item['City']=="Online":
                item['StudyMode']="Online"
            


            try:
                SL=response.xpath("((//strong[contains(text(),'Duration')])[1]/parent::*[1]/text())[2]").extract_first().lower()
                durationinformation=SL.replace("one",'1').replace("two",'2').replace("four",'4').replace("three",'3').replace('five','5').replace(" - ",'-').replace(" to ",'-').replace(" or ",'-')
                durationdigits = re.findall(r'[\d]+ |[\d]+-[\d]+',str(durationinformation))[0].strip()
                durationterm = re.findall(durationdigits+" ([a-z]+)",durationinformation)[0]
                
                
                item['StudyLoad']="Both" if SL.find("full")!=-1 and SL.find("part")!=-1 else ("Full Time" if SL.find("full")!=-1 else ("Part Time" if SL.find("part")!=-1 else ""))
                item['Duration']=durationdigits
                item['DurationTerm']=durationterm

            except:
                pass

            try:
                DF=response.xpath("(//*[contains(text(),'UK and EU 2021 entry')])[1]/following::*[1]/text() | (//*[contains(text(),'UK and EU')])[1]/following::*[1]/text()").extract()
                for i in DF:
                    item['DomesticFee']=re.findall('£([\d+]+,[\d]+)|£([\d+]+)', i)[0]
                    item['Currency']="GBP"
                    item['FeeTerm']="Annual"
                    item['FeeYear']="2021"

                IF=response.xpath("(//*[contains(text(),'International 2021 entry')])[1]/following::*[1]/text() | (//*[contains(text(),'International')])[1]/following::*[1]/text() | (//*[contains(text(),'International 2020')])[1]/following::*[1]/text()").extract()
                for i in IF:
                    item['InternationalFee']=re.findall('£([\d+]+,[\d]+)|£([\d+]+)', i)[0]
                    item['Currency']="GBP"
                    item['FeeTerm']="Annual"
                    item['FeeYear']="2021"
            except:
                pass
                
            

           
            try:
                z=response.xpath("(//*[contains(text(),'IELTS')])[1]/text()").extract_first()
                z1=[float(s) for s in re.findall(r'-?\d+\.?\d*', z)]
                if len(z1)==1:
                    item['IELTS_Overall']=z1[0]
                    
                elif len(z1)==2:
                    item['IELTS_Overall']=z1[0]
                    item['IELTS_Listening']=item['IELTS_Speaking']=item['IELTS_Writing']=item['IELTS_Reading']=z1[1]
                elif len(z1)==3:
                    item['IELTS_Overall']=z1[0]
                    
                    item['IELTS_Listening']=item['IELTS_Speaking']=item['IELTS_Reading']=item['IELTS_Writing']=z1[1]
            except:
                pass

            item['IntakeMonth']=response.xpath("((//strong[contains(text(),'Start date')])[1]/parent::*[1]/text())[2]").extract_first().replace(" – ","").replace("2021","")

            item['CourseDescription']=response.xpath("//tab[@title='Course overview']/child::* | (//h2[contains(text(),'Course overview')])[1]/following-sibling::* | (//h2[contains(text(),'Course Overview')])[1]/following-sibling::*").extract()

            item['CourseStructure']=response.xpath("//tab[@title='Course structure']/child::* | (//h2[contains(text(),'Course Structure')])[1]/following-sibling::* | (//h2[contains(text(),'Course structure ')])[1]/following-sibling::*").extract()


            item['OtherRequirement']=response.xpath("//tab[@title='Entry Requirements']/child::*").extract()






        return item