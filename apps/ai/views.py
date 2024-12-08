import os
import torch
from django.http import JsonResponse
from transformers import LlamaForCausalLM, LlamaTokenizer, AutoTokenizer, AutoModelForCausalLM

# 모델 로드 (서버 시작 시에만)
# 모델 이름
# model_name = "meta-llama/Llama-3.2-3B"
model_name = "Bllossom/llama-3.2-Korean-Bllossom-3B"
# 다운로드 경로
model_path = os.path.join(os.getcwd(), "apps", "ai", "models", model_name.split("/")[1])

# tokenizer = LlamaTokenizer.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=model_path)
# model = LlamaForCausalLM.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir=model_path,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)


def get_answer(request):
    question = request.GET.get("question")
    if not question:
        return JsonResponse({"error": "No question provided"}, status=400)

    messages = [
        {"role": "user", "content": f"{question}"}
    ]
    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)
    terminators = [
        tokenizer.convert_tokens_to_ids("<|end_of_text|>"),
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=1024,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9
    )
    answer = tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True)

    return JsonResponse({"question": question, "answer": answer})
