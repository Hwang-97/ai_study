import os
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, AutoTokenizer, AutoModelForCausalLM

# 모델 이름
# model_name = "meta-llama/Llama-3.2-3B"
model_name = "Bllossom/llama-3.2-Korean-Bllossom-3B"

# 다운로드할 경로 설정
model_path = os.path.join(os.getcwd(), "apps", "ai", "models", model_name.split("/")[1])

# 모델과 토크나이저 다운로드
# tokenizer = LlamaTokenizer.from_pretrained(model_name, cache_dir=model_path)
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=model_path)
# model = LlamaForCausalLM.from_pretrained(model_name, cache_dir=model_path, legacy=False)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir=model_path,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
print("모델 다운로드 완료!")

instruction = "다운로드 확인용 질문입니다. 철수가 20개의 연필을 가지고 있었는데 영희가 절반을 가져가고 민수가 남은 5개를 가져갔으면 철수에게 남은 연필의 갯수는 몇개인가요?"

messages = [
    {"role": "user", "content": f"{instruction}"}
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

print(tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True))