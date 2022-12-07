class FwMspider():
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
    def __init__(self):
        self.Data = []
        date = datetime.now().strftime('%Y%m%d')
        self.Path = f'fairway_market_{date}.csv'
        self.header = [
            'Product Number','Item name','Category','Unit Price','Unit',
            'Price','Sale Price','Serving Size','Serving Size Unit',
            'Calories','Total Fat (g)','Saturated Fat (g)','Trans Fat (g)',
            'Cholesterol (mg)','Sodium (mg)','Total Carbohydrate (g)',
            'Dietary Fiber (g)','Total Sugars (g)','Added Sugars (g)',
            'Protein (g)'
        ]



    def _getMain(self):
        data = [
            'https://www.fairwaymarket.com/sm/planning/rsid/4000/categories/produce-id-520691',
            'https://www.fairwaymarket.com/sm/planning/rsid/4000/categories/meat-id-520692',
            'https://www.fairwaymarket.com/sm/planning/rsid/4000/categories/dairy-id-520698',
            'https://www.fairwaymarket.com/sm/planning/rsid/4000/categories/seafood-id-520693',
        ]
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }
        self.ids = []
        for url in data:
            cageo = url.split('/')[-1].split('-id-')[0]
            res = httpx.get(url=url,headers=headers)
            if res.status_code == 200:
                print('Success...')
                dom = etree.HTML(res.text)
                self.ids.extend(list(map(lambda x:(cageo,x.split('-id-')[1]),dom.xpath('//div[@class="PillMenu--1g9je1p Hyqnv"]/div/a/@href'))))


    def getListPage(self):
        self.productIds = []
        if self.ids:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
            }

            for id_ in self.ids:
                page = 0
                while True:
                    page+=1
                    params = {
                        'take': '30',
                        'skip': str(30*(page-1)),
                        'page': str(page),
                    }
                    URL = 'https://storefrontgateway.brands.wakefern.com/api/stores/4000/categories/%s/search'%id_[1]
                    res = httpx.get(url=URL,headers=headers,params=params)
                    if res.status_code == 200:
                        result = res.json()
                        if result.get('items'):
                            self.productIds.extend(list(map(lambda x:(x['productId'],id_[0]),result.get('items'))))
                        else:
                            break
                    else:
                        print(res.status_code,res.text,headers,params,URL)
                        break
        else:
            print('No id fetched.')


    def parseData(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }
        if self.productIds:
            for id_ in self.productIds:
                res = httpx.get(url='https://storefrontgateway.brands.wakefern.com/api/stores/4000/products/%s'%id_[0],headers=headers)
                if res.status_code == 200:
                    result = res.json()
                    # ******************************************************************************************* #
                    Item_name = result.get('name')
                    if result.get('unitsOfSize'):
                        if result.get('unitsOfSize').get('type') and result.get('unitsOfSize').get('size'):
                            Item_name += ','+str(result.get('unitsOfSize').get('size'))+' '+result.get('unitsOfSize').get('type').upper()

                    Product_Number = id_[0]
                    Category = id_[1]

                    if result.get('unitPrice'):
                        try:
                            Unit_Price = re.findall('\$(.*?)/', result.get('unitPrice'))[0]
                            Unit = '$/' + result.get('unitPrice').split('/')[1]
                        except Exception:
                            Unit_Price = re.findall('\$(.*?)', result.get('unitPrice'))[0]
                            Unit = '$/' + result.get('unitPrice').split(' ')[1]

                    else:
                        Unit_Price = result.get('unitPrice')
                        Unit = None
                    if result.get('price'):
                        Price = result.get('price').replace('$','',-1)
                    else:
                        Price = None
                    if result.get('servingSize'):
                        ss = result.get('servingSize')
                        if ss.get('size') and ss.get('type'):
                            Serving_Size = ss.get('size')
                            Serving_Size_Unit = ss.get('type')
                        else:
                            Serving_Size = None
                            Serving_Size_Unit = None

                    else:
                        Serving_Size = None
                        Serving_Size_Unit = None

                    if result.get('nutritionProfiles'):
                        if result.get('nutritionProfiles').get('nutrition'):
                            ll = result.get('nutritionProfiles').get('nutrition')

                            Calories = ll.get('Calories')
                            if Calories:
                                Calories = Calories.get('size')

                            Total_Fat = ll.get('Total Fat')
                            if Total_Fat:
                                Total_Fat = Total_Fat.get('size')

                            Saturated_Fat = ll.get('Saturated Fat')
                            if Saturated_Fat:
                                Saturated_Fat = Saturated_Fat.get('size')

                            Trans_fat = ll.get('Trans fat')
                            if Trans_fat:
                                Trans_fat = Trans_fat.get('size')

                            Cholesterol = ll.get('Cholesterol')
                            if Cholesterol:
                                Cholesterol = Cholesterol.get('size')

                            Sodium = ll.get('Sodium')
                            if Sodium:
                                Sodium = Sodium.get('size')

                            Total_Carbohydrate = ll.get('Total Carbohydrate')
                            if Total_Carbohydrate:
                                Total_Carbohydrate = Total_Carbohydrate.get('size')

                            Dietary_Fiber = ll.get('Dietary Fiber')
                            if Dietary_Fiber:
                                Dietary_Fiber = Dietary_Fiber.get('size')

                            Total_Sugars = ll.get('Total Sugars')
                            if Total_Sugars:
                                Total_Sugars = Total_Sugars.get('size')

                            Added_Sugars = ll.get('Added Sugars')
                            if Added_Sugars:
                                Added_Sugars = Added_Sugars.get('size')

                            Protein = ll.get('Protein')
                            if Protein:
                                Protein = Protein.get('size')
                        else:
                            Calories = None
                            Total_Fat = None
                            Saturated_Fat = None
                            Trans_fat = None
                            Cholesterol = None
                            Sodium = None
                            Total_Carbohydrate = None
                            Dietary_Fiber = None
                            Total_Sugars = None
                            Added_Sugars = None
                            Protein = None

                    else:
                        Calories = None
                        Total_Fat = None
                        Saturated_Fat = None
                        Trans_fat = None
                        Cholesterol = None
                        Sodium = None
                        Total_Carbohydrate = None
                        Dietary_Fiber = None
                        Total_Sugars = None
                        Added_Sugars = None
                        Protein = None


                    Sale_Price = None

                    data = [Product_Number,Item_name,Category,Unit_Price,Unit,Price,Sale_Price,Serving_Size,Serving_Size_Unit,
                            Calories,Total_Fat,Saturated_Fat,Trans_fat,Cholesterol,Sodium,Total_Carbohydrate,Dietary_Fiber,
                            Total_Sugars,Added_Sugars,Protein]
                    self.Data.append(data)
                    print('Price data：',data)





                else:
                    print('Fail',res.text,res.status_code,id_[0])




        else:
            print('No item id fetched.')


    def Save(self):
        pd.DataFrame(self.Data).to_csv(self.Path,header=self.header,index=False,encoding='utf-8')
        print('Saved successfully.')


import re
import httpx
from lxml import etree
import pandas as pd
from datetime import datetime

if __name__ == '__main__':
    '''
        1、Fetch main page
        2、Fetch sub page
        3、Fetch detail page    
    '''
    with FwMspider() as f:
        f._getMain()
        f.getListPage()
        f.parseData()
        f.Save()



