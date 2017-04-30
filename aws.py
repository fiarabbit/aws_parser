#! /usr/bin/python3
import urllib.request
import json
import re

URL="https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json"
with urllib.request.urlopen(URL) as url:
    root_dict=json.loads(url.read().decode())

# regexp=re.compile('.*(((?<!Host)Box)|Dedicated)Usage.*$')
regexp=re.compile('.*((?<!Host)Box)Usage.*p2.*large.*')
regexp2=re.compile('Linux')

product_list = []
product_instanceType_list=[]
product_region_list = []
product_preInstalledSw_list=[]
for key in root_dict['products']:
    try:
        usage=root_dict['products'][key]['attributes']['usagetype']
        if regexp.match(root_dict['products'][key]['attributes']['usagetype']):
            if regexp2.match(root_dict['products'][key]['attributes']['operatingSystem']):
                product_list.append(str(key))
                product_instanceType_list.append(root_dict['products'][key]['attributes']['instanceType'])
                product_region_list.append(root_dict['products'][key]['attributes']['location'])
                product_preInstalledSw_list.append(root_dict['products'][key]['attributes']['preInstalledSw'])
    except KeyError:
        pass

# reject SQL
while 'SQL Server Enterprise' in product_preInstalledSw_list:
    i=product_preInstalledSw_list.index('SQL Server Enterprise')
    product_list.pop(i)
    _=product_instanceType_list.pop(i)
    _=product_region_list.pop(i)
    _=product_preInstalledSw_list.pop(i)

product_price_list=[]
for key in product_list:
    try:
        terms_ondemand=root_dict['terms']['OnDemand'][key].keys()
        for key_to in terms_ondemand:
            try:
                pd=root_dict['terms']['OnDemand'][key][key_to]['priceDimensions'].keys()
                for key_pd in pd:
                    try:
                        product_price_list.append(root_dict['terms']['OnDemand'][key][key_to]['priceDimensions'][key_pd]['pricePerUnit']['USD'])
                    except KeyError:
                        print('fuck')
            except KeyError:
                print(str(key_to) + " has no priceDimensions")
    except KeyError:
        print(key + " has no correspondence to terms_ondemand")

for i in range(0,len(product_list),1):
    instance=product_instanceType_list[i]
    region = product_region_list[i]
    price=product_price_list[i]
    if instance=='p2.xlarge':
        print("{:<13} {:<30} {:<15}".format(instance, region, price))

for i in range(0,len(product_list),1):
    instance=product_instanceType_list[i]
    region = product_region_list[i]
    price=product_price_list[i]
    if instance=='p2.8xlarge':
        print("{:<13} {:<30} {:<15}".format(instance, region, price))

for i in range(0,len(product_list),1):
    instance=product_instanceType_list[i]
    region = product_region_list[i]
    price=product_price_list[i]
    if instance=='p2.16xlarge':
        print("{:<13} {:<30} {:<15}".format(instance, region, price))
