import math

# [well_id, name, latitude, longitude, plug_id, depth, strat-group, a, b, c, d, e, f]
# ['4987', 'A-1', '56,9163', '3,0719', '1340', '3433,07', 'HELIUM', '5,11', '', '0,19', '98,55', '2,76', '0,43']
# [latitude,longitude,depth, strat-group, a, b, c, d, e, f]
# [2,3,5,6,7,8,9,10,11,12]
# [56.9163, 3433.07, 1, 5.11, '', 0.19, 98.55, 2.76, 0.43]
# Returning an encoder filled with zeroes to represent missing data is not the same as returning an
# encoded version of zero

def setup_encoder():
    n = int(input("Select total # bits in encoder (n):"))
    w = int(input("# active bits on encoder (w):"))
    minVal = int(input("Min value"))
    maxVal = int(input("Max value"))
    rangeVal = maxVal - minVal
    numBuckets = n + 1 - w

    return [n, w, minVal, maxVal, rangeVal, numBuckets]


def scalar_encoder(input_value, encode_val):



    # sets all input values outside of range to max/min
    if input_value == "":
        return [0]*encode_val[0]
        # Returning an encoder filled with zeroes to represent missing data is not the same as returning an
        # encoded version of zero
    elif input_value < encode_val[2]:
            input_value = encode_val[2]

    elif input_value > encode_val[3]:
            input_value = encode_val[3]

    # Calculates which bucket the number fits into
    # use math.floor instead of just int to prevent error using floats,
    # and rounding errors when using negative values

    # out = floor( numBuckets*(input_value-minVal) / rangeVall )

    out = int(math.floor((encode_val[5] * (input_value - encode_val[2]) / encode_val[4])))

    # set number of zeroes = number of total bits
    input_enc = [0] * encode_val[0]
    # out = value of the bucket it is in
    # e.g bucket #1 and -1 is the starting postion.
    # so 1-1 = 0 as the starting index for bucket1
    # 2-1 = 1 for the starting index for bucket 2

    #print("H ",len(input_enc),out)
    #--------------------------ADDED TO FIX INDEX. Concequence unknown!!!!!!!! take a closer look later
    out -= 1

    for j in range(out, out + encode_val[1]):
        input_enc[j] = 1

    return input_enc


def main_encoder():

    encode_val = setup_encoder()

    # use float to accept floats and ensure standarised input
    value = float(input("Value to decode:"))
    input_enc = scalar_encoder(value, encode_val)

    return input_enc

# main_encoder ()
