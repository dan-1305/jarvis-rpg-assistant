# jarvis_core/ai_agent.py
import os
import time
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv
from pathlib import Path

# Import GLOBAL_KEY_MANAGER từ key_manager.py thay vì duplicate
from jarvis_core.key_manager import GLOBAL_KEY_MANAGER

# Tự động tìm về thư mục gốc của dự án (Jarvis/)
base_path = Path(__file__).resolve().parent.parent
env_path = base_path / '.env'

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    logging.warning(f"KHÔNG TÌM THẤY file .env tại: {env_path}")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
MODEL_PRIORITY = ['gemini-2.5-flash-lite',  'gemini-2.5-flash']
DEFAULT_MODEL = 'gemini-2.5-flash-lite'
MAX_RETRIES = 3
CACHE_TTL = 3600


class AIService:
    """Core AI Service - Trái tim của Jarvis."""

    def __init__(self, key_manager = None):
        self.key_manager = key_manager or GLOBAL_KEY_MANAGER
        self.cache = {}
        self.cache_ttl = CACHE_TTL

    def _get_cached_response(self, prompt: str, model: str) -> Optional[str]:
        """Kiểm tra xem câu hỏi này đã có trong cache chưa."""
        cache_key = f"{model}:{hash(prompt)}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            # Kiểm tra hạn sử dụng (TTL)
            if (datetime.now() - cached['timestamp']).seconds < self.cache_ttl:
                return cached['response']
            # Xóa cache hết hạn
            del self.cache[cache_key]
        return None

    def _update_cache(self, prompt: str, model: str, response: str):
        """Lưu câu trả lời vào cache."""
        cache_key = f"{model}:{hash(prompt)}"
        self.cache[cache_key] = {
            'response': response,
            'timestamp': datetime.now()
        }
        # Dọn dẹp cache nếu quá lớn (giữ 1000 mục mới nhất)
        if len(self.cache) > 1000:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def _call_llm_api(self, prompt: str, model: str = None) -> str:
        """Gọi API Gemini với cơ chế Retry và Key Rotation."""
        model = model or DEFAULT_MODEL
        current_key = self.key_manager.get_next_key()

        try:
            genai.configure(api_key=current_key)
            # Cấu hình model an toàn để tránh bị block nội dung vô lý
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            generative_model = genai.GenerativeModel(model_name=model, safety_settings=safety_settings)

            response = generative_model.generate_content(prompt)
            return response.text

        except Exception as e:
            self.key_manager.report_error(current_key)
            logger.error(f"Lỗi API với key ...{current_key[-4:]}: {str(e)}")
            raise
        finally:
            # Xóa cấu hình key để tránh dùng nhầm cho request sau
            genai.configure(api_key=None)

    def generate_response(self, prompt: str, model: str = None) -> str:
        """Hàm chính để tạo phản hồi (Có Cache + Fallback Model)."""
        model = model or DEFAULT_MODEL

        # 1. Check Cache
        if cached := self._get_cached_response(prompt, model):
            logger.info("-> Serving from Cache (Tốc độ ánh sáng!)")
            return cached

        # 2. Thử lần lượt các Model theo độ ưu tiên
        models_to_try = [model] if model in MODEL_PRIORITY else MODEL_PRIORITY
        last_error = None

        for current_model in models_to_try:
            try:
                # logger.info(f"Đang thử model: {current_model}...")
                response = self._call_llm_api(prompt, current_model)
                self._update_cache(prompt, current_model, response)
                return response
            except Exception as e:
                last_error = e
                logger.warning(f"Model {current_model} thất bại, đang thử cái tiếp theo...")
                continue

        raise RuntimeError(f"Tất cả các model đều thất bại. Lỗi cuối cùng: {str(last_error)}")


# Global instance
ai_service = AIService()


# --- Public API (Các hàm cho module khác gọi) ---

def ask_jarvis(prompt: str) -> str:
    """Hàm giao tiếp cơ bản với Jarvis."""
    try:
        return ai_service.generate_response(prompt)
    except Exception as e:
        logger.error(f"Critical Error in ask_jarvis: {str(e)}")
        return "Xin lỗi The Builder, hệ thống AI đang gặp sự cố kết nối. Vui lòng kiểm tra Log."


def evaluate_evolution(current_profile: dict, completed_tasks: str) -> dict:
    """
    Đánh giá nhiệm vụ để tính XP/HP (RPG System).
    Có xử lý JSON an toàn.
    """
    prompt = f"""
    Bạn là Gamemaster của hệ thống RPG đời thực. Hãy đánh giá các nhiệm vụ sau:
    {completed_tasks}

    Profile hiện tại:
    {json.dumps(current_profile, indent=2)}

    Yêu cầu:
    - Phân tích độ khó của task để tính XP (Dễ: 10-20, Trung bình: 30-50, Khó: 50-100).
    - Nếu task không hoàn thành tốt, trừ HP.
    - Trả về DUY NHẤT một chuỗi JSON thuần (không markdown) với định dạng:
    {{
        "xp_gained": int,
        "hp_change": int,
        "new_status": "string",
        "message": "Lời nhận xét ngắn gọn, hài hước kiểu IT/DevOps"
    }}
    """

    try:
        raw_response = ai_service.generate_response(prompt)

        # --- CLEANUP JSON (Quan trọng) ---
        # Gemini hay trả về ```json ... ```, phải cắt bỏ
        clean_json = raw_response.strip()
        if clean_json.startswith("```"):
            clean_json = clean_json.split("```")[1]
        if clean_json.startswith("json"):
            clean_json = clean_json[4:]
        clean_json = clean_json.strip()
        # ---------------------------------

        result = json.loads(clean_json)
        return {
            'xp_gained': result.get('xp_gained', 0),
            'hp_change': result.get('hp_change', 0),
            'new_status': result.get('new_status', 'active'),
            'message': result.get('message', 'Nhiệm vụ đã được cập nhật!')
        }
    except json.JSONDecodeError:
        logger.error(f"Lỗi Parse JSON từ AI: {raw_response}")
        return {
            'xp_gained': 10,  # Fallback: Cho ít XP an ủi
            'hp_change': 0,
            'new_status': current_profile.get('status', 'active'),
            'message': 'AI bị ngáo JSON, nhưng tôi vẫn cộng cho bạn 10 XP an ủi!'
        }
    except Exception as e:
        logger.error(f"Error in evaluate_evolution: {str(e)}")
        return {
            'xp_gained': 0,
            'hp_change': 0,
            'new_status': current_profile.get('status', 'active'),
            'message': 'Lỗi hệ thống khi đánh giá nhiệm vụ.'
        }


if __name__ == "__main__":
    # Test nhanh khi chạy trực tiếp file này
    print("--- Test Key Rotation & AI ---")
    try:
        print(ask_jarvis("Chào Jarvis, hãy giới thiệu ngắn gọn về bạn bằng 1 câu."))
    except Exception as e:
        print(f"Test Failed: {e}")