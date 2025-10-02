import fitz


pdf_path="./PDFs/Active-Skills-for-Reading-1.pdf"
texto_por_pagina = {}  # Diccionario para almacenar el texto por página
documento=fitz.open(pdf_path)




pagina=documento.load_page(13)
texto=pagina.get_text("text")  # Extraer texto de la página


documento.close()

with open("./txts/Texto_LibroIngles.txt", "w", encoding="utf-8") as archivo_txt:
    
    archivo_txt.write(texto)
      