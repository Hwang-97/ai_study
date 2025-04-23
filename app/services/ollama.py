import httpx
import torch
from app.config import settings

class OllamaService:
    def __init__(self, base_url=settings.OLLAMA_BASE_URL):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)
        
        # MPS 설정 (MacOS Metal GPU 가속)
        self.device = torch.device("mps" if torch.backends.mps.is_available() and settings.USE_MPS else "cpu")
        print(f"PyTorch using device: {self.device}")
    
    async def generate_response(self, model, prompt, system_prompt=""):
        """Ollama API를 사용하여 응답 생성"""
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        
        try:
            response = await self.client.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return f"Error generating response: {str(e)}"
        except Exception as e:
            print(f"Unexpected error: {e}")
            return f"Unexpected error: {str(e)}"
    
    async def generate_response_stream(self, model, prompt, system_prompt=""):
        """스트리밍 응답 생성"""
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": True,
            "options": {
                "num_gpu": 48,  # GPU 레이어 수 조정
                "num_thread": 4  # 스레드 수 조정
            }
        }
        
        try:
            async with self.client.stream("POST", f"{self.base_url}/api/generate", json=payload) as response:
                response.raise_for_status()
                
                full_response = ""
                async for chunk in response.aiter_bytes():
                    try:
                        # 스트리밍 응답은 JSONL 형식임
                        chunk_str = chunk.decode("utf-8")
                        # 여러 줄이 올 수 있음
                        for line in chunk_str.strip().split("\n"):
                            if line:
                                import json
                                chunk_data = json.loads(line)
                                if "response" in chunk_data:
                                    response_piece = chunk_data["response"]
                                    full_response += response_piece
                                    yield response_piece
                    except Exception as e:
                        print(f"Error processing chunk: {e}")
                        
                yield full_response
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            yield f"Error generating response: {str(e)}"
        except Exception as e:
            print(f"Unexpected error: {e}")
            yield f"Unexpected error: {str(e)}"
            
    async def get_available_models(self):
        """사용 가능한 모델 목록 조회"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return response.json()["models"]
        except Exception as e:
            print(f"Error getting models: {e}")
            return []