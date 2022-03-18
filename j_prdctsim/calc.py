""" Calculate the similarity between products and provide scaling

Given two product codes return a similarity proportion by calculating the overlap. A scaling function is also included

Author: J Leon Batulayan <jleon.batulayan@gmail.com>

Created: 24th February, 2022

"""

# imports
import numpy as np
import pandas as pd

from j_prdctsim.bom import leafcomponents_qp

def ravisim(sku1, sku2, bom, verbose=0):
    """
    Return the similarity proportion (0 as no leaf component overlap, 1 as identical leaf component overlap) between two items represented
    by their respective SKU codes. Similarity is calculated as the proportion of the amount of lowest level component overlap

    Parameters
    ---------
    sku1 : str or int
        Code of first item to compare
    sku2 : str or int
        Code of second item to compare
    bom : numpy.ndarray
        Bill of Materials - The table contining the parent component data and their respective quantity pers
    verbose : {0, 1, 2}, default 0
        verbosity of function

    Returns
    ---------
    proportion : float
        Proportion of similarity between items sku1 and sku2
    """
    # Format paramters
    sku1 = str(sku1).strip("['']")
    sku2 = str(sku2).strip("['']")
    if verbose in (1,2) : print(f"Calculating Similarity between {sku1} and {sku2}")

    # Trivial Case       
    if sku1 == sku2 : return float(1.0)                     

    # Get Leaf Components and qtypers of each sku
    leaves1 = leafcomponents_qp(sku1, bom)    
    leaves2 = leafcomponents_qp(sku2, bom)

    # Calculate the Overlapping Material
    overlap_mat = np.intersect1d(leaves1[:,0], leaves2[:,0])
    overlap = 0
    for mat in overlap_mat:
        qty1 = leaves1[leaves1[:,0]==mat][0][1]
        qty2 = leaves2[leaves2[:,0]==mat][0][1]
        overlap += np.minimum(qty1, qty2)

    # Calculate the output (overlap/totalqty -> proportion)
    total = (np.sum(leaves1[:,1], axis=0) + np.sum(leaves2[:,1], axis=0)) - overlap
    proportion = float(np.around(overlap/total, 2))
    if verbose == 2: verbose_printer(overlap, total, round(proportion*100), proportion)

    return proportion

def verbose_printer(overlap, total, percent, proportion):
    print(" ")
    print(f" Overlap Qty:  {overlap}")
    print(f" Total Qty:  {total}")
    print(f" Percent Similar:{percent}")
    print(f" Proportion: {proportion}")
    print(" ")