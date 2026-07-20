"""
Morgan fingerprint calculation functions.
"""

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator


def calculate_morgan_fingerprint(df, smiles_column="Smile",
                                    radius=2, n_bits=2048 ):
    
    fp_gen=rdFingerprintGenerator.GetMorganGenerator(radius= radius, fpSize= n_bits)
    mols=df[smiles_column].apply(Chem.MolFromSmiles)
    fingerprints=[]
    for mol in mols:
        if mol is None:
            fingerprints.append([np.nan] * n_bits)
            continue
        try:
          fp=fp_gen.GetFingerprint(mol)
          fp_bits=list(fp)
        except Exception:
           fp_bits=[np.nan]*(n_bits)
        
        fingerprints.append(fp_bits)
    
    fingerprints_df=pd.DataFrame(fingerprints, columns=[f"FP_{i}" for i in range(n_bits)])
    return fingerprints_df


