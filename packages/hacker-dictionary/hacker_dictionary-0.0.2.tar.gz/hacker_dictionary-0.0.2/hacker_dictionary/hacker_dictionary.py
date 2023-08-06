def Pure (Minimum_value,Maximum_value,interval=1):
    '''
    :param Minimum_value:最小数值
    :param Maximum_value: 最大数值
    :param interval: 步长（默认为1）
    :return:
    '''
    print(Minimum_value, interval, Maximum_value)
    int_Minimum_value = int(Minimum_value)
    storage = []
    for i in range(int_Minimum_value, Maximum_value + 1, interval):
        Original_value = list(str(i))  # 生成密码原始数据
        if len(Original_value) < len(Minimum_value):
            Difference = []
            while len(Difference) + len(Original_value) != len(Minimum_value):
                Difference.append('0')
            passwd = Difference + Original_value
            password = ''.join(passwd)
            storage.append(str(password))
        else:
            password = ''.join(Original_value)
            storage.append(str(password))
    return storage
def flie(File_name,List_Name):
    '''

    :param File_name:文件名称
    :param List_Name: 列表名称
    :return:
    '''
    file1 = open(File_name, 'w')
    for i in List_Name:
        file1.write(i)
        file1.write('\n')
def General(character,Minimum_length,Maximum_length):
    '''
    :param character: 所需字符
    :param Minimum_length: 最小长度
    :param Maximum_length: 最大长度
    '''
    storage = []
    list1 = list(character)
    list2 = [x for x in range(len(list1))]
    Key_array = dict(zip(list2, list1))
    # 算法
    key = []
    max_key = []
    while len(max_key) != Minimum_length:
        max_key.append(list2[len(list2) - 1])
    while len(key) != Minimum_length:
        key.append(0)
    while True:
        for i in list2:
            key[0] = i
            password = []
            for h in key:
                password.append(Key_array.get(h))
            psswd = ''.join(password)  # 去除多余符号
            storage.append(psswd)
            # 算法
            if key[0] == max_key[0]:
                for j in range(len(key)):
                    if key[j] != max_key[0]:
                        key[j] = key[j] + 1
                        key[j - 1] = 0
                        break
            if key == max_key:
                break
        if key == max_key:
            break
    if Maximum_length != Minimum_length:
        while len(key) != Maximum_length:
            for h in range(0, len(key)):
                key[h] = 0
            key.append(0)
            max_key.append(list2[len(list2) - 1])
            while True:
                for i in list2:
                    key[0] = i
                    password = []
                    for h in key:
                        password.append(Key_array.get(h))
                    psswd = ''.join(password)  # 去除多余符号
                    storage.append(psswd)
                    # 算法
                    if key[0] == max_key[0]:
                        for j in range(len(key)):
                            if key[j] != max_key[0]:
                                key[j] = key[j] + 1
                                key[j - 1] = 0
                                break
                    if key == max_key:
                        break
                if key == max_key:
                    break
    return storage
def Social_workers(name,Age,birthday,Company_school,Lucky_number,Name_relatives,Relative_age,Relative_birthday,Relative_Company_school,length):
    '''
    :param name: 姓名
    :param Age: 年龄
    :param birthday:生日
    :param Company_school:公司或学习
    :param Lucky_number:幸运数字
    :param Name_relatives:亲人姓名
    :param Relative_age:亲人年龄
    :param Relative_birthday:亲人生日
    :param Relative_Company_school:亲人公司或学习
    :param length: 长度
    :return:
    '''
    storage =[]
    birthday1=''
    for i in range(len(birthday)):
        if birthday[i] != '/':
            birthday1 = birthday1+birthday[i]
    Name_relatives1 = ''
    for i in range(len(Name_relatives)):
        if Name_relatives[i] != '|':
            Name_relatives1 = Name_relatives1+Name_relatives[i]
    Relative_age1 = ''
    for i in range(len(Relative_age)):
        if Relative_age[i] != '|':
            Relative_age1 = Relative_age1+Relative_age[i]
    Relative_birthday1 = ''
    for i in range(len(Relative_birthday)):
        if Relative_birthday[i] != '/' and Relative_birthday[i] != '|':
            Relative_birthday1 = Relative_birthday1+Relative_birthday[i]
    Relative_Company_school1=''
    for i in range(len(Relative_Company_school)):
        if Relative_Company_school != '|':
            Relative_Company_school1 = Relative_Company_school1+Relative_Company_school[i]
    character = name+Age+birthday1+Company_school+Name_relatives1+Relative_birthday1+Relative_Company_school1
    character = ''.join(list(set(character)))
    print(character)
    list1 = list(character)
    list2 = [x for x in range(len(list1))]
    Key_array = dict(zip(list2, list1))
    # 算法
    key = []
    max_key = []
    while len(max_key) != length:
        max_key.append(list2[len(list2) - 1])
    while len(key) != length:
        key.append(0)
    while True:
        for i in list2:
            key[0] = i
            password = []
            for h in key:
                password.append(Key_array.get(h))
            psswd = ''.join(password)  # 去除多余符号
            print(psswd)
            storage.append(psswd)
            # 算法
            if key[0] == max_key[0]:
                for j in range(len(key)):
                    if key[j] != max_key[0]:
                        key[j] = key[j] + 1
                        key[j - 1] = 0
                        break
            if key == max_key:
                break
        if key == max_key:
            break
    return storage