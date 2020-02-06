#
# "C:\ssd\Steam\SteamApps\common\Empyrion - Galactic Survival\Content\Configuration\Config.ecf"
# "C:\ssd\Steam\SteamApps\common\Empyrion - Galactic Survival\Content\Configuration\Config_Example.ecf"
# "C:\ssd\Steam\SteamApps\common\Empyrion - Galactic Survival\Content\Configuration\TraderNPCConfig.ecf"
# https://empyrion.gamepedia.com/Game_API_tuts_configecf
import re
from enum import Enum

def find_ecf_value_MoneyCard(output):
    # expr = \{\s*(?:(?!Name).)*Name:[ ]*MoneyCard(?:(?!StackSize:|\})(?:.|\n))*StackSize:[ ]*([0-9]*)
    x = re.search("\\{\\s*(?:(?!Name).)*Name:[ ]*MoneyCard(?:(?!StackSize:|\\})(?:.|\\n))*StackSize:[ ]*([0-9]*)", output)
    if x:
        print(x.group(1))


class ALine:
    """
    Keep track of text line numbers internally.
    """
    def __init__(self, text, number=1):
        self.text = text.lstrip()
        self.line = number
        self.ignore = len(self.text) == 0 or self.text[0] == '#'

    def __repr__(self):
        if self.ignore: return ""
        return f'{self.text}'


# class to define the kinds of ecf file we cater for
class ECFType(Enum):
    AutoDetect=0
    Config=1    # Config_example/Config
    Trader=2    # TraderNPCConfig
    Faction=3   # FactionWarfare
    EGroup=4   # EGroupsConfig
    Reputation=5  # DefReputation
    Shapes=6    # BlockShapesWindow

class ECFException(Exception):
    """base class to define the parser exceptions we support"""
    pass

class ECFCollision(ECFException):
    def __index__(self, a, b, msg="ECF key collision"):
        super().__init__(msg)
        _context = a + b


class ECFExpectedInteger(ECFException):
    def __index__(self, context=None, msg="ECF expected an integer"):
        super().__init__(msg)
        _context = context

class ECFExpectedString(ECFException):
    def __index__(self, context=None, msg= "ECF expected a string"):
        super().__init__(msg)
        _context = context

def load_ecf(config_file = "C:\\ssd\\Steam\\SteamApps\\common\\Empyrion - Galactic Survival\\Content\\Configuration\\Config_Example.ecf", type=ECFType.AutoDetect, debug = False):
    """
    Returns a dictionary, or a dictionary tupple depending on which file we parse. The records are plain text, and do
    not get parsed yet.
    """
    output = open(config_file,'r').read()
    ecfimport = {}      #Allow for String => int lookup
    ecfimportOrig = {}  #Allow for int => string lookup for blocks only
    ecfImportTrader = {}    # Traders
    ecfImportFaction = {}   # Names
    ecfImportScenario = {}  # Faction scenario
    ecfImportUnit = {}      # Faction units
    ecfImportGroup = {}
    ecfImportReputation = {}

    version = re.search("VERSION:\\s([\\d]*)", output) # only in the Config.ecf file
    if version:
        version = version.group(1)
    outputlines = output.split('\n')
    outputclean=""
    for line in outputlines:
        if len(line) and line[0] != '#':
            outputclean+=line + '\n'
    st = outputclean.split('{')
    for ss in st:
        #print(ss)
        te = -1
        ts = ""
        trader_ID = ""
        faction_name = ""
        faction_scenario = ""
        faction_unit = ""
        egroup_name = ""
        reputation_name = ""
        sb = re.split(",|\n",ss)
        for se in sb:
            # print(se)

            if te == -1 and se.__contains__("Id:"):
                #print("[ID] {0}".format(se))
                try:
                    te = int(se.split(':')[1].strip())
                    if se.__contains__("Block ") and type==ECFType.AutoDetect:  # autodetect logic
                        type = ECFType.Config
                except Exception as e: # TODO: gobble handle numberic parse errors here
                    print("Exception:{0}".format(e))
                    raise ECFExpectedInteger(str(e))
            elif ts == "" and se.__contains__("Name:"):
                #print("[NAME] {0}".format(se))
                try:
                    ts = se.split(':')[1].strip()
                    if se.__contains__("Trader "):  # Traders don't have block id's
                        if type == ECFType.AutoDetect:  # autodetect logic
                            type = ECFType.Trader
                        te = 1
                        trader_ID = ts
                    elif se.__contains__(" FactionSettings"):  # Faction name
                        if type == ECFType.AutoDetect:  # autodetect logic
                            type = ECFType.Faction
                        te = 1
                        faction_name = re.search(".*Faction:\\s([a-zA-Z]*)", ss).group(1)
                    elif se.__contains__(" Unit"):  # unit class
                        te = 1
                        faction_unit = re.search(".*ClassName:\\s([a-zA-Z]*)", ss).group(1)
                    elif se.__contains__(" Scenario"):  # unit class
                        te = 1
                        m = re.findall(".*\\sName:\\s([a-zA-Z0-9\\d]*)", ss)
                        faction_scenario = m[1] # second match in a findall
                    elif se.__contains__(" EGroup"): # EGroup
                        if type == ECFType.AutoDetect:  # autodetect logic
                            type = ECFType.EGroup
                        te = 1
                        m = re.findall(".*\\sName:\\s([a-zA-Z0-9\\d]*)", ss)
                        egroup_name = m[0]
                    elif se.__contains__(" Reputation"): # EGroup
                        if type == ECFType.AutoDetect:  # autodetect logic
                            type = ECFType.Reputation
                        te = 1
                        m = re.findall(".*\\sName:\\s\"([a-zA-Z0-9\\d:]*)\"", ss)
                        reputation_name = m[0]

                except Exception as e: # TODO: gobble handle text/alphabetics type errors here
                    print("Exception:{0}".format(e))
                    raise ECFExpectedString(str(e))
            if te != -1 and ts != "":
                break
        if te != -1 and ts != "":
            if ts.lower().strip() in ecfimport.keys():
                if debug:
                    print("key collision/duplicate: {0} with {1}".format(ts,te))
                    raise ECFCollision(ts,te)
            else:
                if trader_ID != "":
                    ecfImportTrader[trader_ID] = sb  # Traders have no ID, just dump their data in here for now
                elif faction_name != "":
                    ecfImportFaction[faction_name] = sb  # faction name
                elif faction_scenario != "":
                    ecfImportScenario[faction_scenario] = sb  # faction scenario
                elif faction_unit != "":
                    ecfImportUnit[faction_unit] = sb # faction unit
                elif egroup_name != "":
                    ecfImportGroup[egroup_name] = sb  # EGroup
                elif reputation_name != "":
                    ecfImportReputation[reputation_name] = sb  # EGroup
                else:
                    ecfimport[ts.lower().strip()] = te
                    ecfimportOrig[te] = ts.lower().strip()
    if debug:
        print("ECF loaded: {0}".format(config_file))

    if ECFType.Trader == type:
        return  ecfImportTrader
    elif ECFType.Faction == type:
        return (ecfImportFaction,ecfImportScenario,ecfImportUnit)
    elif ECFType.EGroup == type:
        return ecfImportGroup
    elif ECFType.Reputation == type:
        return ecfImportReputation
    else:
        return (ecfimport, ecfimportOrig)