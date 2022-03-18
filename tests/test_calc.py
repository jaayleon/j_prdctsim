from cgi import test
from unittest import expectedFailure
import pytest
import j_prdctsim.calc 
import numpy as np
import pandas as pd
import os


@pytest.fixture
def load_bom():
    BomStructure = pd.read_csv(os.path.join(os.getcwd(), "data", "test_data", "test_BomStructure.csv"))
    return BomStructure
 
@pytest.fixture
def load_skus():
    ProductSKUs = pd.read_csv(os.path.join(os.getcwd(), "data", "test_data", "test_ProductSKUs.csv"))
    return ProductSKUs

def test_load_bom(load_bom):
    df = load_bom
    assert df.shape == (282,3)
    assert df.notnull().values.any() == True, print(df.type())

def test_load_skus(load_skus):
    df = load_skus
    assert df.shape == (21,1)
    assert df.notnull().values.any() == True, print(df.type())

# Test trivial case: Similarity proportion with itself should be 1
def test_ravisim_trivial_case(load_bom, load_skus):
    bom = load_bom.to_numpy()
    skus = load_skus.to_numpy().reshape(-1)
    expected = 1.0
    sku_count = 0
    for sku in skus:
        output = j_prdctsim.calc.ravisim(sku, sku, bom)
        assert output == expected, f"For trivial case of item {sku}, ravisim calculates a proportion of {output}"
        # Note that the inverse is trivial for this case
        sku_count += 1   
    assert sku_count == len(skus)

# Test Similarity with sku not in Bill of Materials: Expected proportion is 0
def test_ravisim_sku_not_in_bom(load_bom, load_skus):
    bom = load_bom.to_numpy()
    skus = load_skus.to_numpy().reshape(-1)
    expected = 0
    sku_count = 0
    for sku in skus:
        output = j_prdctsim.calc.ravisim(sku, "SAMPLE_SKU", bom)
        inv_output = j_prdctsim.calc.ravisim("SAMPLE_SKU", sku, bom)
        assert output == expected, f"For case of item {sku} with an item not in the BoM, ravisim calculates a proportion of {output} while {expected} was expected"
        assert inv_output == expected, f"For the inverse case of item {sku} with an item not in the BoM, ravisim calculates a proportion of {inv_output} while {expected} was expected"
        sku_count += 1   
    assert sku_count == len(skus)

def test_ravisim_PROD000_PR001(load_bom):
    bom = load_bom.to_numpy()
    sku1 = "PROD000"
    sku2 = "PROD001"
    expected = 0.11
    output = j_prdctsim.calc.ravisim(sku1, sku2, bom)
    inv_output = j_prdctsim.calc.ravisim(sku2, sku1, bom)
    assert output == expected, f"Between items {sku1} annd {sku2}, ravisim calculates a proportion of {output} while {expected} was expected"
    assert inv_output == expected, f"Between items {sku2} annd {sku1}, ravisim calculates a proportion of {inv_output} while {expected} was expected"

def test_ravisim_PROD000_PR010(load_bom):
    bom = load_bom.to_numpy()
    sku1 = "PROD000"
    sku2 = "PROD010"
    expected = 0.07
    output = j_prdctsim.calc.ravisim(sku1, sku2, bom)
    inv_output = j_prdctsim.calc.ravisim(sku2, sku1, bom)
    assert output == expected, f"Between items {sku1} annd {sku2}, ravisim calculates a proportion of {output} while {expected} was expected"
    assert inv_output == expected, f"Between items {sku2} annd {sku1}, ravisim calculates a proportion of {inv_output} while {expected} was expected"


def test_ravisim_PROD000_PR016(load_bom):
    bom = load_bom.to_numpy()
    sku1 = "PROD000"
    sku2 = "PROD016"
    expected = 0.01
    output = j_prdctsim.calc.ravisim(sku1, sku2, bom)
    inv_output = j_prdctsim.calc.ravisim(sku2, sku1, bom)
    assert output == expected, f"Between items {sku1} annd {sku2}, ravisim calculates a proportion of {output} while {expected} was expected"
    assert inv_output == expected, f"Between items {sku2} annd {sku1}, ravisim calculates a proportion of {inv_output} while {expected} was expected"

def test_ravisim_PROD001_PR002(load_bom):
    bom = load_bom.to_numpy()
    sku1 = "PROD001"
    sku2 = "PROD002"
    expected = 0.08
    output = j_prdctsim.calc.ravisim(sku1, sku2, bom)
    inv_output = j_prdctsim.calc.ravisim(sku2, sku1, bom)
    assert output == expected, f"Between items {sku1} annd {sku2}, ravisim calculates a proportion of {output} while {expected} was expected"
    assert inv_output == expected, f"Between items {sku2} annd {sku1}, ravisim calculates a proportion of {inv_output} while {expected} was expected"

def test_ravisim_PROD007_PR013(load_bom):
    bom = load_bom.to_numpy()
    sku1 = "PROD007"
    sku2 = "PROD013"
    expected = 0.06
    output = j_prdctsim.calc.ravisim(sku1, sku2, bom)
    inv_output = j_prdctsim.calc.ravisim(sku2, sku1, bom)
    assert output == expected, f"Between items {sku1} annd {sku2}, ravisim calculates a proportion of {output} while {expected} was expected"
    assert inv_output == expected, f"Between items {sku2} annd {sku1}, ravisim calculates a proportion of {inv_output} while {expected} was expected"

