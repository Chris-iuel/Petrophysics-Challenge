


def print_pool(pool_set, threshold):

    print("[")
    for i in range(0, len(pool_set)):
        temp_list = [0] * len(pool_set[0])
        print()
        for j in range(0, len(pool_set[i])):

              if pool_set[i][j] >= threshold:
                    temp_list[j] = 1.000
              else :


                    a = float("{0:.3f}".format(pool_set[i][j]))
                    temp_list[j] = a

        print(temp_list)

    print("]")

def main_test(pool_set, threshold, input_enc):


    act_cell = [0] * len(pool_set)

# Calculates number of cells activated in each collum
    for i in range(0, len(pool_set)):
        for j in range(0, len(pool_set[i])):
            # if this bit in the output is active :
            if input_enc[j] == 1:
                # andif the cell permanence is above the threshold
                if pool_set[i][j] >= threshold:
                    act_cell[i] += 1

    return (act_cell)
# main_test ()

def training(index_list, pool_set, max_col, input_enc):

    act_inc = 0.05
    inact_dec = 0.008

    try:
        for i in range(1, max_col + 1):
            # returns index of col to be trained
            index = index_list.index(i)

            # itterates through the col and trains
            # cells which alligns with input
            for j in range(0, len(pool_set[index])):

                # Reinforces the cells in input space
                if pool_set[index][j] != -1:

                    if input_enc[j] == 1:

                            if pool_set[index][j] < (1-act_inc) :
                                pool_set[index][j] += act_inc
                    else:
                            if pool_set[index][j] >(0+inact_dec) :
                                    pool_set[index][j] -= inact_dec

    except ValueError:
        # Not enough activated collumns in set to reach max_col
        print("Value Error in  training")
        print(i," i value")
        pass

    return pool_set

# Takes in act_col, copies it in a list called score
# and then sorts it from high to low
# Creates and returns a list called index_list where
# the score and position of each col is stored


def training_index(act_col):
    # make sure you dont reffer to act_col but clone it
    score = list(act_col)
    score.sort(reverse=True)
    index_list = [0] * len(act_col)

    for i in range(0, len(act_col)):

        index = act_col.index(score[i])

        # gives each col in act_col a score based on highest
        # to lowest # act cell (+1 to make #1 score
        # 1 and not 0)

        if act_col[index] > 0:
            index_list[index] = i + 1
            act_col[index] = 0

    return index_list
