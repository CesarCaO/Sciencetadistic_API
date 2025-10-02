from grobid_client.grobid_client import GrobidClient


client = GrobidClient(config_path="D:/Miniconda/Lib/site-packages/grobid_client/config.json")

input_pdf="D:/Proyectos Spyder/Categorizador de documentos/PDF2/"
output_dir="D:/Proyectos Spyder/Categorizador de documentos/Grobid_resultados/"
service="processFulltextDocument"


xml=client.process(service, input_pdf,output=output_dir,
                         consolidate_header=True, 
                         consolidate_citations=True, 
                         include_raw_citations=True, 
                         include_raw_affiliations=True, 
                         tei_coordinates=True, )



