#!python3

import cvxpy
import functools
import string


def Nash_budget(total, subjects, preferences):
    """
    :param total: float
    :param subjects:  List[str],
    :param preferences: :List[List[str]
    :return:
    """

    num_of_subjects = len(subjects)
    num_of_citizens = len(preferences)
    allocations = cvxpy.Variable(num_of_subjects)

    allocations_dict = dict(zip(subjects, allocations))
    utilities = []
    for citizen in range(num_of_citizens):
        utilities.append(cvxpy.sum([allocations_dict.get(key) for key in preferences[citizen]]))

    sum_of_logs = cvxpy.sum([cvxpy.log(u) for u in utilities])
    positivity_constraints = [v >= 0 for v in allocations]
    sum_constraint = [cvxpy.sum(allocations) == total]

    problem = cvxpy.Problem(
        cvxpy.Maximize(sum_of_logs),
        constraints=positivity_constraints + sum_constraint)
    problem.solve()

    # print budget partition
    print("\ntotal=" + str(total) + " subject=" + str(subjects) + ' preferences='+ str(preferences))

    budget_list = []
    budget = "BUDGET: " + " {}={} , " * num_of_subjects

    for i, v in (allocations_dict.items()):
        budget_list.append(i)
        budget_list.append(v.value)

    print (budget.format(*budget_list))

    # partition for each citizen
    for citizen in range(num_of_citizens):
        output = 'Citizen ' + str(citizen) + ' should donate '

        for subject in preferences[citizen]:
            donate = allocations_dict.get(subject).value * (total / num_of_citizens) / utilities[citizen].value
            output += str(donate) + ' to ' + subject + ', '

        output += 'utility ' + str(utilities[citizen].value)
        print(output)


if __name__ == '__main__':
    Nash_budget(500, ['a', 'b', 'c', 'd'], [['b', 'd'], ['a', 'c'], ['a', 'd'], ['b', 'c'], ['a']])

    Nash_budget(7500, ['Education', 'Sport', 'Road', 'Entertainment', 'Tech', 'Renovation'],
                [['Education', 'Tech'], ['Tech', 'Education'], ['Sport', 'Road'], ['Entertainment', 'Road'], ['Education', 'Sport']])