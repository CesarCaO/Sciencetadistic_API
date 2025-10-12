import pickle

with open(R"./EXPEI_model/2_EXPEI_ICLR_2017_PR.pkl","rb") as file:
    print("Loading pickle...")
    data = pickle.load(file)

    print("Data loaded successfully.")
    print("Setting up model")
    model = data['model']
    vectorizer = data['vectorizer']
    label_encoder = data['label_encoder']
    vocabulario = data['vocabulario']
    caracteristicas = data['caracteristicas']
    pronombres = ['we', 'our', 'us']
    print("Success, model is now ready to predict")