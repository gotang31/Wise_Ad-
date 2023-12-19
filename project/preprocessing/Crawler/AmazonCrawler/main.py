import pickle
from amacrawl import amazon_prod_url, amazon_prod_img_down
from time import sleep
import pandas as pd



if __name__ == '__main__' :

    cate_url_dict = {'2_dog_fence':['https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975312011%2Cn%3A2975346011&dc&ds=v1%3AO%2FdUmSDs6UXM8q5ZBiltLCyOoeiZgkTDYisLdagbcJA&qid=1702140570&rnid=2619533011&ref=sr_nr_n_10'], 
                 '3_dog_nosework':['https://www.amazon.com/s?k=nosework+for+dogs&crid=RN4YBTCU4RYK&qid=1702208454&sprefix=nosework%2Caps%2C253&ref=sr_pg_1'], 
                 '4_cat_tower':['https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975241011%2Cn%3A2975243011%2Cn%3A2975248011&dc&ds=v1%3AiccSBzb%2B7zvuTcI2RKh0K%2FbyVTJ76wnghF2MltPS840&qid=1702141180&rnid=2619533011&ref=sr_nr_n_11'], 
                 '5_cat_scratcher':['https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975241011%2Cn%3A2975243011%2Cn%3A3024130011&dc&ds=v1%3AKcvLLeg63a6nSZquNC63shIsy%2BGghd3kv8QobyuCcfU&qid=1702141180&rnid=2619533011&ref=sr_nr_n_7',
                                   'https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975241011%2Cn%3A2975243011%2Cn%3A2975247011&dc&ds=v1%3A%2B4P%2BaSc5I5EB7aeO1uevvPW82lm%2B54SQadsnf72%2BVuY&qid=1702141180&rnid=2619533011&ref=sr_nr_n_8'], 
                 '6_cat_toilet' :['https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975241011%2Cn%3A2975296011%2Cn%3A2975299011&dc&ds=v1%3ANdsl5u26TJ82%2F7JLNViQgHajgJVOke6VZgQ0%2F%2BbUJ5M&qid=1702141254&rnid=2619533011&ref=sr_nr_n_5'], 
                 '7_house':['https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975312011%2Cn%3A2975400011%2Cn%3A2975402011&dc&ds=v1%3A6mqtLMEB9YX5qDIe04QS5Xke863MTvCDZsK9k%2BrAvGg&qid=1702166892&rnid=2619533011&ref=sr_nr_n_4',
                           'https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975241011%2Cn%3A2975243011%2Cn%3A2975246011&dc&ds=v1%3A7oTIrnXa3d8s1hqzx33T33uIBCSzDgb1bvmhFif5XxY&qid=1702171332&rnid=2619533011&ref=sr_nr_n_5'], 
                 '8_carrier':['https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975312011%2Cn%3A2975333011%2Cn%3A2975337011&dc&ds=v1%3ANfod22SDQDgVwK2jGySM1%2Ftxc5rU8pGWtyXdQp9a6Mk&qid=1702168607&rnid=2619533011&ref=sr_nr_n_4', 
                              'https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975312011%2Cn%3A2975333011%2Cn%3A2975338011&dc&ds=v1%3A5sOVVgCfylu9iRiruAgP5%2FJwtivoXb%2FzEXByyb0Vs48&qid=1702168607&rnid=2619533011&ref=sr_nr_n_7', 
                             'https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975241011%2Cn%3A2975250011%2Cn%3A3024131011&dc&ds=v1%3A1tjmaHMGGEZ3u62A2TpV4%2FSUYqr1xuFGUEJM5t3qYn8&qid=1702171359&rnid=2619533011&ref=sr_nr_n_2',
                             ], 
                 '9_clothes':['https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975312011%2Cn%3A2975313011%2Cn%3A3024173011&dc&ds=v1%3AXfglOl9ynIBEhk%2B%2FAtE9Wiu%2BrG3rFU7cl7QBiuB4sZE&qid=1702170333&rnid=2619533011&ref=sr_nr_n_11',
                             'https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975312011%2Cn%3A2975313011%2Cn%3A3024171011&dc&page=5&qid=1702171263&rnid=2619533011&ref=sr_pg_5'
                             'https://www.amazon.com/s?i=pets-intl-ship&bbn=16225013011&rh=n%3A16225013011%2Cn%3A2619533011%2Cn%3A2975241011%2Cn%3A2975242011&dc&ds=v1%3A%2Fe4n0XDlKZL0VgdzQJ59fPU70wIk8kKZ74GfYaB1f8k&qid=1702171307&rnid=2619533011&ref=sr_nr_n_2']}


    cate_url_prod_dict = {'2_dog_fence':[], '3_dog_nosework':[], '4_cat_tower':[], '5_cat_scratcher':[], 
                        '6_cat_toilet' :[], '7_house':[], '8_carrier':[], '9_clothes':[]}

    for category, url_list in cate_url_dict.items():
        
        result_csv = pd.DataFrame()
        for url in url_list:
            # 적당한 데이터 수집하기
            if len(url_list) == 1:
                urls , product_DB = amazon_prod_url(url, category, 30)
                
            elif len(url_list) == 2:
                urls , product_DB = amazon_prod_url(url, category, 15)
                
            else:
                urls , product_DB = amazon_prod_url(url, category, 10)
                
            cate_url_prod_dict[category].extend(urls)
            result_csv = pd.concat([result_csv, product_DB])
            
        result_csv.to_csv(f'recommend/{category}/result.csv', index = False)
        
        sleep(4)

    with open('recommend/cate_url_prod_dict.pickle', 'wb') as fp:
        pickle.dump(cate_url_prod_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)

    for category, url_list in cate_url_prod_dict.items():
        for url in url_list:
            amazon_prod_img_down(category, url)