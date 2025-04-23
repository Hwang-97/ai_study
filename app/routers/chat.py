from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from typing import List, Dict, Any
from app.models.schemas import DialogueRequest, DialogueResponse, PersonaModel, WebSocketRequest
from app.services.ollama import OllamaService
from app.services.persona import PersonaService
from app.services.conversation import ConversationGenerator
from app.config import settings
import json

# 서비스 인스턴스 생성
ollama_service = OllamaService()
persona_service = PersonaService()
conversation_generator = ConversationGenerator(ollama_service)

router = APIRouter()

@router.get("/personas")
async def get_personas():
    """사용 가능한 모든 페르소나 목록 반환"""
    return persona_service.get_all_personas()

@router.get("/models")
async def get_models():
    """사용 가능한 모든 LLM 모델 목록 반환"""
    models = await ollama_service.get_available_models()
    return {"models": models}

@router.post("/generate-dialogue", response_model=DialogueResponse)
async def generate_dialogue(request: DialogueRequest):
    """두 페르소나 간의 대화 생성 API"""
    persona1 = persona_service.get_persona(request.persona1_id)
    persona2 = persona_service.get_persona(request.persona2_id)
    
    if not persona1 or not persona2:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    conversation = await conversation_generator.generate_dialogue(
        persona1, persona2, request.topic, request.turns
    )
    
    return DialogueResponse(conversation=conversation)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket을 통한 실시간 대화 생성"""
    await websocket.accept()
    
    try:
        # 초기 메시지 전송
        await websocket.send_json({
            "event": "connected",
            "data": {
                "message": "Connected to AI Debate System"
            }
        })
        
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            
            # 요청 검증
            try:
                request_model = WebSocketRequest(**request)
            except Exception as e:
                await websocket.send_json({
                    "event": "error",
                    "data": {
                        "message": f"Invalid request format: {str(e)}"
                    }
                })
                continue
            
            # 페르소나 검증
            persona1 = persona_service.get_persona(request_model.persona1_id)
            persona2 = persona_service.get_persona(request_model.persona2_id)
            
            if not persona1 or not persona2:
                await websocket.send_json({
                    "event": "error",
                    "data": {
                        "message": "Persona not found"
                    }
                })
                continue
            
            # 대화 생성 및 스트리밍
            try:
                # 대화 시작 이벤트 전송
                await websocket.send_json({
                    "event": "dialogue_start",
                    "data": {
                        "topic": request_model.topic,
                        "persona1": persona1.name,
                        "persona2": persona2.name,
                        "turns": request_model.turns
                    }
                })
                
                # 대화 생성 및 각 청크를 웹소켓으로 전송
                async for message in conversation_generator.generate_dialogue_stream(
                    persona1, persona2, request_model.topic, request_model.turns
                ):
                    await websocket.send_json(message)
                
                # 대화 완료 이벤트 전송
                await websocket.send_json({
                    "event": "dialogue_complete",
                    "data": {
                        "topic": request_model.topic
                    }
                })
                
            except Exception as e:
                await websocket.send_json({
                    "event": "error",
                    "data": {
                        "message": f"Error generating dialogue: {str(e)}"
                    }
                })
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "event": "error",
                "data": {
                    "message": f"Unexpected error: {str(e)}"
                }
            })
        except:
            pass