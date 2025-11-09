# Sciencetadistic API

API for stylometric analysis and acceptance prediction of scientific articles. This API allows you to evaluate the lexical quality of PDF documents and predict whether a scientific article will be accepted or rejected in the evaluation process.

## 🚀 Features

- **Lexical metrics analysis**: Evaluates the lexical richness of scientific documents
- **Acceptance prediction**: Uses machine learning models to predict article acceptance
- **PDF processing**: Extracts and analyzes text from PDF documents
- **REST API**: Easy-to-use interface with FastAPI


## 📊 Available Metrics

- **Lexical Density**: Text lexical density
- **Sophistication**: Vocabulary sophistication level
- **TTR (Type-Token Ratio)**: Type-token ratio
- **Root TTR**: Square root TTR
- **Corrected TTR**: Corrected TTR
- **Flesch Reading Ease**: Flesch reading ease
- **Flesch-Kincaid Grade**: Flesch-Kincaid grade level
- **Gunning Fog Index**: Gunning fog index
- **SMOG Index**: SMOG index

### Quick Access
- **Interactive Documentation (Swagger)**: https://scientadistic-api.onrender.com/docs

# 📝 Usage Examples
## 🛠️ Installation


### Prerequisites

- Python 3.8+
- pip

### Install dependencies
Only requires the `requests` library (usually pre-installed):

```bash
pip install requests
```


### Lexical Metrics endpoint

**Type** : Post. <br>
**URL** : https://scientadistic-api.onrender.com//metrics. <br>
**Possibles values of 'metric_type'** :
- lexical_density
- sophistication
- ttr
- root_ttr
- ttr_corrected
- flesh
- kincaid
- fog
- smog <br>

 
**PDF file** :  PDF file to analyze (max 4MB)
```python
import requests

def analyze_document_metrics(pdf_path, metric_type):
    """
    Analyze lexical metrics of a PDF document
    
    Args:
        pdf_path (str): Path to your PDF file
        metric_type (str): Type of metric to calculate
    """

    
    
    url = "https://scientadistic-api.onrender.com//metrics"
    
    data = {"metric": metric_type}
    
    with open(pdf_path, "rb") as file:
        files = {"file": (pdf_path.split("/")[-1], file, "application/pdf")}
        
        response = requests.post(url, data=data, files=files)
        
        if response.status_code == 200:
            result = response.json()
            
            

            print(f"Metric used: {result['metric']} ")
            print(f"Your document score: {result['current_document']:.4f}")
            #Warning: Warning: If you run the following lines, more than 21000 values will appear on the console. They are commented out so you can observe a simplified API response instead.
            #print(f"Accepted papers : {result['Accepted']}")
            #print(f"Rejected papers : {result['Rejected']}")
            return result
        else:
            print(f" Error: {response.text}")
            return None
```
**Expected response**

```bash
Metric used: 
Your document score: 
```
### Prediction endpoint

**Type** : Post. <br>
**URL** : https://scientadistic-api.onrender.com/prediction. <br>
**PDF file** :  PDF file to analyze (max 4MB)
```python
def predict_paper(pdf_path):
    """
    Analyze lexical metrics of a PDF document
    
    Args:
        pdf_path (str): Path to your PDF file
        
    """

    url = "https://scientadistic-api.onrender.com/prediction"
    

    with open(pdf_path, "rb") as file:
        files = {"file": (pdf_path.split("/")[-1], file, "application/pdf")}
        
        response = requests.post(url,files=files)
        
        if response.status_code == 200:
            result = response.json()

            print(f" {result['prediction']} Analysis Results:")
            
            return result
        else:
            print(f" Error: {response.text}")
            return None

```

#### Expected response
**Accepted**
```bash
Results: 1 
```

**Rejected**
```bash
Results: 10
```


## Acknowledgments
-spaCy for natural language processing models
-FastAPI for the web framework
-NLTK for text processing tools
-Readability for readability metrics

## Limitations
- The server shuts down after an inactivity period, it would take few minutes to start up again
- The accuracy of the Machine Learning model used for prediction is currenty 66%. It is expected to be improved
- The RAM server is limited due to the free Render account, so it may crash after too many requests or heavy documents. This problem will be resolved in the future
