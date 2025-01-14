import numpy as np

# url = 'https://github.com/numpy/numpy/blob/master/numpy/random/mtrand.pyx#L778'
# a threshold for floating point arithmetic error handling
accuracy = np.sqrt(np.finfo(np.float64).eps)


def normalize_scheduling_probabilities(input_list: list) -> list:
    """    returns a rounded off list with the sum of all elements in the list to be equal to 1.0
    Handles these case:
        1) All the elements of the list are 0 -> the Probabilities are equally distributed
        2) When the sum(input_list) is away from 1.0 by an offset -> each prob. is divided by sum(input_list) and
           the difference of the sum of this new list to 1.0 is added to the first element of the list.
        3) An empty list is provided as input -> simply returns an empty list.
    Because of [1] an error range of +-0.000000014901161193847656 in the sum has to be handled.
    [1]:  https://stackoverflow.com/questions/588004/is-floating-point-math-broken
    """

    output_list = []
    # to handle the empty list case, we just return the empty list back
    if len(input_list) == 0:
        return output_list

    offset = 1 - sum(input_list)

    # a list with all elements 0, will be equally distributed to sum-up to 1.
    # sum can also be 0 if some elements of the list are negative.
    # In our case the list contains probabilities and they are not supposed to be negative, hence the case won't arise
    if sum(input_list) == 0:
        output_list = [round(1 / len(input_list), 2)] * len(input_list)

    # Because of floating point precision (.59 + .33 + .08) can be equal to .99999999
    # So we correct the sum only if the absolute difference is more than a tolerance(0.000000014901161193847656)
    else:
        if abs(offset) > accuracy:
            sum_list = sum(input_list)
            # we divide each number in the list by the sum of the list, so that Prob. Distribution is approx. 1
            output_list = [round(prob / sum_list, 2) for prob in input_list]
        else:
            output_list = input_list.copy()

    # 1 - sum(output_list) = the diff. by which the elements of the list are away from 1.0, could be +'ive /-i've
    new_offset = 1 - sum(output_list)
    if new_offset != 0:
        i = 0
        while output_list[i] + new_offset < 0:
            i += 1
        # the difference is added/subtracted from the 1st element of the list, which is also rounded to 2 decimal points
        output_list[i] = output_list[i] + new_offset
    assert abs(1 - sum(output_list)) < accuracy, "Sum of list not equal to 1.0"
    return output_list
