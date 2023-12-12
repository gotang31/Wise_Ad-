import modules.create_dummydata
import random


def create_insert_user_sql(repeat: int):
    f = open('./sql/insert_user.sql', 'w', encoding="utf-8")

    index = 0
    for i in range(repeat):
        table_name = "userinfo"
        idx = index
        name = modules.create_dummydata.create_name()
        gender = modules.create_dummydata.weighted_create(['male','female'], weights=[0.563,0.437])
        age = modules.create_dummydata.weighted_create([10,20,30,40,50,60],[0.047, 0.255, 0.219, 0.269, 0.167, 0.044])
        age = age + random.randint(0, 9)
        address = modules.create_dummydata.create_address_ko()
        index = index + 1

        f.write("insert into {0} values ({1}, \'{2}\', {3}, \'{4}\', \'{5}\');\n".format(table_name, idx, name, age, gender, address))


    print(index, "users were created")

    f.close()
    