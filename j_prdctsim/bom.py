""" Product Bill of Materials: Extract a product's component structure and by extension represent it visually

This module deals with the structure of a product by extracting each layer of its components. Recursive functions are utilized 
to traverse through the inputted Bill of Materials (BoM) and to extract the  component codes (sku) and the quantity needed per unit of product
at each level (QtyPer).  Functions for generating tree images and pygraphiz GraphObjects utilize these DFS functions and are included in 
this module.

Author: J Leon Batulayan <jleon.batulayan@gmail.com>

Created: 24th February, 2022
"""

# imports 
import os
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from matplotlib.pyplot import figure
from networkx.drawing.nx_agraph import  graphviz_layout
from networkx.drawing.nx_pydot import graphviz_layout



def components(sku, bom):
    """
    Return a list of SKU codes of all unique components used for the inputted sku according to the inputted bom

    Paramters
    ---------
    sku : str or int
        The code of the item whose unique components we are extracting
    bom : numpy.ndarray
        Bill of Materials - The table contining the parent component data

    Returns
    ---------
    out : list
        list of all sku component item codes
    """
    
    sku = str(sku)
    out = []
    sku_table = bom[bom[:,0]==sku]
    sku_comp = sku_table[:,1]
    sku_comp = sku_comp[np.argsort(sku_comp)]

    # Iterate over each SKU component
    for comp in sku_comp:
        comp = str(comp)
        out.append(comp)
        out = out + components(comp, bom)
    out = list(dict.fromkeys(out))

    return out

def leafcomponents(sku, bom):
    """
    Return a list of SKU codes of all unique lowest level components used for the inputted sku according to the inputted bom

    Paramters
    ---------
    sku : str or int
        The code of the item whose unique components we are extracting
    bom : numpy.ndarray
        Bill of Materials - The table contining the parent component data

    Returns
    ---------
    out : list
        list of all sku component item codes
    """
    pass

def sku_usage(sku, bom):
    """
    Return a list of all unique SKU codes that require the inputted sku according to the inputted bom

    Paramters
    ---------
    sku : str or int
        The code of the item whose usage we are extracting
    bom : numpy.ndarray
        Bill of Materials - The table contining the parent component data

    Returns
    ---------
    out : list
        list of all item codes that require the inputted sku
    """
    sku = str(sku)
    out = []
    sku_table = bom[bom[:,1]==sku]
    sku_used = sku_table[:,0]
    sku_used = sku_used[np.argsort(sku_used)]

    # Iterate over each SKU component
    for comp in sku_used:
        comp = str(comp)
        out.append(comp)
        out = out + sku_usage(comp, bom)
    out = list(dict.fromkeys(out))

    return out

def highestlevel_usage(sku, bom):
    pass


def leafcomponents_qp(sku, bom_qp, qty=1.0):
    """
    Returns the lowest level of components and their respective QtyPer for the inputted sku  based on input qty and the inputted bom
    If the inputted sku does not exist or is a leaf component, it returns the output with the sku as itself and qty as the inputted
    Paramters
    ---------
    sku : str or int
        The code of the item whose lowest level of components we are extracting
    bom_qp : numpy.ndarray
        Bill of Materials - The table contining the parent component data and their respective quantity pers
    qty : number, default 1.0
        the quantity of the item we are accounting for

    Returns
    ---------
    out : numpy.ndarray
        dx2 ndarray of leaf component codes in the first column and their respective QtyPers (rounded to 3 decimal places) 
        in the second for d leaf components
    """
    sku = str(sku)
    qty = float(qty)
    assert bom_qp.shape[1] >= 3, "The Bill of Materials has insufficient dimensions. Please format as [[Parent, Component, QtyPer]]"

    # Recursively acquire leaf components and respective QtyPers
    init_out = leaf_components_recursive_helper(sku, bom_qp, qty)
    init_out[:,1] = init_out[:,1].astype(np.float64)
    
    # Aggregate Sum Group By Leaf SKUs
    leaves = np.unique(init_out[:,0])
    out = np.empty((len(leaves),2), dtype=object)
    for i in range(len(leaves)):
        leaf = leaves[i]
        leaf_qtys = init_out[init_out[:,0]==leaf][:,1]
        sum = np.around(np.sum(leaf_qtys, axis=0), 3)
        out[i] = np.array([leaf, sum], dtype=object)
        
    # Sort by increasing QtyPer
    out = out[np.argsort(out[:,-1])]

    return out

