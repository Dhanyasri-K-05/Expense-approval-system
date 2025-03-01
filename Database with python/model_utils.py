from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
import torch

def load_model(model_path):
    # Load your trained model here
    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")
    return model

def predict(model, input_text, tokenizer):
    # Use your model to make a prediction
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = logits.softmax(dim=-1)
    predicted_class = torch.argmax(probabilities, dim=-1).item()
    return predicted_class, probabilities
