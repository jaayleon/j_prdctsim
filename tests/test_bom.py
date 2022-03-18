from cgi import test
import pytest
import j_prdctsim.bom 
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

def test_leaf_components_qp_on_leaves(load_bom):
    """
    If we get the leaf components of a sku that is a leaf component or an item that is not a parent 
    then we get an output with the sku as itself and the qtyper as the inputted
    """
    bom = load_bom.to_numpy()
    leaf_skus = ['L2024', 'L2033', 'L2017','L2022', 'L2019', 'L2043', 'L2049', 'L2018']
    qtys = [1, 1.0, "4", 0.444, 7.875, 10000, 10000.0, 0.0001]
    
    for i in range(len(leaf_skus)):
        out = j_prdctsim.bom.leafcomponents_qp(leaf_skus[i], bom, qty=qtys[i])
        expected = np.array([[str(leaf_skus[i]), np.around(float(qtys[i]), 3)]], dtype=object)
        np.testing.assert_array_equal(out, expected)

def test_leaf_components_qp_not_in_bom(load_bom):
    """
    Test for item codes that are not present in the inputted BoM.
    The output should worl the same way it does for leaf components:
        - get an output with the sku as itself and the qtyper as the inputted
    """
    bom = load_bom.to_numpy()
    pseudo_skus = ["NEW_ITEM", 11111, 5374, "5374", "11RFH0", 77.7, "ANG7NUm", 99.99999]
    qtys = [1, 1.0, "4", 0.444, 7.875, 10000, 10000.0, 0.0001]

    for i in range(len(pseudo_skus)):
        out = j_prdctsim.bom.leafcomponents_qp(pseudo_skus[i], bom, qty=qtys[i])
        expected = np.array([[str(pseudo_skus[i]), np.around(float(qtys[i]), 3)]], dtype=object)
        np.testing.assert_array_equal(out, expected)

def test_leaf_components_qp_PROD000_qty_1(load_bom, load_skus):
    """
    Test the first product (SKU: PROD000)
    This test case includes a standard two layers as well as shared lowest layer componets (L2022, L2016, L2018, L2039)
    There has been a slight rounding error for components L2019, L2043, L2049
    """
    prod = load_skus.to_numpy().reshape(-1)[0] # SKU: PROD000
    bom = load_bom.to_numpy()
    out = j_prdctsim.bom.leafcomponents_qp(prod, bom)
    expected = np.array([
        ['L2024', 0.125],
        ['L2033',1.8],
        ['L2017',6.75],
        ['L2022',13.928],
        ['L2019',0.562], 
        ['L2043',0.644], 
        ['L2005',0.444],
        ['L2000',0.778],
        ['L2016',12.483],
        ['L2030',0.333],
        ['L2020',0.296],
        ['L2018',5.732],
        ['L2009',7.875],
        ['L2042',9.0],
        ['L2039',5.603],
        ['L2014',1.333],
        ['L2049',0.214] 
    ], dtype=object)
    sorted_expected = expected[np.argsort(expected[:,-1])]
    print(out)
    print(sorted_expected)
    np.testing.assert_array_equal(out, sorted_expected)

def test_leaf_components_qp_PROD000_qty_2(load_bom, load_skus):
    """
    Test the first product (SKU: PROD000) leaf components when we want qty=2 of the product
    This test case includes a standard two layers as well as shared lowest layer componets (L2022, L2016, L2018, L2039)
    There has been a slight rounding error for components L2019, L2043, L2049
    """
    prod = load_skus.to_numpy().reshape(-1)[0] # SKU: PROD000
    bom = load_bom.to_numpy()
    out = j_prdctsim.bom.leafcomponents_qp(prod, bom, qty=2)
    expected = np.array([
        ['L2024', 0.25],
        ['L2049', 0.429],
        ['L2020', 0.592],
        ['L2030', 0.666],
        ['L2005', 0.888],
        ['L2019', 1.125],
        ['L2043', 1.287],
        ['L2000', 1.556],
        ['L2014', 2.666],
        ['L2033', 3.6],
        ['L2039', 11.206],
        ['L2018', 11.463],
        ['L2017', 13.5],
        ['L2009', 15.75],
        ['L2042', 18.0],
        ['L2016', 24.966],
        ['L2022', 27.856]
    ], dtype=object)
    sorted_expected = expected[np.argsort(expected[:,-1])]
    print(out)
    print(sorted_expected)
    np.testing.assert_array_equal(out, sorted_expected)

def test_leaf_components_qp_PROD002_qty_1(load_bom, load_skus):
    """
    Test the third product (SKU: PROD002)
    This test case includes two irregularities: (1) an L2 component (L2013) in the first layer meaning there is
    a leaf in the first layer and (2) an L1 component in the second layer meaning there is a third layer
    """
    prod = load_skus.to_numpy().reshape(-1)[2] # SKU: PROD002
    bom = load_bom.to_numpy()
    out = j_prdctsim.bom.leafcomponents_qp(prod, bom)
    expected = np.array([
        ['L2031', 0.446],
        ['L2009', 0.536], 
        ['L2026', 1.428],
        ['L2038', 0.714],
        ['L2012', 1.714],
        ['L2015', 0.214],
        ['L2001', 1.999],
        ['L2003', 0.833],
        ['L2024', 0.333],
        ['L2033', 4.801],
        ['L2013', 0.5]
       
    ], dtype=object)
    sorted_expected = expected[np.argsort(expected[:,-1])]
    print(out)
    print(sorted_expected)
    np.testing.assert_array_equal(out, sorted_expected)

def test_edges_PROD001(load_bom, load_skus):
    """
    Test j_prdctsim.bom.edges rooted at PROD001
    """
    pass

def test_edges_PROD012(load_bom, load_skus):
    """
    Test j_prdctsim.bom.edges rooted at PROD012
    """
    prod = load_skus.to_numpy().reshape(-1)[12] # SKU: PROD012
    bom = load_bom.to_numpy()
    out = j_prdctsim.bom.edges(prod, bom)
    expected = [
        ('PROD012', 'L1003'),
        ('L1003', 'L2007'),
        ('L1003', 'L2016'),
        ('L1003', 'L2030'),
        ('PROD012', 'L1009'),
        ('L1009', 'L2009'),
        ('L1009', 'L2042'),
        ('PROD012', 'L1022'),
        ('L1022', 'L2027'),
        ('L1022', 'L2029'),
        ('L1022', 'L2033')
    ]
    assert out==expected, out

def test_edges_PROD016(load_bom, load_skus):
    """
    Test j_prdctsim.bom.edges rooted at PROD016
    """
    pass

def test_components_PROD019(load_bom, load_skus):
    """
    Test j_prdctsim.bom.components on PROD019
    """
    prod = load_skus.to_numpy().reshape(-1)[19] # SKU: PROD019
    bom = load_bom.to_numpy()
    out = j_prdctsim.bom.components(prod, bom)
    expected = [
        'L1007','L2001','L2011','L2047'
        ,'L1008','L2018','L2020','L2022','L2030'
        ,'L1013','L2004','L2046'
    ]
    assert out==expected, out

# python -m pytest tests/