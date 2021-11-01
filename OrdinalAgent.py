from typing import List
import random

class OrdinalAgent:

    def bestRoom(self, prices:List[int])->int:
     '''
     INPUT: the prices of the n rooms, in shekels.
     // OUTPUT: the index of a room that the agent most
     // prefers in these prices. Index is between 0 and n-1 '''

     if 0 in prices:
         return prices.index(0)
     else:
         return random.randint(0,2)


def findAlmostEnvyFree(agents:List[OrdinalAgent], totalRent:int):

    for x in range(totalRent , -1, -1):
        for y in range(totalRent - x, -1, -1):
            z = totalRent -x -y
            result = []
            for i in range(3):
                result.insert(i, agents[i].bestRoom([x,y,z]))

            if 0 in result and 1 in result and 2 in result:
                return result, [x,y,z]


def printResult(result:list, prices:list):

    for i in range(3):
        print('Agent', i,  'receives room' , result[i], 'for' , prices[result[i]], 'shekels' )



if __name__ == '__main__':
    result, price = findAlmostEnvyFree([OrdinalAgent(), OrdinalAgent(), OrdinalAgent()], 3000)
    printResult(result, price)