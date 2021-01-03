import scrapy
from scrapy.http import FormRequest
from main.models import arsProduct , seleniumpages


class ArsspiderSpider(scrapy.Spider):
    name = 'arsspider'
    allowed_domains = ['www.abayi.net']
    start_urls = ['http://www.abayi.net/']

    payload = {
    'cBayiKodu': '10217',
    'cKullaniciAdi': 'protech',
    'cParola': 'pro1234',
    }

    def start_requests(self,payload=payload):
        return [FormRequest("http://www.abayi.net", formdata=payload, callback=self.parse)]


    def parse(self, response):
        urls = response.xpath('//a[contains(@href, "UrunGrubu")]/@href').getall()

        for url in urls:
            yield response.follow(url, callback=self.parse_urungrups)

    def parse_urungrups(self,response):
        try:
            mevcutLink = seleniumpages.objects.get(url = response.request.url)
        except:
            mevcutLink = None

        pagination = response.xpath('//*[@id="AramaSonucu"]/div[4]/div/div[2]/div/ul/li').getall()

        if not mevcutLink:        
            if len(pagination) > 5 :
                selenlink = seleniumpages.objects.create(url = response.request.url)
                selenlink.save()
            else:
                urunpagelinks = response.xpath('//a[contains(@class, "arama-adi-h")]/@href').getall()
                for urunpagelink in urunpagelinks:
                    yield response.follow(urunpagelink, callback=self.parse_urun)
                
        
    def parse_urun(self, response):
        print("parseurun")
        try:
            mevcutUrun = arsProduct.objects.get(urunlink = response.request.url)
        except:
            mevcutUrun = None

        stokkod = response.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/ul/li[4]/span[3]/text()').get()
        birim = response.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/ul/li[3]/span[3]/text()').get()
        name =response.xpath('/html/body/div[3]/div[1]/div[1]/div/div[2]/h1/a/text()').get()
        stok = response.xpath('//html/body/div[3]/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[1]/table/tbody/tr/td[2]/text()').get()
        stok = "".join(stok.split())
        if stok == "Yok":
            stok = "0"
        if "+" in stok:
            stok = stok.replace("+","")
        stok = int(stok)
        print(stok , type(stok))
        
        fiyat =  response.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/ul/li[1]/span[3]/text()').get()
        fiyat = "".join(fiyat.split())
        if "." in fiyat:
            fiyat = fiyat.replace(".","")
        if "," in fiyat:
            fiyat = fiyat.replace(",",".")
        
        fiyat = float(fiyat[:-2])
        print(fiyat ,  type(fiyat))
        kdv = response.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/ul/li[2]/span[3]/text()').get()
        ozellik = response.xpath('//*[@id="Ozellikler"]/table').get()
        imglink = response.xpath('//*[@id="UrunResimleri"]/div/div/a/img/@src').get()
        anakategori = response.xpath('/html/body/div[3]/div[1]/div[1]/div/div[1]/div/ul/li[1]/a/text()').get()
        altkategori = response.xpath('/html/body/div[3]/div[1]/div[1]/div/div[1]/div/ul/li[2]/a/text()').get()
        sonkategori = response.xpath('/html/body/div[3]/div[1]/div[1]/div/div[1]/div/ul/li[3]/a/text()').get()
        if mevcutUrun:
            print(type(mevcutUrun.stok ) , type(mevcutUrun.fiyat))
            if mevcutUrun.stok != stok :
                mevcutUrun.stok = stok
                if stok == 0:
                    mevcutUrun.stokislem = "sil"
                else:
                    mevcutUrun.stokislem = 'stokguncelle'
            if mevcutUrun.fiyat != fiyat:
                mevcutUrun.fiyat = fiyat
                mevcutUrun.fiyatislem = 'fiyatguncelle'
            mevcutUrun.checkCount = mevcutUrun.checkCount +1
            mevcutUrun.save()
        else:
            print("namevcut")
        
            urun = {
                'urunlink':response.request.url,
                'stokkod':stokkod,
                'birim':birim,
                'name':name,
                'stok':stok,
                'fiyat':fiyat,
                'ozellik':ozellik,
                'imglink':imglink,
                'anakategori':anakategori,
                'altkategori':altkategori,
                'sonkategori':sonkategori,
       
            }
            
            yeniurun = arsProduct(**urun)
            yeniurun.save()