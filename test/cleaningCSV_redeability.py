import pandas as pd
from tqdm.auto import tqdm


df = pd.read_csv("./CSVs/CSVsUnidos.csv", encoding="utf-8")
print("Registros origniales:", len(df))
df_copy=df.copy


def contar_palabras(texto):
    if isinstance(texto, str):  
        return len(texto.split())
    return 0 


tqdm.pandas(desc="Contando palabras de los papers...")
df['conteo_palabras'] = df["Texto Completo"].progress_apply(contar_palabras)

df_filtrado = df[df['conteo_palabras'] >= 100]

df_filtrado.drop(columns=['conteo_palabras'])
print("Número de registros seleccionados", len(df_filtrado))
df_filtrado.to_csv('./CSVs/ReadeabilityPapers_CSV.csv', index=False)