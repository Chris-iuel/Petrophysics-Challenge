from data_handler import *
from data_encoder import *
from data_setup import *
from pool_setup import *
from pool_main import *
import json


#Spatial Neural Network 
#	by Christopher Iuel

#NOTE Testing assumes a,b,c are located at index 399-699
# Choice (2)
#NOTE negative trends in g value is not included (neg sign is ignored)

#TODO
#Analyse number of active collumns and cells.
#concider using boosting to inc efficiency off network
#Is main_std redundant after menu implementation?
#disp training counter by increments of 10 to reduce lag caused by display
#make it a choice which records to test against
#a,b,c estimation needed
#translate estimation from record to numbers



def main_testing (pool,threshold,record,index,enc_val) :
#index = index of variable being estimated
#innefficient.. Runst this each time it estimates a value. even if it is from the same collumn.

        start = 0
        for i in range(0,index) :
          #calc start index based on n values in enc_val
          start += enc_val[i][0]
        stop = start + enc_val[index][0]

        act_cell = main_test(pool, threshold, record)
        index_list = training_index(act_cell)
        index_winner = index_list.index(1)
        temp_list = [0] * len(pool[0])

        for i in range(0, len(pool[index_winner])):
          if pool[index_winner][i] >= threshold:
                    temp_list[i] = 1
          elif pool[index_winner][i] > 0 :
                    temp_list[i] = 0

        length_guess = 0
        #guess_list = [length of 1's(certainty), value]
        guess_list = [0,""]

        # [latitude,longitude,depth, strat-group, a, b, c, d, e, f]
        #enc_val =    [[n,w,minVal,maxVal,rangeVal,numBuckets]]'

        #out = floor( numBuckets*(input_value-minVal) / rangeVall )
        #[[n,w,minVal,maxVal,rangeVal,numBuckets]]
        # input_enc = floor( numBuckets*(input_val-minVal) / rangeVall )
        # input_val = (input_enc*range_val)/numBuck + minVal

        for i in range(start,stop):
          #finds number of collective 1's. This signifies certainty of guess
          if  (temp_list[i] == 1):
            length_guess += 1
          else:
            if length_guess > guess_list[0] :
              #converts list of 1's to values

              y = (i--int(length_guess/2) - start)
              x = ((y/enc_val[index][4])/enc_val[index][5]) + enc_val[index][2]
              guess_list[1] =  x
              guess_list[0] = length_guess
              length_guess = 0
        return guess_list


def main_setup_std():

   data,min_list,max_list= data_setup_std()
   enc_val =  enc_setup_std(data,min_list,max_list)
   input_enc = []

   for i in range(len(data)) :
      a = []

      for j in range(len(data[0])) :
        a+= scalar_encoder(data[i][j], enc_val[j])
      input_enc += [a]

   max_col,threshold,pool_spec = pool_setup_std(len(input_enc[0]))
   pool = create_pool(pool_spec)

   return max_col,threshold,pool,input_enc,enc_val
#enc val contains enc vals for each variable in a record.
# encode each variable with its enc val and then add the encodings together into one enc per record.
#need to differentiate between a value of "" and a value of 0


def main_training(max_col,threshold,pool,input_enc):
  act_cell = main_test(pool, threshold, input_enc)
  index_list = training_index(act_cell)
  pool = training(index_list, pool, max_col, input_enc)
  return pool



def main_std():
  max_col,threshold,pool,input_enc = main_setup_std()
  count = 0
  for ITEM in input_enc :
    count += 1
    pool = main_training(max_col,threshold,pool,ITEM)
    print (count)


