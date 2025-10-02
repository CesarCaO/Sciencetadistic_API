import pandas as pd
import json
import scripts.MetricsV4 as m 
from tqdm.auto import tqdm

file_path="./CSVs/ReadeabilityPapers_CSV.csv"
save_path="./JSON_Metrics/"


df= pd.read_csv(file_path,encoding="utf-8")
#print(df.shape)
print(df.columns)
df_aceptados=df[df["Accepted"]==1]
#df_aceptados=df_aceptados.head(1000)
#print(df_aceptados)
df_rechazados=df[df["Accepted"]==0]
#df_rechazados=df_rechazados.head(1000)
#print(df_rechazados)
"""
#Densidad lexica
tqdm.pandas(desc="Progreso de procesamiento de Aceptados")
dl_accepted = df_aceptados['Texto Completo'].progress_apply(m.calculateLexicalDensity).tolist()
tqdm.pandas(desc="Progreso de procesamiento de Rechazados")
dl_rejected = df_rechazados["Texto Completo"].progress_apply(m.calculateLexicalDensity).tolist()

dl = {
    'Accepted': dl_accepted,
    'Rejected': dl_rejected
}

with open(save_path+'/Lexical_Density.json', "w", encoding="utf-8") as file:
    json.dump(dl,file, indent=4)
    file.close()
"""

tqdm.pandas(desc="Progreso de procesamiento de Aceptados")
sf_accepted = df_aceptados['Texto Completo'].progress_apply(m.calculateSophistication).tolist()
tqdm.pandas(desc="Progreso de procesamiento de Rechazados")
sf_rejected = df_rechazados["Texto Completo"].progress_apply(m.calculateSophistication).tolist()

sf = {
    'Accepted': sf_accepted,
    'Rejected': sf_rejected
}

with open(save_path+'/Sophistication.json', "w", encoding="utf-8") as file:
    json.dump(sf,file, indent=4)
    file.close()
"""
#TTR
tqdm.pandas(desc="Progreso de procesamiento de Aceptados")
ttr_acepted=df_aceptados["Texto Completo"].progress_apply(m.calculateTTR).tolist()
tqdm.pandas(desc="Progreso de procesamiento de Rechazados")
ttr_rejected=df_rechazados["Texto Completo"].progress_apply(m.calculateTTR).tolist()

ttr={
    'Acepted':ttr_acepted,
    'Rejected':ttr_rejected
}

with open(save_path+'TTR.json', "w", encoding="utf-8") as file:
    json.dump(ttr,file, indent=4)
    file.close()
"""
"""
#Root TTR
tqdm.pandas(desc="Progreso de procesamiento de Aceptados")
ttr_acepted=df_aceptados["Texto Completo"].progress_apply(m.calculateTTRRoot).tolist()
tqdm.pandas(desc="Progreso de procesamiento de Rechazados")
ttr_rejected=df_rechazados["Texto Completo"].progress_apply(m.calculateTTRRoot).tolist()

ttr={
    'Acepted':ttr_acepted,
    'Rejected':ttr_rejected
}

with open(save_path+'Root_TTR.json', "w", encoding="utf-8") as file:
    json.dump(ttr,file, indent=4)
    file.close()
"""
"""
#TTR corrected

tqdm.pandas(desc="Progreso de procesamiento de Aceptados")
ttr_acepted=df_aceptados["Texto Completo"].progress_apply(m.calculateTTRCorregido).tolist()
tqdm.pandas(desc="Progreso de procesamiento de Rechazados")
ttr_rejected=df_rechazados["Texto Completo"].progress_apply(m.calculateTTRCorregido).tolist()

ttr={
    'Acepted':ttr_acepted,
    'Rejected':ttr_rejected
}

with open(save_path+'Corrected_TTR.json', "w", encoding="utf-8") as file:
    json.dump(ttr,file, indent=4)
    file.close()
"""

'''
#*Flesch

tqdm.pandas(desc="Progreso de procesamiento de Aceptados")
acepted=df_aceptados["Texto Completo"].progress_apply(m.TFRE).tolist()
tqdm.pandas(desc="Progreso de procesamiento de Rechazados")
rejected=df_rechazados["Texto Completo"].progress_apply(m.TFRE).tolist()

ttr={
    'Acepted':acepted,
    'Rejected':rejected
}

with open(save_path+'Flesh.json', "w", encoding="utf-8") as file:
    json.dump(ttr,file, indent=4)
    file.close()
'''