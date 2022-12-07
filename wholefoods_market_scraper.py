class FwMspider():
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
    def __init__(self):
        self.Data = []
        date = datetime.now().strftime('%Y%m%d')
        self.Path = f'wholefoods_market_{date}.csv'
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
            'https://www.wholefoodsmarket.com/products/produce',
            'https://www.wholefoodsmarket.com/products/dairy-eggs',
            'https://www.wholefoodsmarket.com/products/meat',
            'https://www.wholefoodsmarket.com/products/seafood',
        ]
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        self.ids = []
        for url in data:
            cageo = url.split('/')[-1]
            res = httpx.get(url=url,headers=headers)
            if res.status_code == 200:
                print('Success...')
                temp = httpx.get(url='https://www.wholefoodsmarket.com/_next/data/gA_0Z8pXk88CJBarkJ90-/products/%(x)s.json?category=%(y)s'%{'x':cageo,'y':cageo}, headers=headers)
                if temp.status_code ==200:
                    total_items = temp.json().get('pageProps').get('data').get('meta').get('total').get('value')
                    self.ids.append(tuple([cageo,total_items]))


    def getListPage(self):
        self.productIds = []
        if self.ids:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
            }
            for id_ in self.ids:
                page = 0
                print(id_[0])
                while page <= math.ceil(id_[1] / 60):
                    page+=1
                    params = {
                        'limit': '60',
                        'offset': str(60*(page-1)),
                    }
                    URL = 'https://www.wholefoodsmarket.com/api/products/category/[leafCategory]?leafCategory=%s&store=10245'%id_[0]
                    res = httpx.get(url=URL,headers=headers,params=params)
                    if res.status_code == 200:
                        result = res.json()
                        if result.get('results'):
                            self.productIds.extend(map(lambda x: (x.get('slug'), id_[0]), result.get('results')))
                        else:
                            break
                    else:
                        print(res.status_code,res.text,headers,params,URL)
                        break
        else:
            print('No id fetched.')


    def parseData(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        if self.productIds:
            for id_ in self.productIds:
                res = httpx.get(url='https://www.wholefoodsmarket.com/_next/data/gA_0Z8pXk88CJBarkJ90-/product/%(x)s.json?store=10245&product-detail=%(y)s'%{'x':id_[0],'y':id_[0]},headers=headers)
                if res.status_code == 200:
                    result = res.json().get('pageProps').get('data')
                    # ******************************************************************************************* #
                    Item_name = result.get('name').split(',')[0]
                    if result.get('servingInfo'):
                        if result.get('servingInfo').get('totalSizeUom') and result.get('servingInfo').get('totalSize'):
                            Item_name += ','+str(result.get('servingInfo').get('totalSize'))+' '+result.get('servingInfo').get('totalSizeUom').upper()

                    Product_Number = result.get('id')
                    Category = id_[1]
                       
                    if result.get('regularPrice'):
                        Price = result.get('regularPrice')
                        if result.get('name'):
                            try:
                                Unit_Price = Price / int(result.get('servingInfo').get('totalSize'))
                                Unit = '$/' + result.get('servingInfo').get('totalSizeUom')
                            except Exception:
                                Unit_Price = None
                                Unit = None

                        else:
                            Unit_Price = None
                            Unit = None
                    else:
                        Price = None
                    
                        
                    if result.get('servingInfo'):
                        si = result.get('servingInfo')
                        if si.get('totalSizeUom') and si.get('totalSize'):
                            Serving_Size = si.get('totalSize')
                            Serving_Size_Unit = si.get('totalSizeUom')
                        else:
                            Serving_Size = None
                            Serving_Size_Unit = None

                    else:
                        Serving_Size = None
                        Serving_Size_Unit = None

                    if result.get('nutritionElements'):
                        ll = result.get('nutritionElements')

                        Calories = next((i for i in ll if i['key'] == 'calories'), None)
                        if Calories:
                            Calories = Calories.get('perServing')
                           
                        Total_Fat = next((i for i in ll if i['key'] == 'totalFat'), None)
                        if Total_Fat:
                            Total_Fat = Total_Fat.get('perServing')

                        Saturated_Fat = next((i for i in ll if i['key'] == 'saturatedFat'), None)
                        if Saturated_Fat:
                            Saturated_Fat = Saturated_Fat.get('perServing')

                        Trans_fat = next((i for i in ll if i['key'] == 'transFat'), None)
                        if Trans_fat:
                            Trans_fat = Trans_fat.get('perServing')

                        Cholesterol = next((i for i in ll if i['key'] == 'cholesterol'), None)
                        if Cholesterol:
                            Cholesterol = Cholesterol.get('perServing')

                        Sodium = next((i for i in ll if i['key'] == 'sodium'), None)
                        if Sodium:
                            Sodium = Sodium.get('perServing')

                        Total_Carbohydrate = next((i for i in ll if i['key'] == 'carbohydrates'), None)
                        if Total_Carbohydrate:
                            Total_Carbohydrate = Total_Carbohydrate.get('perServing')

                        Dietary_Fiber = next((i for i in ll if i['key'] == 'fiber'), None)
                        if Dietary_Fiber:
                            Dietary_Fiber = Dietary_Fiber.get('perServing')

                        Total_Sugars = next((i for i in ll if i['key'] == 'sugar'), None)
                        if Total_Sugars:
                            Total_Sugars = Total_Sugars.get('perServing')

                        Added_Sugars = next((i for i in ll if i['key'] == 'addedSugar'), None)
                        if Added_Sugars:
                            Added_Sugars = Added_Sugars.get('perServing')

                        Protein = next((i for i in ll if i['key'] == 'protein'), None)
                        if Protein:
                            Protein = Protein.get('perServing')
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
import math
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



