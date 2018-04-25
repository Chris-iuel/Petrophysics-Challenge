#Add pool creation
#Change some data_setup_std to return records. make data extraction a choice???
#remopve min/max list from here
#make set_size,threshold and such variables easier to edit


from data_handler import *
from data_encoder import *


def pool_setup_std(col_size):
    #set_size = # cols you want
    set_size = 500
    #col_size  = len(encode_val)

    # center of normal distribution
    loc_value = 0.5
    # standard deviation
    scale_value = loc_value / 2

    max_col = 25
    threshold = 0.6
    return max_col,threshold,[set_size, col_size, loc_value, scale_value]


def data_setup_std():

  wells= data_join()
  records= data_parse(wells)



  min_list, max_list = data_scope(records)
  min_list = data_extract(min_list)
  max_list = data_extract(max_list)

  data = []

  for i in range(len(records)):
      data += [data_extract(records[i])]

  return data,min_list,max_list


def enc_setup_std(data, min_list, max_list):


  #[n, w, minVal, maxVal, rangeVal, numBuckets]
  encode_vals =[]


  n = 100
  w = 5
  numBuckets = n + 1 - w

  for i in range(len(data[0])) :
      minVal = min_list[i]
      maxVal = max_list[i]
      rangeVal = maxVal - minVal
      encode_vals += [[n,w,minVal,maxVal,rangeVal,numBuckets]]

   # creates the encoder values needed to encode each variable in a record

  return encode_vals


