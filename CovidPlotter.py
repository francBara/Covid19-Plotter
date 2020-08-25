import json
from sys import argv
import matplotlib.pyplot as plt
import numpy as np

def CollectNationData(data_file, dataType):
    data = []
    dates = []

    for i in range(len(data_file)):
        data.append(data_file[i][dataType])
        dates.append(data_file[i]["data"])

    return data, dates

def CollectRegionData(region, data_file, dataType):
    data = []
    dates = []
    i = 0

    region = region.lower()

    for j in data_file:
        j["denominazione_regione"] = j["denominazione_regione"].lower()

    if (not region in CheckRegions(data_file)):
        print("Region not recognized")
        print("Use -r command to see the list of available regions")
        exit()

    while (i < len(data_file) and data_file[i]["denominazione_regione"] != region):
        i += 1

    while (i < len(data_file)):
        data.append(data_file[i][dataType])
        dates.append(data_file[i]["data"])
        i += 21

    return data, dates

#Represents the increment of the curve for an ever increasing set of data
def DataIncrement(data):
    new_data = []
    tmp = 0

    for d in data:
        new_data.append(d - tmp)
        tmp = d

    return new_data
   
def divide_data_set(data1, data2):
    new_data = []

    for i in range(len(data1)):
        if (data2[i] == 0):
            data2[i] = 1
        new_data.append(data1[i] / data2[i])

    return new_data

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

def PlotData(data, dates, label):
    plt.plot(dates, data)
    plt.xticks(np.arange(0, len(dates), 8))
    plt.ylabel(label)
    np.arange(0, len(dates), 10)
    plt.show()


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

        elif (inputLine[i] == '-a'):
            commands[1] = "A"

        elif (inputLine[i] == '-t'):
            commands[1] = "T"

        elif (inputLine[i] == '-e'):
            commands[1] = "E"

        elif (option):
            commands[0] += " "
            commands[0] += inputLine[i]

        else:
            commands[0] += inputLine[i]
            option = True
    return commands

commands = Options(argv)

if (len(argv) == 1):
    try:
        data = json.load(open("italy.json"))
    except:
        print("Json database not found, execute 'update_data.sh' to update file")
    else:
        cases, dates = CollectNationData(data, "totale_positivi")
        
        print("Current cases in Italy:",cases[-1])
        print("Last update:",DateFormat(dates)[-1])

        dates = DateFormat(dates)

        PlotData(cases, dates, "Cases")
        

elif (commands[2] == 'T'):
    print("Covid-19 plotter, shows cases per region in Italy, interfacing with the civil protection database")
    print("COMMANDS:")
    print(argv[0],"| Shows cases in all Italy")
    print(argv[0],"<REGION> | Shows cases in the chosen region")
    print("-a | Shows new cases per day")
    print("-d | Shows deaths plot")
    print("-c | Shows healed plot")
    print("-t | Shows tampons per day")
    print("-e | Shows a curve representing the cases compared to tampons")
    print("-n | Disables plot (just prints infos to screen)")
    print("-r | Shows the list of available regions")
    print("-h | Shows this screen")

elif (commands[1] == 'R'):
    try:
        data = json.load(open("regions.json"))
    except:
        print("Json database not found, execute 'update_data.sh' to update file")
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
        data = json.load(open("regions.json"))
    except:
        print("Json database not found")

    else: 
        if (commands[1] == 'D'):
            cases, dates = CollectRegionData(commands[0], data, "deceduti")
            label = "Deaths"
            print("Total deaths:",cases[len(cases)-1])
        elif (commands[1] == 'P'):
            cases, dates = CollectRegionData(commands[0], data, "totale_positivi")
            label = "Cases"
            print("Total cases:",cases[len(cases)-1])
        elif (commands[1] == 'A'):
            cases, dates = CollectRegionData(commands[0], data, "nuovi_positivi")
            label = "New Cases"
            print("Total cases:",cases[len(cases)-1])
        elif (commands[1] == 'T'):
            cases, dates = CollectRegionData(commands[0], data, "tamponi")
            total = cases[len(cases)-1]
            cases = DataIncrement(cases)
            label = "Tampons"
            print("Total tampons:",total)
        elif (commands[1] == 'H'):
            cases, dates = CollectRegionData(commands[0], data, "dimessi_guariti")
            label = "Healed"
            print("Healed:",cases[len(cases)-1])
        elif (commands[1] == 'E'):
            cases, dates = CollectRegionData(commands[0], data, "nuovi_positivi")
            tampons, dates = CollectRegionData(commands[0], data, "tamponi")
            tampons = DataIncrement(tampons)
            cases = divide_data_set(cases, tampons)
            label = "True curve"

        print("Last update:",DateFormat(dates)[-1])
    
        if (commands[2] != 'N'):
            dates = DateFormat(dates)
            
            PlotData(cases, dates, label)
else:
    print("Unknown error")
