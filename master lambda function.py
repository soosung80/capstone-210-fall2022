import googlemaps 
import pandas as pd
import numpy as np
import json
import boto3
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from io import BytesIO
import requests
import re
import pprint
import string
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import roc_curve, auc, roc_auc_score
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO # Python 2.x
else:
    from io import StringIO # Python 3.x


def lambda_handler(event, context):
    # Data file path
    client = boto3.client('s3')
    bucket='bargaineatsgrocerydata'
    data_key1 = 'Retail_Food_Stores - Sheet5.csv'
    csv_obj1 = client.get_object(Bucket=bucket, Key=data_key1)
    body1 = csv_obj1['Body']
    csv_string1 = body1.read().decode('utf-8')
    
    data_key3 = '221123/Merged_data_translated_20221123.csv'
    csv_obj3 = client.get_object(Bucket=bucket, Key=data_key3)
    body3 = csv_obj3['Body']
    csv_string3 = body3.read().decode('utf-8')

    # user_input_str = json.dumps(event)
    user_input = json.loads(event['body'].encode('utf-8'))
    
    # Data import and preprocess
    df1 = pd.read_csv(StringIO(csv_string1))
    df1['Coordinates'] = [eval(df1['Coordinates'][i]) for i in range(len(df1))]
    
    df2 = pd.json_normalize(user_input)
    # df2['user_preference.user_location.lat'] = [eval(df2['user_preference.user_location.lat'][i]) for i in range(len(df2))]
    # df2['user_preference.user_location.lng'] = [eval(df2['user_preference.user_location.lng'][i]) for i in range(len(df2))]
    if len(user_input['groceries']) == 0:
        return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"  
            },
        # "body": 'No input for grocery list, please provide the grocery item.',
        "body": "[{\"address\": \"\", \"store_name\": \"\", \"lat\": -777 , \"lng\": -777, \"distance\": -777, \"travel_time\": -777, \"total\": -777, \"grocery_list\": []}]"
            }
        sys.exit()
    
    df3 = pd.read_csv(StringIO(csv_string3))
    
    # API setup for googlemaps
    API_key = 'AIzaSyCRvZm1MCZuU7sVyBd664xa0PFZcyFWGm4' 

    gmaps = googlemaps.Client(key=API_key)
    
    # Origin and dest setup
    origin = (df2['user_preference.user_location.lat'][0],df2['user_preference.user_location.lng'][0]) 
    destinations = df1.Coordinates
    mode = df2['user_preference.travel_mode'][0]
    
    # Travel time and duration calculation
    actual_duration = []
    for destination in destinations:
        result = gmaps.distance_matrix(origin, destination, mode=mode)["rows"][0]["elements"][0]["duration"]["value"]  
        result = round(result/60, 2)
        actual_duration.append(result)
    df1["duration (Mins)"] = actual_duration
    
    actual_distance = []
    for destination in destinations:
        result = gmaps.distance_matrix(origin, destination, mode=mode)["rows"][0]["elements"][0]["distance"]["value"]  
        result = round(result/1000 * 1.609344, 2)
        actual_distance.append(result)
    df1["distance (mi)"] = actual_distance #Add the list of coordinates to the main data set
    
    # Defining functions for cosine similarity and text cleaning
    def clean_item_data(df):
        df['Item name']=df['Item name'].str.replace('Yoghurt', 'Yogurt')
        df['Store']=df['Store'].replace(regex='Footdown', value='Foodtown')
        df=df.drop('Unnamed: 0', axis='columns')
        return df
    
    def clean_store_data(df):
        df['Store']=df['Entity Name'].map({'TRADER JOES EAST INC':"Trader Joe's",
                                            'ALDI INC':'Aldi',
                                            'WHOLE FOODS MARKET GROUP INC':'Wholefoods Market',
                                           'FOOD TOWN': 'Foodtown Market',
                                           'FAIRWAY MARKET':'Fairway Market'})
        df['Street']=df[['Street Number', 'Street Name']].apply(lambda x: ' '.join(x.dropna().astype(str)),axis=1)
        df['Address']=df[['Street', 'City', 'State', 'Zip Code']].apply(lambda x: ', '.join(x.dropna().astype(str)),axis=1)
        # df['Store']=df['Store'].replace(regex='Footdown', value='Foodtown')
        cl_df=df[['Borough','Store', 'Address','Coordinates', 'duration (Mins)', 'distance (mi)']].drop_duplicates()
        return cl_df
    
    def nlp_engine(df, product_input):
        new_df = df
        new_df['metadata'] = new_df.apply(lambda x : x['Item name'], axis = 1)
        count_vec = CountVectorizer(stop_words='english')
        count_vec_matrix = count_vec.fit_transform(new_df['metadata'])
        vec = count_vec.transform(pd.Series(product_input))
        simil = cosine_similarity(vec, count_vec_matrix)
        simil_scores = pd.DataFrame(simil.reshape(new_df.shape[0],), index = new_df.index, columns=['score'])
    
        # Don't return scores of zero, only as many positive scores as exist
        non_zero_scores = simil_scores[simil_scores['score'] > 0]
    
        if len(non_zero_scores) == 0:
            print('No similar products found.  Please refine your search terms and try again')
            return 
        
        similarity_scores = simil_scores.sort_values(['score'], ascending=False)[:10]
        return new_df[new_df.index.isin(list(similarity_scores.index))]
    
    def dietary_filter(df, columns):
        query_list = []
        for col in columns:
            query_list.append(f'{col}== 1')
        query = ' & '.join(query_list)
        return df.query(query)
    
    def get_data(df1, df2):
        item_df = clean_item_data(df1)
        store_df = df2
        #get store location data
    
        store_locator= clean_store_data(store_df)
        #merge dataframes
        merged_df=item_df.merge(store_locator, how='left', on='Store')
        return merged_df
        
    def Clean_names(item_name):
        # Search for opening bracket in the name followed by
        # any characters repeated any number of times
        if re.search('\,\s*\d+\s*.*', item_name):
            # Extract the position of beginning of pattern
            pos = re.search('\,\s*\d.*', item_name).start()
      
            # return the cleaned name
            return item_name[:pos]
        elif re.search('\(\s*.*\s*\).*',item_name):
           # Extract the position of beginning of pattern
            start = re.search('\(.*', item_name).start()
            end = re.search('\)', item_name).start()
            return item_name[:start]
      
        else:
            # if clean up needed return the same name
            return item_name
            
    def remove_punctuations(text):
        for char in string.punctuation:
            text = text.replace(char, '')
        return text
        
    def FindSubcategory(vec): #function to find key words in the item name
        clean_item_name = vec['clean_item_name']
        Category = vec['Category']
        item_name = vec['Item name'].lower()
        # print(item_name)
        for cat in subcat_key_words:
            if cat == Category:
                for subcat in subcat_key_words[cat]:
                    for key_word in subcat_key_words[cat][subcat]:
                      #check if the any of the keywords for each subcategory are in the item name
                        if key_word in clean_item_name or key_word+'s' in clean_item_name:
                        #if yes set the the subcategory
                            subcategory = subcat
                            # print(subcategory)
                            return subcategory
            
    # create subcategory key words dictionary
    # Format:   {'category':{'subcategory':['key words']}}
    subcat_key_words = {'dairy':{ 'dairy substitutes':['soy','dairy-free','almond','lactaid','coconut','oat','nut milk','silk','dairy free','plant based','plantbased','almondmilk','lactose free','lactosefree','soymilk','oatmilk','cashewmilk'],
                                'yogurt':['yogurt','danimals','kefir','yoghurt','chobani','greek','smoothie'],
                                 'milk products':['half','smoothie','2%','beverage','vanilla','cacao','mocha','nog','egg nog','milk','soymilk','buttermilk','half and half','half half','creamer','cream','heavy whipping cream','french vanilla'],
                                 'cheese':['cheese','piave','italian blend','grand cru','caramella','mozz','fromage','humboldt fog','saint angel','kefalograviera','ovalie cendree','chevre','pepper jack','cheddar','mahon','daffinois','queso','sargento','havarti','manchego','asiago ','mascarpone','halloumi','brie','singles','le marechal','burrata','feta','parmesan','mozzarella','cheddar','gouda','provolone','velveeta'],
                                 'juice, tea & coffee':['juice','naked','minute maid','drink','punch','lemonade','limeade','tea','kombucha','simply','coffee'],
                                 'ice cream/novelty':['jello','chocolate','pudding','gelatin','moo tubes','candy','cookie dough','ice cream','novelty','whipped cream','whipped topping','cream puff','sorbet'],
                                 'butter and spreads':['butter','parkay','pate','dressing','sour cream','mousse','margarine','ghee','shortening','spread','cream cheese','dip'],
                                 'eggs':['eggs','egg whites','egg','egg yolks']
                                 },
                
                        'produce':{'spices & herbs':['parsley','herbs','bay leaves','sage','yellow name','tarragon','tumeric','red oak leaf','white name','chicory','capers','okra','aloe','mint','basil','cilantro','italian herbs','garlic','ginger'],
                                   'vegetables':['parsnip','yautia','kim chee','bok choy','collard green','sprout','artichoke','daikon','dill','pickles','malanga coco','kimchi','scallions','tempeh','veggie','vegetable','tofu','brussel sprout','brussels sprout','corn','artichokes','shallots','mushroom','asparagus','green beans','eggplant','broccoli','cabbage','fennel','carrot','celery','broccili','broccilini','cauliflower','seaweed','zucchini','potato','beet','yam','tomato','cucumber','onion','bean sprouts','squash','chard','leek','pepper','peas'],
                                   'salad':['coleslaw','butter','caesar','butterhead','mix','radish','spring mix','salad','greens','kale','spinach','arugula','lettuce','romaine','rocket salad'],
                                   'fruits':['papaya','tomatillo','olive','coconut','tangerines','honey dew','apples','pink lady','melon','pumpkin','mandarins','nectarines','prunes','dates','grapes','clementines','watermelon','banana','kiwi','kiwifruit','apple','grapefruit','avocado','watermelon','cantaloupe','mango','pomegranate','apricot','pear','plum','peach','peaches','lemon','lime','orange','cutie'],
                                   'berries':['plantain','blueberry','cranberry','cranberries','gooseberries','platain','raspberries','blackberries','blueberries','strawberries','cherries','cranberries'],
                                   'nuts and seeds' : ['pepitas','pecan','pistachios','filberts','raisins','almonds','cashews','cashew','almond','seeds','figs','nuts','nut']    
                                 
                                 },
                        
                        'meat':{'meat substitue':['meatless','tofu','beyond burger','impossible burger', 'beyond','plantbased','plant based'],                       
                                'poultry':['chicken','nugget','hen','tenders','turkey','duck','wings','drumsticks'],
                                'red meat':['franks','chorizo','pork','filet mignon','sauasge','beef','sirloin','meatball','carne','chuck','roast','bratwurst','wieners','wiener','hot dogs','hot dog','ribs','sausage','pork','burger patties','burger','burger patty','bacon','ham','lamb','veal','goat','venison','bison','boar','steak'],
                                'deli':['soppressata','salame','salami','prosciutto','salami','italian sausage','pepperoni']
                                },
    
                        'seafood':{'crusteceans':['shrimp','lobster','oysters','crab','prawns'],
                                   'mollusks/bivalves':['scallops','octopus','squid','clams','mussels','abalone','snail'],
                                   'fish':['perch','herring','sea bass','porgie','dab','atlantic','pollock','haddock','drumsticks','cod','salmon','fillet','fish','anchovies','porgy','tenders','branzini','sardines','sardine','mackerel','codfish','seafood','trout','mahi mahi','grouper','tuna','catfish','snapper','tilapia']
                            
                                  }
                        }
        
    # Finding the best cosine similarity based on item name and suggested based on the travel time
    data = get_data(df3, df1)
    # data['distance (mi)'] = data['distance (mi)'].astype(float)
    df4 = data[data['distance (mi)'] <= user_input['user_preference']['distance']]
    if len(df4) != 0 :
        output = pd.DataFrame()
        for store in list(df4['Store'].unique()):
            df5=df4[df4['Store'] == store]
            for item in user_input['groceries']:
                filtered_df=(nlp_engine(df5, item))
                output=output.append(filtered_df)
    
        user_dietary_restrictions=[k.capitalize() for k, v in user_input['user_preference']['dietary_restrictions'].items() if v == 'true']
        if len(user_dietary_restrictions) != 0:
            for res in user_dietary_restrictions:
                df6=output[output[res] == 1]
        else:
            df6=output
    else:
        return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"  
            },
        # "body": 'No available store within the distance, please extend the input distance.',
        "body": "[{\"address\": \"\", \"store_name\": \"\", \"lat\": -888 , \"lng\": -888, \"distance\": -888, \"travel_time\": -888, \"total\": -888, \"grocery_list\": []}]"
            }
        sys.exit()
    
    
    ny_df = data.copy(deep=True)
    ny_df['clean_item_name'] = data["Item name"].str.lower()
    ny_df['clean_item_name'] =ny_df['clean_item_name'].apply(Clean_names)
    ny_df['clean_item_name'] =ny_df['clean_item_name'].apply(remove_punctuations)
    ny_df["subcategory"] = ny_df.apply(FindSubcategory,axis=1)
    
    
    # Text cleaning for optimized grocery list
    df7 = df6.copy(deep=True)
    df7['clean_item_name'] = df7['Item name'].str.lower()
    df7['clean_item_name'] =df7['clean_item_name'].apply(Clean_names)
    df7['clean_item_name'] =df7['clean_item_name'].apply(remove_punctuations)
    df7["subcategory"] = df7.apply(FindSubcategory,axis=1)
    df7['Cheaper Alternative Name'] = df7.apply(lambda _: None, axis=1)
    df7['Cheaper Alternative Price'] = df7.apply(lambda _: None, axis=1)
    df7['Cheaper Alternative Unit Price'] = df7.apply(lambda _: None, axis=1)
    
    store_list = df7['Store'].unique()
    df7_new = pd.DataFrame(data=None, columns=df7.columns, index=None)
    #filter the dataset for the aldi
    for store in store_list:
        filtered_store = ny_df.loc[(ny_df['Store'] == store)]
        df7_temp = df7.loc[(df7['Store'] == store)]
        for index, row in df7_temp.iterrows():
            filtered_dataset = filtered_store.loc[(filtered_store['Price'] < row['Price']) & (filtered_store['Category'] == row['Category']) & (filtered_store['subcategory'] == row['subcategory'])].sort_values('Price')
            if len(filtered_dataset) >= 1:
                recommendation_info = filtered_dataset.iloc[1]
                df7_temp['Cheaper Alternative Name'][index] =  recommendation_info['Item name']
                df7_temp['Cheaper Alternative Price'][index] =  recommendation_info['Price']
                df7_temp['Cheaper Alternative Unit Price'][index] =  recommendation_info['Unit Price']
            else:
                df7_temp['Cheaper Alternative Name'][index] =  None
                df7_temp['Cheaper Alternative Price'][index] =  None
                df7_temp['Cheaper Alternative Unit Price'][index] = None
        df7_new = pd.concat([df7_new, df7_temp])
   

    # Prepare the output response
    output = []
    for i in range(len(df7_new['Address'].unique())):
        total = 0
        selected_row = df7_new.loc[df7_new['Address'] == df7_new['Address'].unique()[i]]
        output.append(dict({'address': selected_row['Address'].iloc[0], 'store_name': selected_row['Store'].iloc[0], 'lat': selected_row['Coordinates'].iloc[0][0],
                                    'lng': selected_row['Coordinates'].iloc[0][1], 'distance': selected_row['distance (mi)'].iloc[0],
                                    'travel_time': selected_row['duration (Mins)'].iloc[0], 'total': total, 'grocery_list': []}))
        for j in range(len(selected_row)):
            total += selected_row['Price'].iloc[j]
            output[i]['grocery_list'].append(dict({'item_name' : selected_row['Item name'].iloc[j], 'price':selected_row['Price'].iloc[j],
                                                'unit_price':selected_row['Unit Price'].iloc[j], 'unit': selected_row['Unit'].iloc[j], 
                                                'alternative': selected_row['Cheaper Alternative Name'].iloc[j], 'alternative_price': selected_row['Cheaper Alternative Price'].iloc[j],
                                                'alternative_unit_price': selected_row['Cheaper Alternative Unit Price'].iloc[j], 'subcategory': selected_row['subcategory'].iloc[j]}))
            output[i]['total'] = round(total, 2)
    
    # Sort by distance and total price
    temp_output = pd.json_normalize(output)
    temp_output = temp_output.sort_values(by = ['distance', 'total'], ascending = [True, True], na_position = 'first')
    # Filtering out items from same subcategory within same store
    temp_temp_output = []
    for i in range(len(temp_output)):
        total = 0
        temp_temp_output.append(dict({'address': temp_output.iloc[i]['address'], 'store_name': temp_output.iloc[i]['store_name'], 'lat': temp_output.iloc[i]['lat'],
                            'lng': temp_output.iloc[i]['lng'], 'distance': temp_output.iloc[i]['distance'],
                            'travel_time': temp_output.iloc[i]['travel_time'], 'total': temp_output.iloc[i]['total'], 'grocery_list': []}))
        sub_list = []
        for j in range(len(temp_output.iloc[i]['grocery_list'])):
            if temp_output.iloc[i]['grocery_list'][j]['subcategory'] not in sub_list:
                total += temp_output.iloc[i]['grocery_list'][j]['price']
                sub_list.append(temp_output.iloc[i]['grocery_list'][j]['subcategory'])
                temp_temp_output[i]['grocery_list'].append(temp_output.iloc[i]['grocery_list'][j])
                temp_temp_output[i]['total'] = "{:.2f}".format(total)
    # remove subcategory in final response
    for i in range(len(temp_temp_output)):
        for j in range(len(temp_temp_output[i]['grocery_list'])):
            del temp_temp_output[i]['grocery_list'][j]['subcategory']
    temp_temp_output = pd.DataFrame(data=temp_temp_output)
    temp_temp_output = temp_temp_output.to_dict('records')
    
    new_output = []
    temp = 0
    for i in range(len(temp_temp_output)):
        if float(temp_temp_output[i]['total']) < user_input['user_preference']['budget']:
            temp += 1
            new_output.append(temp_temp_output[i])
    if temp == 0:
        return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"  
            },
        # "body": 'No store satisfy with the budget selection. We can provide more if more budget is allowed.',
        "body": "[{\"address\": \"\", \"store_name\": \"\", \"lat\": -999 , \"lng\": -999, \"distance\": -999, \"travel_time\": -999, \"total\": -999, \"grocery_list\": []}]",
        }
        sys.exit()
    else:
        return {
            "statusCode": 200,
            "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"  
            },
            "body": json.dumps(new_output),
            }
