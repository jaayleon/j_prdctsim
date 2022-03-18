""" Bill of Materials Generator

Generates suedo products Bill of Materials (BoM) with two layers of materials used for testing 'j_prdctsim.bom'.
20 baseline products are randomly generated with 50 first and second layer compoents
(denoted as L1 and L2 respectively).

Author: J Leon Batulayan <jleon.batulayan@gmail.com>

Created: 25th February, 2022
"""
import os
import numpy as np
import pandas as pd


# GENERATE PRODUCTS
size_products = 21
products = []
for i in range(size_products):
    num = str(i)
    zeroes = 3 - len(num)
    serial = "000"[:zeroes] + num
    products.append("PROD" + serial)

ProductSKUs = pd.DataFrame(data = products, columns=["SKU"])


# GENERATE LAYER1 COMPONENTS
size_L1_components = 50
L1_components = []
for i in range(size_L1_components):
    num = str(i)
    zeroes = 3 - len(num)
    serial = "000"[:zeroes] + num
    L1_components.append("L1" + serial)

L1SKUs = pd.DataFrame(data = L1_components, columns=["SKU"])


# GENERATE LAYER2 COMPONENTS
size_L2_components = 50
L2_components = []
for i in range(size_L2_components):
    num = str(i)
    zeroes = 3 - len(num)
    serial = "000"[:zeroes] + num
    L2_components.append("L2" + serial)

L2SKUs = pd.DataFrame(data = L2_components, columns=["SKU"])


#GENERATE BOMSTRUCTURE
BoMStructure = pd.DataFrame(columns=["Parent", "Component", "QtyPer"])


# Size and indicies of 1st layer SKUs
np.random.seed(0)
num_product_comps = np.random.randint(3,10, size=size_products)
np.random.seed(1)
L1_inds = np.random.randint(0,size_L1_components, size=sum(num_product_comps))

# QtyPer for 1st layer as rational numbers in range [0.1, 10]
np.random.seed(2)
prod_qp_numerators = np.random.randint(1,10, size=sum(num_product_comps))
np.random.seed(3)
prod_qp_denominators = np.random.randint(1,10, size=sum(num_product_comps))
prod_qty_pers = np.around(prod_qp_numerators/prod_qp_denominators, 3)

# Size and indicies of 2nd layer SKUs
np.random.seed(4)
num_L1_comps = np.random.randint(2,5, size=size_L1_components)
np.random.seed(5)
L2_inds = np.random.randint(0,size_L2_components, size=sum(num_L1_comps))

# QtyPer for 2nd layer as rational numbers in range [0.1, 10]
np.random.seed(6)
L1_qp_numerators = np.random.randint(1,10, size=sum(num_L1_comps))
np.random.seed(7)
L1_qp_denominators = np.random.randint(1,10, size=sum(num_L1_comps))
L1_qty_pers = np.around(L1_qp_numerators/L1_qp_denominators, 3)

# Product : Layer1
prod_comp_ind = 0
for i in range(size_products):
    parent = products[i]
    num_comps = num_product_comps[i]

    for j in range(num_comps):
        component = L1_components[L1_inds[prod_comp_ind]]
        qty_per = prod_qty_pers[prod_comp_ind]
        prod_comp_ind += 1
        temp = pd.DataFrame(
            data=[[parent, component, qty_per]],
            columns=["Parent", "Component", "QtyPer"]
            )
        BoMStructure = pd.concat([BoMStructure, temp], ignore_index=True)

# Layer1 : Layer2
L1_comp_ind = 0
for i in range(size_L1_components):
    parent = L1_components[i]
    num_comps = num_L1_comps[i]

    for j in range(num_comps):
        component = L2_components[L2_inds[L1_comp_ind]]
        qty_per = L1_qty_pers[L1_comp_ind]
        L1_comp_ind += 1
        temp = pd.DataFrame(
            data=[[parent, component, qty_per]],
            columns=["Parent", "Component", "QtyPer"]
            )
        BoMStructure = pd.concat([BoMStructure, temp], ignore_index=True)


# IRREGULAR LAYER CASE (Manually inputted)

# First layer L2 component (1)
irregular_1 = pd.DataFrame(
    data=[[products[2], L2_components[13], 0.5]], 
    columns=["Parent", "Component", "QtyPer"]
    )

# First layer L2 component (2)
irregular_2 = pd.DataFrame(
    data=[[products[15], L2_components[13], 1]], 
    columns=["Parent", "Component", "QtyPer"]
    )

# Second layer L1 component
irregular_3 = pd.DataFrame(
    data=[[L1_components[25], L1_components[4], 0.4]], 
    columns=["Parent", "Component", "QtyPer"]
    )

BoMStructure = pd.concat([BoMStructure, irregular_1, irregular_2, irregular_3], ignore_index=True)

# EXPORT TEST DATA

BoMStructure.to_csv(os.path.join(os.getcwd(), "test_data", "test_BoMStructure.csv"), index=False)
ProductSKUs.to_csv(os.path.join(os.getcwd(), "test_data", "test_ProductSKUs.csv"), index=False)
L1SKUs.to_csv(os.path.join(os.getcwd(), "test_data", "test_Layer1SKUs.csv"), index=False)
L2SKUs.to_csv(os.path.join(os.getcwd(), "test_data", "test_Layer2SKUs.csv"), index=False)
