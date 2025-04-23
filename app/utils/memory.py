import torch
import gc
from app.config import settings

def clear_gpu_memory():
    """MPS 메모리 정리 함수"""
    if torch.backends.mps.is_available() and settings.USE_MPS:
        # PyTorch 캐시 정리
        gc.collect()
        torch.mps.empty_cache()  # MPS 장치 메모리 정리
        return True
    return False

def get_gpu_info():
    """GPU 상태 정보 반환"""
    info = {
        "device": "mps" if torch.backends.mps.is_available() and settings.USE_MPS else "cpu",
        "available": torch.backends.mps.is_available()
    }
    return info
