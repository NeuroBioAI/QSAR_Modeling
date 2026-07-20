"""
Descriptor calculation functions for QSAR modeling.
"""

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

BASIC_DESCRIPTOR_NAMES = [
    "NumAtoms",
    "MW",
    "HBA",
    "HBD",
    "logP",
    "TPSA",
    "RotatableBonds",
    "NumAromaticRing" ]


def descriptors_names():
    """Return the names of all RDKit molecular descriptors."""
    return [name for name,func in Descriptors._descList]


def get_descriptors_functions():
    """Return RDKit descriptor names and corresponding functions."""
    return Descriptors._descList


def calculate_basic_descriptors(df, smiles_column="Smile"):
    """
    Calculate basic molecular descriptors from SMILES strings.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe containing SMILES.
    smiles_column : str, default="Smile"
        Name of the column containing SMILES strings.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing basic molecular descriptors.
    """
    mols=df[smiles_column].apply(Chem.MolFromSmiles)
    descriptors=[]
    for mol in mols:
        if mol is None:
            descriptors.append({name: np.nan for name in BASIC_DESCRIPTOR_NAMES})
        continue
    descriptors.append({'NumAtoms':mol.GetNumAtoms(),
                    'MW':Descriptors.MolWt(mol),
                    'HBA':Descriptors.NumHAcceptors(mol),
                    'HBD':Descriptors.NumHDonors(mol),
                    'logP':Descriptors.MolLogP(mol),
                    'TPSA':Descriptors.TPSA(mol),
                    'RotatableBonds':Descriptors.NumRotatableBonds(mol),
                    'NumAromaticRing':Descriptors.NumAromaticRings(mol)})
                    
    descriptors_df=pd.DataFrame(descriptors)
    return descriptors_df



def calculate_extended_descriptors(df, smiles_column="Smile"):
    """
    Calculate extended molecular descriptors from SMILES strings.
    This function converts SMILES strings into molecular structures and
    calculates a set of extended molecular descriptors for each molecule.
    Invalid SMILES or failed descriptor calculations are assigned NaN values

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe containing SMILES.
    smiles_column : str, default="Smile"
        Name of the column containing SMILES strings.

    Returns
    -------
    pandas.DataFrame
       DataFrame containing calculated molecular descriptors, where each
       row corresponds to a molecule and each column corresponds to a descriptor.
    """
    des_list=get_descriptors_functions()
    mols=df[smiles_column].apply(Chem.MolFromSmiles)
    descriptors=[]
    for mol in mols:
        row={}
        for name, func in des_list:
            try:
               row[name]=func(mol)
            except Exception:
                row[name]=np.nan
        descriptors.append(row)
        
    descriptors_df=pd.DataFrame(descriptors) 
    return descriptors_df
    

