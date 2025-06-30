import pandas as pd
import json
import MetricsV3 as m 
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
