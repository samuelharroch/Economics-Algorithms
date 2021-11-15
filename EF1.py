from typing import List
import random
import pandas as pd

class Agent:

    def __init__(self, items_utilities:list):
        self.items_utilities = items_utilities

    def item_value(self,item_index:int)->float:
        return self.items_utilities[item_index]


def is_EF1(agents:List[Agent], bundles:List[List[int]])->bool:

    for i in range(len(agents)):
        my_items_prices = map(lambda x: agents[i].item_value(x), bundles[i])
        my_utility = sum(list(my_items_prices))

        for item_list in bundles:

            item_prices = list(map(lambda x: agents[i].item_value(x), item_list))
            max_item = max(item_prices)
            sum_prices = sum(item_prices)

            if len(bundles[i]) <= len(item_list):
                total_price = (sum_prices-max_item)
            else:
                total_price = sum_prices

            if total_price > my_utility:
                return False

    return True


def round_robin(agents:List[Agent], num_of_items:int, list_of_items:list)->List[List[int]]:

    bundles =  [[] for i in range(len(agents))]

    agents_utilities = [agent.items_utilities.copy() for agent in agents]
    df = pd.DataFrame(agents_utilities, columns=list_of_items)

    while num_of_items != 0:

        for i in range(len(agents)):
            best_item = df.idxmax(axis=1)[i]
            bundles[i].append(list_of_items.index(best_item))
            df[best_item] = 0
            num_of_items -= 1
            if num_of_items == 0: break

    return bundles


if __name__ == '__main__':

    num_of_items = 7
    list_of_items = ['apple', 'banana', 'lemon', 'pear', 'watermelon', 'cherry', 'tomato']

    ami = Agent(random.sample(range(1, 100), num_of_items))
    print("ami utilities: ", ami.items_utilities)

    tami = Agent(random.sample(range(1, 100), num_of_items))
    print("tami utilities: ", tami.items_utilities)

    rami = Agent(random.sample(range(1, 100), num_of_items))
    print("rami utilities: ", rami.items_utilities)

    agents = [ami, tami, rami]
    bundles = round_robin(agents,num_of_items,list_of_items)

    print(bundles, '\n')
    print("is EF1 bundles: ", is_EF1(agents,bundles))

    dump_partition1 = [[0,1,2],[3,4],[5,6]]
    dump_partition2 = [[0, 3, 6], [1, 4 ], [2, 5]]

    print("is EF1 dump_partition1: ", is_EF1(agents, dump_partition1))
    print("is EF1 dump_partition2: ", is_EF1(agents, dump_partition2))