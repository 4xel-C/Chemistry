import tkinter as tk
from tkinter import Canvas, Scrollbar, Frame
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw, rdMolDescriptors
from rdkit.Chem.Crippen import MolLogP
from rdkit.Chem.rdChemReactions import ReactionFromSmarts
import itertools
from PIL import Image, ImageTk
import io
 
# Define the reaction SMARTS for the formation of an amide from a carboxylic acid and an amine
amide_formation_smarts = "[C:1](=O)[O:2].[N:3]>>[C:1](=O)[N:3]"
amide_formation_reaction = ReactionFromSmarts(amide_formation_smarts)
 
# Function to react carboxylic acid with amine to form amide
def form_amide(acid_smiles, amine_smiles):
    acid_mol = Chem.MolFromSmiles(acid_smiles)
    amine_mol = Chem.MolFromSmiles(amine_smiles)
    product_set = amide_formation_reaction.RunReactants((acid_mol, amine_mol))
    if product_set:  # Check if the reaction produced any products
        product_mol = product_set[0][0]  # Take the first product of the first set
        return Chem.MolToSmiles(product_mol)
    else:
        return None
 
# Function to process the input and generate the table
def process_input():
    carboxylic_acids_smiles = acids_text.get("1.0", tk.END).strip().split('\n')
    amines_smiles = amines_text.get("1.0", tk.END).strip().split('\n')
 
    # Generate all combinatorial pairs of acids and amines
    combinations = list(itertools.product(carboxylic_acids_smiles, amines_smiles))
    # Generate amides for each combination
    amides_data = []
    for acid, amine in combinations:
        amide_smiles = form_amide(acid, amine)
        if amide_smiles:  # If a product was successfully generated
            amide_mol = Chem.MolFromSmiles(amide_smiles)
            clogP = MolLogP(amide_mol)
            mw = Descriptors.MolWt(amide_mol)
            formula = rdMolDescriptors.CalcMolFormula(amide_mol)
            amides_data.append((acid, amine, amide_smiles, clogP, mw, formula))
 
    # Display the results
    display_results(amides_data)
 
# Function to display the results in a new window
def display_results(amides_data):
    result_window = tk.Toplevel(root)
    result_window.title("Results")
 
    # Setting up the scrollable canvas
    canvas = Canvas(result_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
    scrollbar_y = Scrollbar(result_window, orient="vertical", command=canvas.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill="y")
 
    scrollbar_x = Scrollbar(result_window, orient="horizontal", command=canvas.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill="x")
 
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
 
    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
 
    # Displaying the table headers
    headers = ["#", "Acid Image", "Amine Image", "Amide Image", "Acid SMILES", "Amine SMILES", "Amide SMILES", "cLogP", "MW", "Formula"]
    for i, header in enumerate(headers):
        tk.Label(frame, text=header, borderwidth=2, relief="groove").grid(row=0, column=i, sticky="nsew")
 
    # Displaying the data
    for row_index, (acid, amine, amide, clogP, mw, formula) in enumerate(amides_data, start=1):
        tk.Label(frame, text=str(row_index), borderwidth=2, relief="groove").grid(row=row_index, column=0, sticky="nsew")
        for col_index, smiles in enumerate([acid, amine, amide], start=1):
            mol = Chem.MolFromSmiles(smiles)
            img = Draw.MolToImage(mol, size=(100, 100))
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            img_data = bio.getvalue()
            photo = ImageTk.PhotoImage(data=img_data)
            img_label = tk.Label(frame, image=photo)
            img_label.image = photo  # keep a reference!
            img_label.grid(row=row_index, column=col_index, padx=5, pady=5)
        for col_index, smiles_code in enumerate([acid, amine, amide], start=4):
            tk.Label(frame, text=smiles_code, borderwidth=2, relief="groove").grid(row=row_index, column=col_index, sticky="nsew")
        tk.Label(frame, text=f"{clogP:.2f}", borderwidth=2, relief="groove").grid(row=row_index, column=7, sticky="nsew")
        tk.Label(frame, text=f"{mw:.2f}", borderwidth=2, relief="groove").grid(row=row_index, column=8, sticky="nsew")
        tk.Label(frame, text=formula, borderwidth=2, relief="groove").grid(row=row_index, column=9, sticky="nsew")
 
# Create the main window
root = tk.Tk()
root.title("SMILES Input")
 
# Create input fields
tk.Label(root, text="Enter carboxylic acids SMILES (one per line):").pack()
acids_text = tk.Text(root, height=10, width=50)
acids_text.pack()
 
tk.Label(root, text="Enter amines SMILES (one per line):").pack()
amines_text = tk.Text(root, height=10, width=50)
amines_text.pack()
 
# Create a button to start the processing
process_button = tk.Button(root, text="Process", command=process_input)
process_button.pack()
 
# Run the main loop
root.mainloop()