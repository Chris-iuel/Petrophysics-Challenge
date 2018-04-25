import tkinter as tk
from easygui import *
from data_handler import *

def gui_menu  (options,msg):



  title = "NN Interface"

  option   = choicebox(msg, title, options)
  return option


def gui_record_collect(record):

  msg = "Custom Input"
  title = "NN Interfacee"
  fieldNames = ["Latitude:","Longitude:","Depth:","Stratigraphic Group:"," a"," b"," c"," d"," e"," f"," g"," h"," i"," j"," k"," l"," m"," n"," o"," p"]
  fieldValues = record
  fieldValues = multenterbox(msg,title, fieldNames,fieldValues)

  #parses input
  strat_groups = ['','HELIUM', 'LITHIUM', 'BERYLLIUM', 'BORON', 'CARBON', 'NITROGEN', 'HYDROGEN', 'MANGANESE', 'COBALT', 'RUBIDIUM', 'OXYGEN', 'FLUORINE', 'NEON', 'SODIUM', 'ALUMINIUM', 'SILICON', 'PHOSPHORUS', 'SULFUR', 'CHLORINE', 'ARGON', 'POTASSIUM', 'CALCIUM', 'CHROMIUM', 'IRON', 'VANADIUM', 'TITANIUM', 'SCANDIUM', 'NICKEL', 'COPPER', 'ZINC', 'GALLIUM', 'GERMANIUM', 'ARSENIC', 'BROMINE', 'KRYPTON', 'STRONTIUM']

  for i in range(len(fieldValues)) :
    if  i == 3:
      #converts strat group into value
      try:
        fieldValues[i] = strat_groups.index(str(fieldValues[i])) +1
        continue
      except:
        try:
          fieldValues[i] = int(fieldValues[i])
          if fieldValues[i] > len(strat_groups):
            fieldValues[i] = ""
        except :
          fieldValues[i] = ""
    else:
      try:
        fieldValues[i] = float(fieldValues[i])
      except:
        fieldValues[i] = ""
  return fieldValues


