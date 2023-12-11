from faker import Faker
import random

fake = Faker('ko_KR')
Faker.seed()


def create_name():
    name = fake.name()
    return name


def create_phone_number():
    p_number = ('010-' + str(random.randint(1, 9999)).zfill(4) + '-' + str(random.randint(1, 9999)).zfill(4))
    return p_number


def create_rating():
    rating = random.choices([5,4,3,2,1],[0.8, 0.1, 0.04, 0.02, 0.02])
    return rating[0]


def weighted_create(group, weights):
    weight = weights
    dummy = random.choices(group, weights = weight)
    return dummy[0]
