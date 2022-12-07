class FwMspider():
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
    def __init__(self):
        self.Data = []
        date = datetime.now().strftime('%Y%m%d')
        self.Path = f'footdown_market_dairy_2_{date}.csv'
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
            'https://www.foodtown.com/shopping/dairy/d/247',
            # 'https://www.foodtown.com/shopping/meat/d/290',
            # 'https://www.foodtown.com/shopping/seafood/d/440',
            # 'https://www.foodtown.com/shopping/produce/d/252',
        ]
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        self.ids = []
        for url in data:
            cageo = url.split('/')[-3]
            print(cageo)
            category_ids = url.split('/')[-1]
            res = httpx.get(url=url,headers=headers)
            if res.status_code == 200:
                print('Success...')
                temp = httpx.get('https://api.freshop.com/1/products?app_key=foodtown&department_id_cascade=true&include_departments=true&limit=0&render_id=1669258930662&store_id=2601&token=5bcef159637079db4cdbea55f5b9c4c2',headers=headers)
                department = temp.json().get('departments')
                total_items = next((i for i in department if i['name'].lower() == cageo), None)
                if total_items:
                            total_items = total_items.get('count')
                self.ids.append(tuple([cageo, category_ids, total_items]))


    def getListPage(self):
        self.productIds = []
        if self.ids:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
            }
            
            for id_ in self.ids:
                page = 20
                while page <= 40:
                    page+=1 
                    params = {
                        'limit': '48',
                        'skip': str(48*(page-1)),
                    }
                    print(page)
                    URL = 'https://api.freshop.com/1/products?app_key=foodtown&department_id={}&department_id_cascade=true&fields=id%2Cidentifier%2Cattribution_token%2Creference_id%2Creference_ids%2Cupc%2Cname%2Cstore_id%2Cdepartment_id%2Csize%2Ccover_image%2Cprice%2Csale_price%2Csale_price_md%2Csale_start_date%2Csale_finish_date%2Cprice_disclaimer%2Csale_price_disclaimer%2Cis_favorite%2Crelevance%2Cpopularity%2Cshopper_walkpath%2Cfulfillment_walkpath%2Cquantity_step%2Cquantity_minimum%2Cquantity_initial%2Cquantity_label%2Cquantity_label_singular%2Cvarieties%2Cquantity_size_ratio_description%2Cstatus%2Cstatus_id%2Csale_configuration_type_id%2Cfulfillment_type_id%2Cfulfillment_type_ids%2Cother_attributes%2Cclippable_offer%2Cslot_message%2Ccall_out%2Chas_featured_offer%2Ctax_class_label%2Cpromotion_text%2Csale_offer%2Cstore_card_required%2Caverage_rating%2Creview_count%2Clike_code%2Cshelf_tag_ids%2Coffers%2Cis_place_holder_cover_image%2Cvideo_config%2Cenforce_product_inventory%2Cdisallow_adding_to_cart%2Csubstitution_type_ids%2Cunit_price%2Coffer_sale_price%2Ccanonical_url%2Coffered_together%2Csequence&include_offered_together=true&limit=48&popularity_sort=asc&render_id=1669258930662&skip=960&sort=popularity&store_id=2601&token=5bcef159637079db4cdbea55f5b9c4c2'.format(id_[1])
                    res = httpx.get(url=URL,headers=headers,params=params)
                    if res.status_code == 200:
                        result = res.json()
                        if result.get('items'):
                            self.productIds.extend(list(map(lambda x:(x['id'],id_[0]),result.get('items'))))
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
                res = httpx.get(url='https://api.freshop.com/1/products/%s?app_key=foodtown&render_id=1669258930662&store_id=2601&token=5bcef159637079db4cdbea55f5b9c4c2'%id_[0],headers=headers)
                if res.status_code == 200:
                    result = res.json()
                    # ******************************************************************************************* #
                    Item_name = result.get('name')
                    if result.get('size'):
                        Item_name += ','+str(result.get('product_size')).upper()

                    Product_Number = id_[0]
                    Category = id_[1]

                    if result.get('unit_price'):
                            Unit_Price = result.get('unit_price')
                    else:
                        Unit_Price = None
                        
                    if result.get('size'):
                            Unit = '$/' + result.get('size').split(' ')[-1]
                    else:
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
import math
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



