import pdfplumber


pdf=pdfplumber.open("D:/Documentos HDD/Proyectos Spyder/Categorizador de documentos/PDFs/IA1.pdf")

with pdf as pdfLeer:
     
         
     img= pdf.pages[0].to_image(resolution=150)
         
       
     with open("D:/Documentos HDD/Proyectos Spyder/Categorizador de documentos/Images-PDFPlumber/","wb") as fp:
         fp.write(img.data)#para poder generar imagenes se necesitan valores binarios
         fp.close()


