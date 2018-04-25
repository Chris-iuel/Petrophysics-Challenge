#record = [well_id, name, latitude, longitude, plug_id, depth, strat-group, a, b, c, d, e, f]
 # extracted data = [latitude,longitude,depth, strat-group, a, b, c, d, e, f]
# [2,3,5,6,7,8,9,10,11,12]
#len = 20
#assumes the first record is a complete record, which needs no padding
#ERROR IN STRAT GROUPS!! value 11 is left blank. (missing strat group is given a VALUE OF 11)
#poss fixed by giving blank value of 0
#strat group dont have connection with each other. concept should have no overlap.



import csv


def data_fetch(name) :

  data = []
  with open(name) as csvfile:

    reader = csv.reader(csvfile, delimiter = ';')
    for row in reader:
      data += [row]

  return data





def data_join():
  fname = ["data/WELLS.csv", "data/ALPHA.csv", "data/BETA.csv", "data/DELTA.csv", "data/EPSILON.csv", "data/GAMMA.csv"]


  wells = []

  wells += data_fetch(fname[0])
  alpha = data_fetch(fname[1])
  beta = data_fetch(fname[2])
  delta = data_fetch(fname[3])
  epsilon = data_fetch(fname[4])
  gamma = data_fetch(fname[5])


  wells = wells[1:]
  alpha = alpha[1:]
# cuts off first record which contains name of variables


  records_wells = []

  for i in range(len(wells)):
    for j in range(len(alpha)):
      if wells[i][0] == alpha[j][1] :
        records_wells +=   [wells[i] + [alpha[j][0]] + alpha[j][2:]]
        #print(i," + ",j)

  #Joins together lists with same well_id
  #will create multiple records. one for each plug
  #record = [well_id, name, latitude, longitude, plug_id, depth, strat-group]



#4 is the index of the plug,id
  records_beta = data_records(records_wells,beta,4)
    #appends data from beta to record with same plug id
  #record = [well_id, name, latitude, longitude, plug_id, depth, strat-group, a, b, c, d, e, f]
  #len(records) == len(alpha)  >= len(beta)
  records_delta =  data_records(records_beta,delta,4)
  records_epsilon = data_records(records_delta,epsilon,4)
  records_gamma = data_records(records_epsilon,gamma,4)




  print(records_gamma[0])

  return records_gamma


def data_records(old,new,id_index):

  #a ensures that a record isn't lost if theres no common id eg: plug_id 554. etc

  records_temp = []
  for i in range(len(old)):
    a = 0
    for j in range(len(new)):
      if old[i][id_index] == new[j][0]:
        records_temp +=  [old[i]+new[j][1:]]
        a = 1

    if a == 0 :
      records_temp +=  [old[i]]



      #finds len of record with most variables. for purpose of padding
    max_len = 0
    for i in range(len(records_temp)):
        if max_len < len(records_temp[i]) :
          max_len =  len(records_temp[i])

    for i in range(len(records_temp)):
       records_temp[i] += ['']*(max_len-len(records_temp[i]))
    #pads the records. assumes record with most variables is correct

  return records_temp

def data_strat_groups(records):
  #creates a list of strat groups from data set
  #strat_groups needed later when converting custom input

  strat_groups = [""]
  for i in range( len(records)):
      if (records[i][6]) not in strat_groups :
        strat_groups += [records[i][6]]
  return strat_groups


def data_parse(records):

  for i in range(len(records)):
    for j in range(len(records[0])):
      try:

        records[i][j] = float(records[i][j].replace(',', '.'))
      except ValueError:
        continue


  strat_groups = data_strat_groups(records)
  for i in range( len(records)):
     records[i][6] = (strat_groups.index(records[i][6]))
# replaces strat_group with an intiger (1-37)
#0 = no strat group....

  for i in range(len(records)):
    for j in range(len(records[0])):
      if j == 1 :
        #keeps the name of the well intact
        continue
      elif type(records[i][j]) == str :
        records[i][j] = ""
        #converts all #value! and other errors in data to empty data


  return records


def data_extract(record):
   # [latitude,longitude,depth, strat-group, a, b, c, d, e, f]
# [2,3,5,6,7,8,9,10,11,12]
  record= record[2:4]+record[5:]

  return record


def data_scope(records):
  #------------computes min / max values to estimate a variable range

  min_list = [99999]*len(records[0])
  max_list = [-1111]*len(records[0])


  for i in range(len(records)) :
   # print (records[i])

    for j in range (len(records[0])):


        if records[i][j] == "" :
          continue
        elif type(records[i][j]) == type('a') :
          continue
        elif records[i][j] < min_list[j] :
          min_list[j] = records[i][j]
        elif records[i][j] > max_list[j] :
          max_list[j] = records[i][j]


  return min_list,max_list



