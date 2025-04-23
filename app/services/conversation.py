from typing import List, Dict, Any, AsyncGenerator
from app.config import settings
from app.models.schemas import PersonaModel, MessageModel
from app.services.ollama import OllamaService
import asyncio

class ConversationGenerator:
    def __init__(self, ollama_service: OllamaService, model=settings.DEFAULT_MODEL):
        self.ollama_service = ollama_service
        self.model = model
        
    async def generate_dialogue(self, persona1: PersonaModel, persona2: PersonaModel, topic: str, turns: int = 3) -> List[MessageModel]:
        """두 페르소나 간의 대화 생성"""
        conversation = []
        current_context = f"주제: {topic}\n\n"
        
        # 첫 발언 생성
        first_prompt = f"{current_context}당신은 {persona1.name}입니다. {topic}에 대한 당신의 견해를 말하세요. 당신은 {persona1.belief}라고 믿습니다."
        first_message = await self.ollama_service.generate_response(
            self.model, 
            first_prompt, 
            persona1.system_prompt
        )
        
        conversation.append(MessageModel(speaker=persona1.name, message=first_message))
        current_context += f"{persona1.name}: {first_message}\n"
        
        # 대화 턴 생성
        for i in range(turns):
            # 현재 발언자와 청자 전환
            current_persona = persona2 if i % 2 == 0 else persona1
            previous_persona = persona1 if i % 2 == 0 else persona2
            
            next_prompt = (
                f"{current_context}\n"
                f"당신은 {current_persona.name}입니다. "
                f"당신은 {current_persona.belief}라고 믿고, {current_persona.tone} 말투를 사용합니다. "
                f"{previous_persona.name}의 이전 발언에 대한 응답을 하세요. "
                f"주제는 '{topic}'입니다."
            )
            
            next_message = await self.ollama_service.generate_response(
                self.model,
                next_prompt,
                current_persona.system_prompt
            )
            
            conversation.append(MessageModel(speaker=current_persona.name, message=next_message))
            current_context += f"{current_persona.name}: {next_message}\n"
            
        return conversation
    
    async def generate_dialogue_stream(
        self, persona1: PersonaModel, persona2: PersonaModel, topic: str, turns: int = 3
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """두 페르소나 간의 대화를 스트리밍 방식으로 생성"""
        current_context = f"주제: {topic}\n\n"
        
        # 첫 발언 생성
        first_prompt = f"{current_context}당신은 {persona1.name}입니다. {topic}에 대한 당신의 견해를 말하세요. 당신은 {persona1.belief}라고 믿습니다."
        
        # 첫 메시지 생성 시작 이벤트 전송
        yield {
            "event": "message_start",
            "data": {
                "speaker": persona1.name,
                "turn": 0
            }
        }
        
        # 첫 메시지 생성 및 스트리밍
        full_message = ""
        async for message_chunk in self.ollama_service.generate_response_stream(
            self.model, first_prompt, persona1.system_prompt
        ):
            full_message += message_chunk
            yield {
                "event": "message_chunk",
                "data": {
                    "speaker": persona1.name,
                    "chunk": message_chunk,
                    "turn": 0
                }
            }
        
        # 첫 메시지 완료 이벤트 전송
        yield {
            "event": "message_complete",
            "data": {
                "speaker": persona1.name,
                "message": full_message,
                "turn": 0
            }
        }
        
        current_context += f"{persona1.name}: {full_message}\n"
        
        # 대화 턴 생성
        for i in range(turns):
            # 현재 발언자와 청자 전환
            current_persona = persona2 if i % 2 == 0 else persona1
            previous_persona = persona1 if i % 2 == 0 else persona2
            turn_number = i + 1
            
            # 턴 시작 이벤트 전송
            yield {
                "event": "message_start",
                "data": {
                    "speaker": current_persona.name,
                    "turn": turn_number
                }
            }
            
            next_prompt = (
                f"{current_context}\n"
                f"당신은 {current_persona.name}입니다. "
                f"당신은 {current_persona.belief}라고 믿고, {current_persona.tone} 말투를 사용합니다. "
                f"{previous_persona.name}의 이전 발언에 대한 응답을 하세요. "
                f"주제는 '{topic}'입니다."
            )
            
            # 메시지 생성 및 스트리밍
            full_message = ""
            async for message_chunk in self.ollama_service.generate_response_stream(
                self.model, next_prompt, current_persona.system_prompt
            ):
                full_message += message_chunk
                yield {
                    "event": "message_chunk",
                    "data": {
                        "speaker": current_persona.name,
                        "chunk": message_chunk,
                        "turn": turn_number
                    }
                }
            
            # 메시지 완료 이벤트 전송
            yield {
                "event": "message_complete",
                "data": {
                    "speaker": current_persona.name,
                    "message": full_message,
                    "turn": turn_number
                }
            }
            
            current_context += f"{current_persona.name}: {full_message}\n"
            
            # 잠시 대기하여 메시지 읽을 시간 제공
            await asyncio.sleep(0.5)