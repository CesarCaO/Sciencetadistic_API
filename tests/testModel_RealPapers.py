"""
#* Testing models with real papers



model_files=[
    r"./predictive_model/2_EXPEI_PEER_READ.pkl",
    r"./predictive_model/2_EXPEI_ASAP.pkl"
]

for file in model_files:
    print(f"\n Loading model from: {file}")

    with open(file,"rb") as f:
        print("Reading Model")
        data = pickle.load(f)
    
    model = data['model']
    vectorizer = data['vectorizer']
    label_encoder = data['label_encoder']
    vocabulario = data['vocabulario']
    caracteristicas = data['caracteristicas']
    pronombres = ['we', 'our', 'us']

    for pdf in langFile:
        pdf_path=os.path.join(pdfs,pdf)
        doc = fitz.open(pdf_path)
        print("Extracting text")
        for page in doc:
            text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')
        doc.close()

        text = mtrs.removeReferences(text)
        text = mtrs.cleanText(text)

        x_test =[text.lower()]
        print("Vectorizing...")
        X_test = vectorizer.transform(x_test)

        print("Calculating Expei")
        fpT, fnpT, contadorPT, contadorNPT = frases(x_test, pronombres, X_test, vocabulario, caracteristicas)
        peit, _ = PeiNei(contadorPT, fpT, contadorNPT, fnpT, X_test)
        expei_test = expei_func(X_test, peit)

        print("Making prediction...")
        y_pred = model.predict(expei_test)

        print(f"{pdf_path}  prediction: ", y_pred)
"""