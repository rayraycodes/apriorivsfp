# Author: Regan Maharjan
# University: University of Michigan
# Date: 2023-14-12

def load_data_set():
    # This function returns a hardcoded dataset of Nepali words for food items
    data_set = [
        ['दूध', 'अन्डा', 'रोटी', 'चिप्स'],
        ['अन्डा', 'पोपकोर्न', 'चिप्स', 'बीर'],
        ['दूध', 'बीर', 'रोटी'],
        ['दूध', 'अन्डा', 'रोटी', 'पोपकोर्न', 'बीर', 'चिप्स'],
        ['अन्डा', 'रोटी', 'चिप्स'],
        ['अन्डा', 'रोटी', 'बीर'],
        ['दूध', 'रोटी', 'चिप्स'],
        ['दूध', 'अन्डा', 'रोटी', 'मक्खन', 'चिप्स'],
        ['दूध', 'अन्डा', 'मक्खन', 'चिप्स']
    ]
    return data_set

def create_C1(data_set):
    # This function creates a set of all unique items in the dataset
    C1 = set()
    for transaction in data_set:
        for item in transaction:
            item_set = frozenset([item])
            C1.add(item_set)
    return C1

def is_apriori(Ck_item, Lksub1):
    # This function checks if an item combination Ck is valid
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True

def create_Ck(Lksub1, k):
    # This function creates Ck, a list of all possible combinations of items of length k
    Ck = set()
    len_Lksub1 = len(Lksub1)
    list_Lksub1 = list(Lksub1)
    for i in range(len_Lksub1):
        for j in range(i+1, len_Lksub1):
            l1 = list(list_Lksub1[i])
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k-2] == l2[0:k-2]:
                Ck_item = list_Lksub1[i] | list_Lksub1[j]
                if is_apriori(Ck_item, Lksub1):
                    Ck.add(Ck_item)
    return Ck