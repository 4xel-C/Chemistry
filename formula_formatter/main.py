import pandas as pd
import re

#Pattern to detect All atoms in a formula and separate the number into tupple (Xx, Num)
pattern =  re.compile(r'([A-Z][a-z]?)(\d*)')

#Function to return a Dictionnary containing the composition of the molecular formula
def parse_formula(formula):
    parsed_formula = dict()
    for i, j in pattern.findall(formula):
        parsed_formula[i] = j
    return parsed_formula

#Load both datafram =
df_formulas = pd.read_excel("C:/Users/GFEEU/OneDrive - Bayer/Desktop/Axel/Code/Projets/2024.06.03 - Formula_formatter/data/detailled_formulas.xlsx")
df_storage = pd.read_excel("C:/Users/GFEEU/OneDrive - Bayer/Desktop/Axel/Code/Projets/2024.06.03 - Formula_formatter/data/LDA_Vials_Sotck&Chem.xlsx")

#Storing the formulas serie to detect into a variable 
formula_serie = df_formulas["Molecular Formula"]

#preparing filter to compare both formulas Series applying the parsing method (Completly ignore formula format)
filter_comparison = df_storage["Molecular_Formula"].apply(parse_formula).isin(formula_serie.apply(parse_formula))

#Storing results
results = df_storage[filter_comparison]

#Writing the list into a new Excel file
results.to_excel("C:/Users/GFEEU/OneDrive - Bayer/Desktop/Axel/Code/Projets/Formula_formatter/data/ODC_in_lyo.xlsx")


# # Test
# form = "C3HBr4F2Cl2"
# form2 = "C3FHBr4Cl2"
# print(parse_formula(form) == parse_formula(form2))