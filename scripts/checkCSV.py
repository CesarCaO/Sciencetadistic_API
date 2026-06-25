import pandas as pd


file_path="./CSVs/ReadeabilityPapers_CSV.csv"

df= pd.read_csv(file_path,encoding="utf-8")

#print(df.columns)

#print(df["Conferencia"].value_counts())

#print(df.groupby(["Conferencia", "Accepted"]).size())

tabla = pd.crosstab(df["Conferencia"], df["Accepted"])

print(tabla)