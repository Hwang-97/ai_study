import os
import torch
from django.http import JsonResponse
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoModelForCausalLM,
    T5Tokenizer,
    T5ForConditionalGeneration,
)

# Base directory for caching models
CACHE_DIR = os.path.join(os.getcwd(), "apps", "ai", "models")

# Load Chat Model (Model A)
chat_model_name = "Bllossom/llama-3.2-Korean-Bllossom-3B"
chat_tokenizer = AutoTokenizer.from_pretrained(chat_model_name, cache_dir=CACHE_DIR)
chat_model = AutoModelForCausalLM.from_pretrained(
    chat_model_name,
    cache_dir=CACHE_DIR,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# Load News Analysis Model (Model B)
news_model_name = "ProsusAI/finbert"
news_tokenizer = AutoTokenizer.from_pretrained(news_model_name, cache_dir=CACHE_DIR)
news_model = AutoModelForSequenceClassification.from_pretrained(
    news_model_name, cache_dir=CACHE_DIR
)

# Load Decision Model (Model C)
decision_model_name = "google/flan-t5-base"
decision_tokenizer = T5Tokenizer.from_pretrained(decision_model_name, cache_dir=CACHE_DIR)
decision_model = T5ForConditionalGeneration.from_pretrained(
    decision_model_name, cache_dir=CACHE_DIR, device_map="auto", torch_dtype=torch.float16,
)


def chat_with_ai(request):
    """Handles chat interactions using the Chat Model."""

    question = request.GET.get("question")
    if not question:
        return JsonResponse({"error": "No question provided"}, status=400)
    messages = [
        {"role": "user", "content": f"{question}"}
    ]
    input_ids = chat_tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(chat_model.device)

    terminators = [
        chat_tokenizer.convert_tokens_to_ids("<|end_of_text|>"),
        chat_tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = chat_model.generate(
        input_ids,
        max_new_tokens=1024,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9
    )

    answer = chat_tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True)

    return JsonResponse({"question": question, "answer": answer})


def analyze_news(request):
    """Analyzes news sentiment using the News Analysis Model."""
    news_text = request.GET.get("news")
    if not news_text:
        return JsonResponse({"error": "No news text provided"}, status=400)

    inputs = news_tokenizer(news_text, return_tensors="pt", padding=True, truncation=True).to(
        news_model.device
    )
    outputs = news_model(**inputs)
    sentiment = torch.argmax(outputs.logits, dim=1).item()

    sentiment_label = {0: "Negative", 1: "Neutral", 2: "Positive"}  # Adjust based on FinBERT's training
    return JsonResponse({"news": news_text, "sentiment": sentiment_label.get(sentiment, "Unknown")})


def make_trading_decision(request):
    """Makes trading decisions based on news and stock information."""
    news_sentiment = request.GET.get("sentiment")
    stock_info = request.GET.get("stock")
    if not news_sentiment or not stock_info:
        return JsonResponse({"error": "Insufficient data provided"}, status=400)

    prompt = f"The news sentiment is {news_sentiment}. The stock info is {stock_info}. What should I do?"
    inputs = decision_tokenizer(prompt, return_tensors="pt").to(decision_model.device)
    outputs = decision_model.generate(inputs["input_ids"], max_new_tokens=50)
    decision = decision_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return JsonResponse({"sentiment": news_sentiment, "stock": stock_info, "decision": decision})