def main_menu():
  choice = 0
  test_range = 0
  trained = 0
  accuracy = 0
  network_bool = 0
  record = 0

  while (choice != -1):
    print()
    print("1)  Setup network and encode input")
    print("        Created: ", network_bool)
    print("2)  Split input training/testing")
    print("        Records:",test_range)
    print("3)  Train network")
    print("        Times trained:", trained)
    print("4)  Test network")
    print("        Record num:",record)
    print("        Accuracy:", accuracy)
    print("5) Save network")
    print("6) Load network")
    print("7) Train over night")
    print("-1) Exit")
    print()
    try:
      choice = int(input("Select:"))
    except:
      choice = 0
    if choice  == 1:
      max_col,threshold,pool,input_enc,enc_val = main_setup_std()
      network_bool = 1


    elif choice == 2:

      str_temp =  "Range(0-" + str(len(input_enc)-1) + "):"
      test_start = int(input(str_temp))
      str_temp = "End index(" + str(test_start + 1) + "-" + str(len(input_enc)) + "):"
      test_end =  int(input(str_temp))
      test = input_enc[test_start : test_end]
      input_enc_temp =list( input_enc[0:test_start] + input_enc[test_end: ])
      input_enc = input_enc_temp
      test_range = len(test)

      test_answer = [0]*len(test)
      for i in range(len(test)):
        test_answer[i]  = test[i][399:700]
        for j in range(399,700):
          test[i][j] = 0


    elif choice == 3:
        count = 0
        for ITEM in input_enc :
          count += 1
          pool = main_training(max_col,threshold,pool,ITEM)
          if (count%10) == 0:
            print (count," / ",len(input_enc))

        trained += 1

    elif choice == 4:
        temp_str = "Select record(0-" + str(test_range-1) + ")"
        record = int(input(temp_str))
        act_cell = main_test(pool, threshold, test[record])
        index_list = training_index(act_cell)
        index = index_list.index(1)

        temp_list = [0] * len(pool[0])
        for i in range(0, len(pool[index])):
          if pool[index][i] >= threshold:
                    temp_list[i] = 1
          elif pool[index][i] > 0 :
                    temp_list[i] = 0
        print("")
        print("Record: ",record)

        #print(temp_list)
        #print (input_enc[record])

        overlap = 0
        length_guess = 0
        index = 0
        #guess_list = [length of 1's(certainty), value]
        guess_list = [0,0]
        j = 0
        t = 0

        # [latitude,longitude,depth, strat-group, a, b, c, d, e, f]
        #399-700 is the location of the abc variables
        #enc_val =    [[n,w,minVal,maxVal,rangeVal,numBuckets]]'
        #enc_val[4]= a
        #enc_val[6] = c
        #enc_val[5][4] = min_val of b
        #enc_val =    [[n,w,minVal,maxVal,rangeVal,numBuckets]]
        #out = floor( numBuckets*(input_value-minVal) / rangeVall )
        #[[n,w,minVal,maxVal,rangeVal,numBuckets]]
        # y = floor( numBuckets*(x-minVal) / rangeVall )
        # x = (y*range_val)/numBuck + minVal

        for i in range(399,700):

          #Tracks if the field encodes a,b or c
          if i <=499:
            if index != 4:
              print("")
              print("A")
            index = 4
          elif i <= 599 :
            if index != 5:
              print("")
              print ("B")
            index = 5
          else :
            if index != 6:
              print("")
              print("C")
            index = 6





          #finds number of collective 1's. This signifies certainty of guess
          if  (temp_list[i] == 1):
            length_guess += 1
          else:
            if length_guess > guess_list[0] :
              #converts list of 1's to values
              y = (i--int(length_guess/2) - 399)
              x = ((y/enc_val[index][4])/enc_val[index][5]) + enc_val[index][2]
              length_guess = 0
              guess_list[1] =  x


          j += 1
          if j %100 == 0 :
            j = 0
            t = 0
            print("Estimate:",guess_list[1])
            guess_list[0] = 0
            guess_list[1] = 0




          if (test_answer[record][i-399] == 1) and (t == 0):
              y = (i--int(5/2) - 399)
              x = ((y/enc_val[index][4])/enc_val[index][5]) + enc_val[index][2]
              print("Answer:", x)
              t = 1



    elif choice == 5:
      f = open('Network.json', 'w')
      json.dump(pool, f)
      f.close()
      print("Saved...")

    elif choice == 6:
      f = open('Network.json', 'r')
      pool = json.load(f)
      f.close()
      print("Loaded...")

    elif choice == 7:
        trained = 0
        saved = 0

        while 1:
          print("Trained:",trained)
          print("Saved:",saved)
          count = 0
          for ITEM in input_enc :
            count += 1
            pool = main_training(max_col,threshold,pool,ITEM)
            if (count%100) == 0:
              print (count," / ",len(input_enc))

          trained += 1
          if (trained % 3) == 0:
                  str_f = "Network"+str(saved)+".json"
                  f = open(str_f, 'w')
                  json.dump(pool, f)
                  f.close()
                  print("Saved...")
                  saved += 1

#main_menu()
#print("End...")
