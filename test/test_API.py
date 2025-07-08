import requests

url="https://scientadistic-api.onrender.com/metrics"

params={"metric":"ttr"}

with open("./PDFs/Cost_sensitive_selective_naive_Bayes_cla.pdf", "rb") as file:
    files = {"file": ("Cost_sensitive_selective_naive_Bayes_cla.pdf", file, "application/pdf")}

    response = requests.post(
        url,
        params=params,
        files=files
    )

    if response.status_code == 200:
        print("Resultado:", response.json())
    else:
        print("Error:",response.text)