import pytest
from egs_read import load_ecf

# 1588 objects expected
def test_numobjects_loaded_ExampleECF():
    v= load_ecf("TESTDATA\\Config_Example.ecf")
    assert len(v[0].keys()) == 1588
    assert len(v[1].keys()) == 1588

# 16 objects expected
def test_numobjects_loaded_ConfigECF():
    v= load_ecf("TESTDATA\\Config.ecf")
    assert len(v[0].keys()) == 16
    assert len(v[1].keys()) == 16

# 37 Traders expected
def test_numobjects_loaded_NPCTraderECF():
    v= load_ecf("TESTDATA\\TraderNPCConfig.ecf")
    assert len(v.keys()) == 37
    # Traders don't have ID's

# 37 Units/Factions/Scenarios
def test_numobjects_loaded_FactionECF():
    v= load_ecf("TESTDATA\\FactionWarfare.ecf")
    assert len(v[0].keys()) == 37
    assert len(v[1].keys()) == 37

# 37 Traders expected
def test_numobjects_loaded_GroupsECF():
    v= load_ecf("TESTDATA\\EGroupsConfig.ecf")
    assert len(v[0].keys()) == 37
    assert len(v[1].keys()) == 37

# 37 Traders expected
def test_numobjects_loaded_BlockShapesECF():
    v= load_ecf("TESTDATA\\BlockShapesWindow.ecf")
    assert len(v[0].keys()) == 7
    assert len(v[1].keys()) == 7

# 37 Traders expected
def test_numobjects_loaded_ReputationECF():
    v= load_ecf("TESTDATA\\DefReputation.ecf")
    assert len(v[0].keys()) == 37
    assert len(v[1].keys()) == 37
