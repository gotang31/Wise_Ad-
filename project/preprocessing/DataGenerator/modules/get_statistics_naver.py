#-*- coding: utf-8 -*-
import urllib.request
import re

client_id = "lY8C04HqGdcVzGaJx2dn"
client_secret = "7_ACUmdBcx"

startDate = "\"2023-11-01\""
endDate = "\"2023-11-30\""
timeUnit = "\"month\""
device = "\"pc\""
ages = "[\"10\",\"20\",\"30\",\"40\",\"50\",\"60\"]"
gender = "[\"f\", \"m\"]"


# return [10s-ratio, 20s-ratio, 30s-ratio, 40s-ratio, 50s-ratio, 60s-ratio] of selected category
def item_statistics_age(category_code):
    url = "https://openapi.naver.com/v1/datalab/shopping/category/age"
    category = "\"{0}\"".format(category_code)
    body = '{{\"startDate\": {0}, \"endDate\": {1}, \"timeUnit\": {2}, \"category\": {3}, \"device\": {4}, \"ages\": {5}}}'.format(
        startDate,
        endDate,
        timeUnit,
        category,
        device,
        ages,
        gender
    )

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
    resp_code = response.getcode()
    if resp_code == 200:
        response_body = response.read()
        data = response_body.decode('utf-8')
        ratios = re.findall(r'"ratio":(\d+(?:\.\d+)?)', data)
        num_ratios = list(map(float, ratios))
        list_sum = sum(num_ratios)
        # ['10','20','30','40','50','60']
        ratio_list = list(map(lambda x: x / list_sum, num_ratios))
        return ratio_list
    else:
        print("Error Code:" + resp_code)


# return [female-ratio,male-ratio] of selected category
def item_statistics_gender(category_code):
    url = "https://openapi.naver.com/v1/datalab/shopping/category/gender"
    category = "\"{0}\"".format(category_code)
    body = '{{\"startDate\": {0}, \"endDate\": {1}, \"timeUnit\": {2}, \"category\": {3}, \"device\": {4}, \"ages\": {5}}}'.format(
        startDate,
        endDate,
        timeUnit,
        category,
        device,
        ages,
        gender
    )

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
    resp_code = response.getcode()
    if resp_code == 200:
        response_body = response.read()
        data = response_body.decode('utf-8')
        ratios = re.findall(r'"ratio":(\d+(?:\.\d+)?)', data)
        num_ratios = list(map(float, ratios))
        # ['femaleRatio', 'maleRatio']
        list_sum = sum(num_ratios)
        ratio_list = list(map(lambda x: x / list_sum, num_ratios))
        return ratio_list
    else:
        print("Error Code:" + resp_code)


def get_item_distribution(category_code):
    age_ratio_list = item_statistics_age(category_code)
    gender_ratio_list = item_statistics_gender(category_code)
    while len(age_ratio_list) < 6:
        age_ratio_list.append(0)
    while len(gender_ratio_list) < 6:
        gender_ratio_list.append(0)

    male_10s = age_ratio_list[0] * gender_ratio_list[0]
    female_10s = age_ratio_list[0] * gender_ratio_list[1]
    male_20s = age_ratio_list[1] * gender_ratio_list[0]
    female_20s = age_ratio_list[1] * gender_ratio_list[1]
    male_30s = age_ratio_list[2] * gender_ratio_list[0]
    female_30s = age_ratio_list[2] * gender_ratio_list[1]
    male_40s = age_ratio_list[3] * gender_ratio_list[0]
    female_40s = age_ratio_list[3] * gender_ratio_list[1]
    male_50s = age_ratio_list[4] * gender_ratio_list[0]
    female_50s = age_ratio_list[4] * gender_ratio_list[1]
    male_60s = age_ratio_list[5] * gender_ratio_list[0]
    female_60s = age_ratio_list[5] * gender_ratio_list[1]

    ratio_list = list([male_10s, female_10s, male_20s, female_20s, male_30s, female_30s, male_40s, female_40s, male_50s, female_50s, male_60s, female_60s])

    return ratio_list