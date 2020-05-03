import json
from sys import argv
import matplotlib.pyplot as plt
import numpy as np

def CollectData(region, data, dataType):
    cases = []
    dates = []
    i = 0

    region = region.lower()

    for j in data:
        j["denominazione_regione"] = j["denominazione_regione"].lower()

    if (not region in CheckRegions(data)):
        print("Region not recognized")
        print("Use -r command to see the list of available regions")
        exit()

    while (i < len(data) and data[i]["denominazione_regione"] != region):
        i += 1

    while (i < len(data)):
        cases.append(data[i][dataType])
        dates.append(data[i]["data"])
        i += 21

    return cases, dates

def CheckRegions(data):
    regions = []
    i = 0
    while (not data[i]["denominazione_regione"] in regions):
        regions.append(data[i]["denominazione_regione"])
        i += 1
    return regions

def DateFormat(dates):
    formatted = []

    for i in dates:
        tmp = ""
        j = 0
        while(j < len(i) and i[j] != '-'):
            j += 1
        j += 1
        while (j < len(i) and i[j] != '-'):
            tmp += i[j]
            j += 1
        tmp += '/'
        j += 1
        while (j < len(i) and i[j] != 'T'):
            tmp += i[j]
            j += 1
        formatted.append(tmp)
    return formatted   

def Capitalize(string):
    nu_str = ""

    nu_str = string[0].upper()

    for i in range(1, len(string)):
        nu_str += string[i]
    return nu_str


def Options(inputLine):
    commands = ["", "P", "F"]
    option = False
    for i in range(1,len(inputLine)):
        if (inputLine[i] == '-h' or inputLine[i] == 'help'):
            commands[2] = "T"

        elif (inputLine[i] == '-d'):
            commands[1] = "D"
        
        elif (inputLine[i] == '-c'):
            commands[1] = "H"

        elif (inputLine[i] == '-n'):
            commands[2] = "N"

        elif (inputLine[i] == '-r'):
            commands[1] = "R"

        elif (option):
            commands[0] += " "
            commands[0] += inputLine[i]

        else:
            commands[0] += inputLine[i]
            option = True
    return commands

commands = Options(argv)

if (len(argv) == 1):
    print("COVID-19 plotter, type '-h' for help")

elif (commands[2] == 'T'):
    print("Covid-19 plotter, shows cases per region in Italy, interfacing with the civil protection database")
    print("COMMANDS:")
    print(argv[0],"<REGION>")
    print("-d | Shows deaths plot")
    print("-c | Shows healed plot")
    print("-n | Disables plot (just prints infos to screen)")
    print("-r | Shows the list of available regions")
    print("-h | Shows this screen")

elif (commands[1] == 'R'):
    try:
        data = json.load(open("dpc-covid19-ita-regioni.json"))
    except:
        print("Json database not found")
    else:
        regions = CheckRegions(data)
        print("AVAILABLE REGIONS:")
        for i in regions:
            print(i)

elif (commands[0] != ''):
    dates = []
    cases = []
    label = ""

    try:
        data = json.load(open("dpc-covid19-ita-regioni.json"))
    except:
        print("Json database not found")

    else: 
        if (commands[1] == 'D'):
            cases, dates = CollectData(commands[0], data, "deceduti")
            label = "Deaths"
            print("Total deaths:",cases[len(cases)-1])
        elif (commands[1] == 'P'):
            cases, dates = CollectData(commands[0], data, "totale_positivi")
            label = "Cases"
            print("Current cases:",cases[len(cases)-1])
        elif (commands[1] == 'H'):
            cases, dates = CollectData(commands[0], data, "dimessi_guariti")
            label = "Healed"
            print("Healed:",cases[len(cases)-1])
    
        if (commands[2] != 'N'):
            dates = DateFormat(dates)
            
            plt.plot(dates, cases)
            plt.xticks(np.arange(0, len(dates), 8))
            plt.ylabel(label)
            np.arange(0, len(dates), 10)
            plt.show()

else:
    print("Unknown error")
