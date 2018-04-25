
import numpy


# -------------IMPORTANT----------#
# Reduce number of decimal places. no need to be that big when adjustments
# are in the range of dec = 0.008 and inc = 0.05
# double check vid for inc/dec values

# If center of normal distribution is = to threshold then
# there will be a 50% connectivity strength from the getgo
# and std = loc_value/2 ensures that 95% (should be about)
# of all values will be between 0-1 when loc is 0.5

# -------------DONE----------#
# Add main () to test this script
# if all values above 1 and bellow 0 are set to -1
# and ttreated as "unconnected" then a bit more than 5%
# are unconnected

def setup_pool():
    set_size = int(input("Number of colums:"))
    col_size = int(input("input size/Cells in collum:"))
    # center of normal distribution
    loc_value = 0.5
    # standard deviation
    scale_value = loc_value / 2

    return [set_size, col_size, loc_value, scale_value]


def create_pool(pool_spec):

    pool = [0] * pool_spec[0]
    for i in range(0, len(pool)):
            pool[i] = list(numpy.random.normal(pool_spec[2], pool_spec[3], pool_spec[1]))

            # treats weights over and under 0 as unconnected (-1)
            for j in range(0, len(pool[i])):
                if (pool[i][j] < 0 or pool[i][j] >= 1):
                    pool[i][j] = -1

    return pool


def main_pool():

    pool_spec = setup_pool()
    pool = create_pool(pool_spec)
    return pool

def test_pool():
    pool = main_pool()
    print(pool)
    print_pool(pool, 0.6)


#Rounds the numbers printed out.
 #Doesn not affect actual values
 #1 signifies threshold is breached
 #If number is higher or equal to threshold ist simply a rounding error.
 #rounding error is only on display, actual value isnt rounded.




#test_pool()


