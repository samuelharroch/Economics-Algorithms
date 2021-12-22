#!python2.7

import cvxpy
import doctest
import math
import functools

import logging , sys
logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler(sys.stdout))
# logger.setLevel(logging.INFO)


def equal_dicts(dict1 , dict2 ):
    keys = dict1.keys()
    for key in keys:
        if abs(dict1[key] - dict2[key])>1: return False
    return True


def Nash_budget(total, subjects, preferences):
    """
    :param total: float
    :param subjects:  List[str],
    :param preferences: :List[List[str]
    :return: allocations_dict - allocation for each subject,
            partitions - citizen partitions for each preference

    >>> SUBJECTS = ['a', 'b', 'c', 'd']
    >>> PREFERENCES = [['b', 'd'], ['a', 'c'], ['a', 'd'], ['b', 'c'], ['a']]
    >>> allocations_dict, partitions = Nash_budget(500, SUBJECTS ,PREFERENCES)
    >>> total = sum(allocations_dict.values())
    >>> abs( total - 500) < 1
    True
    >>> [abs(sum(player_part) - 100) < 1 for player_part in partitions ] == [True]*5
    True
    >>> partitions_dict = [dict(zip(PREFERENCES[i],partitions[i])) for i in range(len(PREFERENCES))]
    >>> alloc_test = { k: sum([d.get(k) if d.get(k)!= None else 0  for d in partitions_dict]) for k in set().union(*partitions_dict)}
    >>> equal_dicts(alloc_test,allocations_dict)
    True


    >>> SUBJECTS = ['Education', 'Sport', 'Road', 'Entertainment', 'Tech', 'Renovation']
    >>> PREFERENCES =  [['Education', 'Tech'], ['Tech', 'Education'], ['Sport', 'Road'], ['Entertainment', 'Road'],['Education', 'Sport']]
    >>> allocations_dict, partitions = Nash_budget(7500, SUBJECTS ,PREFERENCES)
    >>> total = sum(allocations_dict.values())
    >>> abs( total - 7500) < 1
    True
    >>> [abs(sum(player_part) - 7500/len(PREFERENCES)) < 1 for player_part in partitions ] == [True]*5
    True
    >>> partitions_dict = [dict(zip(PREFERENCES[i],partitions[i])) for i in range(len(PREFERENCES))]
    >>> alloc_test = { k: sum([d.get(k) if d.get(k)!= None else 0  for d in partitions_dict]) for k in set().union(*partitions_dict)}
    >>> equal_dicts(alloc_test,allocations_dict)
    True
    >>> abs(allocations_dict.get('Renovation') - 0) < 0.01
    True


     >>> SUBJECTS = ['Education', 'Sport', 'Road', 'Entertainment', 'Tech', 'Renovation']
    >>> PREFERENCES =  [['Education', 'Tech'], ['Tech', 'Education'], ['Sport', 'Road'], ['Entertainment', 'Road'],['Education', 'Sport']]
    >>> allocations_dict, partitions = Nash_budget(999999, SUBJECTS ,PREFERENCES)
    >>> total = sum(allocations_dict.values())
    >>> abs( total - 999999) < 3
    True
    >>> [abs(sum(player_part) - 999999/len(PREFERENCES)) < 1 for player_part in partitions ] == [True]*5
    True
    >>> partitions_dict = [dict(zip(PREFERENCES[i],partitions[i])) for i in range(len(PREFERENCES))]
    >>> alloc_test = { k: sum([d.get(k) if d.get(k)!= None else 0  for d in partitions_dict]) for k in set().union(*partitions_dict)}
    >>> equal_dicts(alloc_test,allocations_dict)
    True
    >>> abs(allocations_dict.get('Renovation') - 0) < 0.01
    True
    """

    num_of_subjects = len(subjects)
    num_of_citizens = len(preferences)
    allocations = cvxpy.Variable(num_of_subjects)

    allocations_dict = dict(zip(subjects, allocations))
    utilities = []
    for citizen in range(num_of_citizens):
        utilities.append(cvxpy.sum([allocations_dict[key] for key in preferences[citizen]]))

    sum_of_logs = cvxpy.sum([cvxpy.log(u) for u in utilities])
    positivity_constraints = [v >= 0 for v in allocations]
    sum_constraint = [cvxpy.sum(allocations) == total]

    problem = cvxpy.Problem(
        cvxpy.Maximize(sum_of_logs),
        constraints=positivity_constraints + sum_constraint)
    problem.solve()

    # print budget partition
    logger.info("\ntotal=" + str(total) + "\nsubjects=" + str(subjects) + '\npreferences='+ str(preferences))

    budget_list = []
    budget = "BUDGET: " + " {}={} , " * num_of_subjects

    for i, v in (allocations_dict.items()):
        budget_list.append(i)
        budget_list.append(v.value)

    logger.info (budget.format(*budget_list))

    partitions = []
    # partition for each citizen
    for citizen in range(num_of_citizens):
        output = 'Citizen ' + str(citizen) + ' should donate '
        player_partition = []
        for subject in preferences[citizen]:
            donate = allocations_dict.get(subject).value * (total / num_of_citizens) / utilities[citizen].value
            output += str(donate) + ' to ' + subject + ', '
            player_partition.append(donate)

        partitions.append(player_partition)
        output += 'utility ' + str(utilities[citizen].value)
        logger.info(output)

    for key in allocations_dict.keys():
        allocations_dict[key] = allocations_dict.get(key).value

    return allocations_dict, partitions


if __name__ == '__main__':


    # Nash_budget(7500, ['Education', 'Sport', 'Road', 'Entertainment', 'Tech', 'Renovation'],
    #             preferences = [['Education', 'Tech'], ['Tech', 'Education'], ['Sport', 'Road'], ['Entertainment', 'Road'],
    #                            ['Education', 'Sport']])
    #
    # Nash_budget(1000000, ['Education', 'Sport', 'Road', 'Entertainment', 'Tech', 'Renovation'],
    #             preferences=[['Education', 'Tech'], ['Tech', 'Education'], ['Sport', 'Road'], ['Entertainment', 'Road'],
    #              ['Education', 'Sport']])

    doctest.testmod(name='Nash_budget', verbose=True)