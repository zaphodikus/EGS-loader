#
# "C:\ssd\Steam\SteamApps\common\Empyrion - Galactic Survival\Content\Configuration\Config.ecf"
# "C:\ssd\Steam\SteamApps\common\Empyrion - Galactic Survival\Content\Configuration\Config_Example.ecf"
# "C:\ssd\Steam\SteamApps\common\Empyrion - Galactic Survival\Content\Configuration\TraderNPCConfig.ecf"
# https://empyrion.gamepedia.com/Game_API_tuts_configecf
import re

def find_ecf_value_MoneyCard(output):
    # expr = \{\s*(?:(?!Name).)*Name:[ ]*MoneyCard(?:(?!StackSize:|\})(?:.|\n))*StackSize:[ ]*([0-9]*)
    x = re.search("\\{\\s*(?:(?!Name).)*Name:[ ]*MoneyCard(?:(?!StackSize:|\\})(?:.|\\n))*StackSize:[ ]*([0-9]*)", output)
    if x:
        print(x.group(1))


def load_ecf(config_file = "C:\\ssd\\Steam\\SteamApps\\common\\Empyrion - Galactic Survival\\Content\\Configuration\\Config_Example.ecf", debug = False):
    output = open(config_file,'r').read()
    ecfimport = {}      #Allow for String => int lookup
    ecfimportOrig = {}  #Allow for int => string lookup for blocks only
    ecfImportTrader = {}    # Traders
    ecfImportFaction = {}   # Names
    ecfImportScenario = {}  # Faction scenario
    ecfImportUnit = {}      # Faction units

    st = output.split('{')
    for ss in st:
        #print(ss)
        te = -1
        ts = ""
        trader_ID = ""
        faction_name = ""
        faction_scenario = ""
        faction_unit = ""
        sb = re.split(",|\n",ss)
        for se in sb:
            #print(se)
            if te == -1 and se.__contains__("Id:"):
                #print("[ID] {0}".format(se))
                try:
                    te = int(se.split(':')[1].strip())
                except Exception as e: # TODO: gobble handle numberic parse errors here
                    print("Exception:{0}".format(e))
            elif ts == "" and se.__contains__("Name:"):
                #print("[NAME] {0}".format(se))
                try:
                    ts = se.split(':')[1].strip()
                    if se.__contains__("Trader "):  # Traders don't have block id's
                        te = 1
                        trader_ID = ts
                except Exception as e: # TODO: gobble handle text/alphabetics type errors here
                    print("Exception:{0}".format(e))
            if te != -1 and ts != "":
                break
        if te != -1 and ts != "":
            if ts.lower().strip() in ecfimport.keys():
                if debug:
                    print("key collision/duplicate: {0} with {1}".format(ts,te))
            else:
                if trader_ID != "":
                    ecfImportTrader[trader_ID] = sb  # Traders have no ID, just dump their data in here for now
                else:
                    ecfimport[ts.lower().strip()] = te
                    ecfimportOrig[te] = ts.lower().strip()
    if debug:
        print("ECF loaded: {0}".format(config_file))
    if len(ecfImportTrader.keys()):
        return  ecfImportTrader
    elif len(ecfImportFaction.keys()):
        return (ecfImportFaction,ecfImportScenario,ecfImportUnit)
    else:
        return (ecfimport, ecfimportOrig)