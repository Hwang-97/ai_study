import re
from typing import Dict, Any, List

def format_persona_prompt(persona: Dict[str, Any], topic: str) -> str:
    """페르소나 프롬프트 포맷팅"""
    return (
        f"당신은 {persona['name']}입니다.\n"
        f"당신은 {persona['belief']}라고 믿습니다.\n"
        f"당신은 {persona['tone']} 말투를 사용합니다.\n"
        f"당신의 배경: {persona['background']}\n\n"
        f"주제: {topic}"
    )

def clean_response(response: str) -> str:
    """LLM 응답에서 불필요한 요소 제거"""
    # 따옴표로 시작하거나 끝나는 경우 제거
    response = response.strip('"\'')
    
    # 역할 표시 제거 (예: "환경주의자: " 제거)
    response = re.sub(r'^[^:]+:\s*', '', response)
    
    return response.strip()

def truncate_context(context: str, max_tokens: int = 4000) -> str:
    """컨텍스트를 최대 토큰 수에 맞게 자르기"""
    # 간단한 근사치로 구현 (더 정확한 토큰화는 tokenizers 라이브러리 필요)
    words = context.split()
    if len(words) <= max_tokens:
        return context
    
    # 최신 대화를 유지하기 위해 앞부분을 자름
    return ' '.join(words[-max_tokens:])