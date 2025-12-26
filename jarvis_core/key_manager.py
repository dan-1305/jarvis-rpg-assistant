# jarvis_core/key_manager.py (FIXED Time-Based Cooldown Logic)

import logging
import os
import time
from typing import List, Dict

from dotenv import load_dotenv

load_dotenv()


class KeyExhaustedError(Exception):
    """Exception raised when all API keys are exhausted or rate-limited."""
    pass


class KeyManager:
    COOLDOWN_SECONDS: int = 60

    def __init__(self, api_keys: List[str]):
        if not api_keys:
            raise ValueError("Danh sách API keys không được rỗng.")

        self._keys: List[str] = api_keys
        self._key_index: int = 0
        self._exhausted_keys: Dict[str, float] = {}
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    def get_next_key(self) -> str:
        """
        Trả về key tiếp theo theo cơ chế Round-Robin, bỏ qua các key đang trong Cooldown.
        Sử dụng vòng lặp N lần để đảm bảo kiểm tra tất cả Keys.
        """
        num_keys = len(self._keys)
        current_time = time.time()

        # FIX LOGIC: Lặp tối đa num_keys lần để kiểm tra tất cả keys theo thứ tự
        for _ in range(num_keys):
            current_key = self._keys[self._key_index]
            self._key_index = (self._key_index + 1) % num_keys  # Tăng index

            last_error_time = self._exhausted_keys.get(current_key)

            if last_error_time is None:
                # 1. Key chưa bị lỗi -> Dùng
                return current_key

            # 2. Key bị lỗi, kiểm tra Cooldown
            if current_time - last_error_time > self.COOLDOWN_SECONDS:
                # Key đã "nguội" -> Reset và dùng
                del self._exhausted_keys[current_key]
                logging.info(f"Key {current_key[:5]}... đã hết Cooldown (Reset).")
                return current_key
            else:
                # Key vẫn đang trong thời gian phạt -> Bỏ qua và chuyển sang Key tiếp theo
                logging.warning(
                    f"Key {current_key[:5]}... đang trong Cooldown ({int(self.COOLDOWN_SECONDS - (current_time - last_error_time))}s). Bỏ qua.")
                continue  # Tiếp tục vòng lặp

        # Nếu vòng lặp kết thúc mà không có Key nào được trả về (tất cả đều đang Cooldown)
        raise KeyExhaustedError("Tất cả Keys đang trong thời gian Cooldown. Thử lại sau.")

    def mark_key_exhausted(self, key: str):
        """
        Đánh dấu key này đã hết hạn mức (Quota Exceeded) hoặc gặp lỗi Rate Limit.
        Lưu lại thời gian lỗi để tính Cooldown.
        """
        self._exhausted_keys[key] = time.time()
        logging.warning(f"🚫 Key {key[:5]}... bị đánh dấu Cooldown trong {self.COOLDOWN_SECONDS}s.")

    def reset_exhausted_keys(self):
        """Xóa toàn bộ trạng thái Cooldown. Dùng khi cần reset thủ công."""
        self._exhausted_keys = {}
        logging.info("♻️ Tất cả Keys đã được Reset trạng thái Cooldown.")


# --- Factory Function và Khởi tạo GLOBAL_KEY_MANAGER (Giữ nguyên) ---
def get_global_key_manager() -> KeyManager:
    """Đọc keys từ biến môi trường và trả về KeyManager."""
    keys_str = os.getenv("GEMINI_API_KEYS", "")
    api_keys = [k.strip() for k in keys_str.split(',') if k.strip()]

    if not api_keys:
        logging.error("Lỗi cấu hình: Không tìm thấy GEMINI_API_KEYS hợp lệ.")
        return KeyManager([])

    logging.info(f"🔑 KeyManager đã nạp thành công: {len(api_keys)} Keys.")
    return KeyManager(api_keys)


# Khởi tạo KeyManager toàn cục (Singleton)
try:
    GLOBAL_KEY_MANAGER = get_global_key_manager()
except ValueError as e:
    logging.error(f"Khởi tạo KeyManager thất bại: {e}")
    GLOBAL_KEY_MANAGER = None