def leaf_components_recursive_helper(sku: str, bom: np.ndarray, qty=1.0):
    """
    Recursive helper function for leaf_components
    returns the lowest level of components for the input sku and the QtyPer
    """ 
    sku_table = bom[bom[:,0]==sku]  # Subset of BoM with sku as the parent
    total_comp = np.empty((0,2), dtype=object)
    
    if len(sku_table) == 0: # Terminate : sku is a leaf
        total_comp = np.append(total_comp, [[sku,qty]], axis=0) 
    else:
        sku_comp = sku_table[:,[1,2]]   # Components and respective QtypPers for given sku
        for comp, qty_per in sku_comp:
            comp_leaves = leaf_components_recursive_helper(str(comp), bom, float(qty_per)*qty)
            total_comp = np.append(total_comp, comp_leaves, axis=0)
    
    return total_comp

def edges(sku, bom):
    """
    Recursuively acquire all edges from Bill of Materials tree. Returns a list of edges represented by
    each vertix making up the edge in a tuple according to the inputted bom

    Paramters
    ---------
    sku : str or int
        The code of the item whose Bill of Material tree edges we are extracting
    bom : numpy.ndarray
        Bill of Materials - The table contining the parent component data and their respective quantity pers

    Returns
    ---------
    tree_edges : list
        list of tuples with each vertix zf an edge represented as each respective elment of the tuple

    Example
    ---------
        P001 -- L3
        /  | 
      /   |  
    L1    L2  

    This BoM tree rooted at P001 will return edges [(P001, L1), (P001, L2), (P001, L3)] 
    """
    sku = str(sku)
    tree_edges = []
    sku_table = bom[bom[:,0]==sku]
    sku_comp = sku_table[:,1]
    sku_comp = sku_comp[np.argsort(sku_comp)]

    # Iterate over each SKU component
    for comp in sku_comp:
        comp = str(comp)
        temp_edge = (sku, comp)
        tree_edges.append(temp_edge)
        tree_edges = tree_edges + edges(comp, bom)
    
    return tree_edges


def image(sku, bom, name=None, save_path=None, img_type='jpeg', verbose=1):
    """
    This function is an extension of networkx's DiGraph. Saves an image of a Bill of Material 
    tree rooted at the inputted sku according to the inputted bom

    Paramters
    ---------
    sku : str or int
        The code of the item which the returned Bill of Materials tree is rooted on
    bom : numpy.ndarray
        Bill of Materials - The table contining the parent component data and their respective quantity pers
    name : str, default None
        Name image is to be saved as  
    save_path : str, default None
        Path to directory image is to be saved in
    img_type :  'png', 'jpg', default 'jpeg'
        file type image is to be saved
    verbose : 0, 1, default 1
        verbrosity of function

    Returns
    ---------
    None

    """
    sku = str(sku)
    G = nx.DiGraph()
    G.add_node(sku) # Root
    G.add_edges_from(edges(sku, bom))
    pos =graphviz_layout(G, prog='dot')
    figure(figsize=(10, 10), dpi=80)
    nx.draw(
        G, 
        pos,
        with_labels=True, 
        arrows=False, 
        node_size=1300, 
        node_color="skyblue", 
        edge_color="grey", 
        width=2.0, 
        node_shape="s", 
        alpha=0.6, 
        linewidths=30, 
        font_color="black"
        )

    if name is None:
        fig_name = "{sku}_bom_tree.{img_type}".format(sku=sku, img_type=img_type)
    else:
        fig_name = "{name}.{img_type}".format(name=name, img_type=img_type)

    if save_path is None:
        fig_path = os.path.join(os.getcwd(), fig_name)
    else:
        fig_path = os.path.join(save_path, fig_name)
    
    print(fig_path)
    plt.savefig(fig_path)
    plt.close()
    if verbose == 1:
        print("Image {name} saved to {path}".format(name=fig_name,path=fig_path))