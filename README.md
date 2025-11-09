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

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip

### Install dependencies

```bash
pip install requests
```



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
            
            

            print(f" {result['metric']} Analysis Results:")
            print(f"Your document score: {result['current_document']:.4f}")
            #Warning: Warning: If you run the following lines, more than 21000 values will appear on the console. They are commented out so you can observe a simplified API response instead.
            #print(f"Accepted papers : {result['Accepted']}")
            #print(f"Rejected papers : {result['Rejected']}")
            return result
        else:
            print(f" Error: {response.text}")
            return None
```
