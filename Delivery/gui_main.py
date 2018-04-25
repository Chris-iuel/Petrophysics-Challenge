from data_handler import *
from data_encoder import *
from data_setup import *
from pool_setup import *
from pool_main import *
from main import *
from gui import *
import json

#Spatial Neural Network 
#	by Christopher Iuel


msg ="Record".ljust(39)+"Overlap(%)".ljust(5)+"Range(+-)"
msg_record_str = ""
msg_record = ["\nLatitude: ","\nLongitude: ","\nDepth: ","\nStratigraphic Group: ","\na: ","\nb: ","\nc: ","\nd: ","\ne: ","\nf: ","\ng:","\nh;","\ni:","\nj:","\nk:","\nl:","\nm:","\nn:","\no:","\np:"]
msg_record_certainty = [0]*20
msg_record_uncertainty = [0]*20
options = ["Setup", "Input", "Estimate", "Help","Exit"]
record = [""]*20
choice = 0
a = [0,""]
#enc val contains the encoding properties of each variable.
#enc val = [[n,w,min,max,range]]
enc_val = [[100, 5, 56.2395, 71.5861, 15.346600000000002, 96], [100, 5, 1.9301, 20.4417, 18.5116, 96], [100, 5, 1280.49, 3962.83, 2682.34, 96], [100, 5, 1, 37, 36, 96], [100, 5, 1.03, 15.63, 14.600000000000001, 96], [100, 5, 2.5, 4.04, 1.54, 96], [100, 5, 0.08, 0.56, 0.48000000000000004, 96], [100, 5, 1.99, 6550.0, 6548.01, 96], [100, 5, 0.53, 5.14, 4.609999999999999, 96], [100, 5, 0.0, 28450.63, 28450.63, 96], [100, 5, 0.04, 3.01, 2.9699999999999998, 96], [100, 5, 1.28, 79.9, 78.62, 96], [100, 5, 0.11, 3.31, 3.2, 96], [100, 5, 0.0, 153.0, 153.0, 96], [100, 5, 0.03, 75.65, 75.62, 96], [100, 5, 0.76, 671.43, 670.67, 96], [100, 5, -414.0, 1400.0, 1814.0, 96], [100, 5, 0.05, 1.04, 0.99, 96], [100, 5, 0.15, 1169.37, 1169.2199999999998, 96], [100, 5, 0.01, 14387.39, 14387.38, 96]]



while choice != -1:

  msg_record_str = ""
  for i in range(len(record)) :
    msg_record_uncertainty[i] = (enc_val[i][4]/enc_val[i][0])*(msg_record_certainty[i]/2)
    msg_record_str+=(str(msg_record[i]) + str(record[i])).ljust(40) + ("("+str((msg_record_certainty[i]/5)*100)+"%)").ljust(10) + "("+ str(msg_record_uncertainty[i])+")"
  choice = gui_menu(options,(msg+msg_record_str))

  if choice == options[0]:
      f = open('Network10.json', 'r')
      pool = json.load(f)
      f.close()
      msg+="\nNN Loaded..."
      threshold = 0.6

      #enc val contains the encoding properties of each variable.
      #enc val = [[n,w,min,max,range]]

  elif choice == options[1]:
    record = gui_record_collect(record)
    print(record)
    msg_record_str = ""
    for i in range(len(record)) :
      msg_record_str+= str(msg_record[i]) + str(record[i])

  elif choice == options[2]:
      input_enc = []
      for i in range(len(record)) :
        input_enc += scalar_encoder(record[i], enc_val[i])
      index = 0
      for index in range(len(record)):
        if record[index] == "":
          a = main_testing (pool,threshold,input_enc,index,enc_val)
          record[index] = a[1]
          msg_record_certainty[index] = a[0]




  elif choice == options[3]:
        msg_help = ["Stratigraphic Groups must be typed in capital letters.\nDecimal values are marked with a period, not a comma.\nSetup must be run before estimation.\nAtleast one input must be entered before estimation.\n\n"]
        msg = msg_help[0]

  elif choice == options[-1]:
    choice = -1

