import nglview as nv
from rdkit import Chem
from rdkit.Chem import AllChem

# Créer une molécule à partir d'une chaîne SMILES
smiles = 'CC(C)C(=O)O'  # Exemple : acide isobutyrique
mol = Chem.MolFromSmiles(smiles)

# Générer un conformère
AllChem.EmbedMolecule(mol)
AllChem.UFFOptimizeMolecule(mol)

# Convertir la molécule en format 3D
block = Chem.MolToMolBlock(mol)

# Visualiser avec nglview
view = nv.show_rdkit(mol)
view.add_representation('ball+stick')
view