# jarvis_core/database.py
import os
import sqlite3
import logging
from contextlib import contextmanager
from typing import Dict, List, Optional, Tuple, Any, Iterator
from datetime import datetime, date, timedelta
from pathlib import Path

# Constants
DEFAULT_DB_PATH = "data/jarvis.db"
DEFAULT_DATA_DIR = "data"

# Database Schema Version
SCHEMA_VERSION = 1

# User Stats Constants
DEFAULT_LEVEL = 1
DEFAULT_XP = 0
DEFAULT_HP = 100
MAX_HP = 100
MAX_LEVEL = 100
XP_MULTIPLIER = 1.5
HP_REGEN_RATE = 10  # HP regenerated per day

# Vocabulary Learning Constants
VOCAB_NEW_LIMIT = 5
VOCAB_REVIEW_LIMIT = 10
VOCAB_MASTERY_THRESHOLD = 5  # Number of correct reviews to master a word

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Base exception for database related errors."""
    pass


class DatabaseManager:
    """Manages all database operations for the Jarvis application."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize the database manager."""
        self.db_path = db_path or self._get_default_db_path()
        self._init_db()

    @staticmethod
    def _get_default_db_path() -> str:
        """Xác định đường dẫn database một cách thông minh."""
        try:
            from jarvis_core.config import DATA_DIR
            return os.path.join(DATA_DIR, "jarvis.db")
        except (ImportError, ModuleNotFoundError):
            base_dir = Path(__file__).resolve().parent.parent
            data_dir = base_dir / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Fallback to dynamic path: {data_dir / 'jarvis.db'}")
            return str(data_dir / "jarvis.db")

    @contextmanager
    def _get_connection(self) -> Iterator[sqlite3.Connection]:
        """Context manager for database connections with transaction lock."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA busy_timeout = 30000")
            conn.execute("BEGIN IMMEDIATE")
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise DatabaseError(f"Database operation failed: {e}") from e
        finally:
            if conn:
                conn.close()

    # --- 3 HÀM NÀY ĐÃ ĐƯỢC ĐƯA RA NGOÀI (Ngang hàng với _get_connection) ---

    def _execute(self, query: str, params: Tuple[Any, ...] = ()) -> None:
        """Execute a write operation (INSERT/UPDATE/DELETE)."""
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                logger.error(f"Query failed: {query[:100]}... - {e}")
                raise DatabaseError(f"Query execution failed: {e}") from e

    def _fetch_one(self, query: str, params: Tuple[Any, ...] = ()) -> Optional[sqlite3.Row]:
        """Execute a query and return a single row."""
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchone()
            except sqlite3.Error as e:
                logger.error(f"Fetch one failed: {e}")
                raise DatabaseError(f"Fetch one failed: {e}") from e

    def _fetch_all(self, query: str, params: Tuple[Any, ...] = ()) -> List[sqlite3.Row]:
        """Execute a query and return all rows."""
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
            except sqlite3.Error as e:
                logger.error(f"Fetch all failed: {e}")
                raise DatabaseError(f"Fetch all failed: {e}") from e

    # -----------------------------------------------------------------------

    def _init_db(self) -> None:
        """Initialize the database schema."""
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("PRAGMA journal_mode=WAL")

                # Create tables
                cursor.executescript("""
                                     CREATE TABLE IF NOT EXISTS user_profile
                                     (
                                         id
                                         INTEGER
                                         PRIMARY
                                         KEY
                                         AUTOINCREMENT,
                                         level
                                         INTEGER
                                         NOT
                                         NULL
                                         DEFAULT
                                         1,
                                         xp
                                         INTEGER
                                         NOT
                                         NULL
                                         DEFAULT
                                         0,
                                         hp
                                         INTEGER
                                         NOT
                                         NULL
                                         DEFAULT
                                         100,
                                         status
                                         TEXT,
                                         class
                                         TEXT,
                                         last_update
                                         DATE
                                         DEFAULT
                                         CURRENT_DATE
                                     );

                                     CREATE TABLE IF NOT EXISTS vocab
                                     (
                                         id
                                         INTEGER
                                         PRIMARY
                                         KEY
                                         AUTOINCREMENT,
                                         word
                                         TEXT
                                         UNIQUE
                                         NOT
                                         NULL,
                                         meaning
                                         TEXT,
                                         learning_level
                                         INTEGER
                                         DEFAULT
                                         0,
                                         correct_count
                                         INTEGER
                                         DEFAULT
                                         0,
                                         wrong_count
                                         INTEGER
                                         DEFAULT
                                         0,
                                         next_review
                                         DATE,
                                         created_at
                                         DATE
                                         DEFAULT
                                         CURRENT_DATE,
                                         last_reviewed
                                         DATE,
                                         tags
                                         TEXT
                                     );

                                     CREATE INDEX IF NOT EXISTS idx_vocab_review ON vocab(next_review);
                                     CREATE INDEX IF NOT EXISTS idx_vocab_word ON vocab(word);

                                     -- FIX: Bắt buộc ID phải là 1. Nếu ID 1 đã có thì IGNORE (Bỏ qua).
                                     INSERT
                                     OR IGNORE INTO user_profile (id, level, xp, hp, status)
                    VALUES (1, 1, 0, 100, 'active');
                                     """)

                # Update schema version
                cursor.execute("CREATE TABLE IF NOT EXISTS schema_info (version INTEGER PRIMARY KEY)")
                cursor.execute("INSERT OR IGNORE INTO schema_info (version) VALUES (?)", (SCHEMA_VERSION,))

                conn.commit()
                logger.info("Database initialized successfully")

            except sqlite3.Error as e:
                conn.rollback()
                logger.error(f"Failed to initialize database: {e}")
                raise DatabaseError(f"Database initialization failed: {e}") from e

                # Update schema version (Tách lệnh riêng)
                cursor.execute("CREATE TABLE IF NOT EXISTS schema_info (version INTEGER PRIMARY KEY)")
                cursor.execute("INSERT OR IGNORE INTO schema_info (version) VALUES (?)", (SCHEMA_VERSION,))

                conn.commit()
                logger.info("Database initialized successfully")

            except sqlite3.Error as e:
                conn.rollback()
                logger.error(f"Failed to initialize database: {e}")
                raise DatabaseError(f"Database initialization failed: {e}") from e

    # User Profile Methods
    def get_user_profile(self) -> Dict[str, Any]:
        row = self._fetch_one("SELECT * FROM user_profile WHERE id = 1")
        if not row:
            return self._create_default_profile()
        return dict(row)

    def _create_default_profile(self) -> Dict[str, Any]:
        default_profile = {
            "id": 1,
            "level": DEFAULT_LEVEL,
            "xp": DEFAULT_XP,
            "hp": DEFAULT_HP,
            "status": "active",
            "class": "beginner",
            "last_update": date.today().isoformat()
        }
        self._execute(
            "INSERT INTO user_profile (id, level, xp, hp, status, class) VALUES (?, ?, ?, ?, ?, ?)",
            (1, DEFAULT_LEVEL, DEFAULT_XP, DEFAULT_HP, "active", "beginner")
        )
        return default_profile

    def update_user_stats(self, xp_gained: int = 0, hp_change: int = 0, new_status: Optional[str] = None,
                          new_class: Optional[str] = None) -> Dict[str, Any]:
        if not isinstance(xp_gained, int) or not isinstance(hp_change, int):
            raise ValueError("xp_gained and hp_change must be integers")

        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user_profile WHERE id = 1")
                profile = cursor.fetchone()

                if not profile:
                    profile = self._create_default_profile()
                else:
                    profile = dict(profile)

                new_xp = profile["xp"] + xp_gained
                new_level = profile["level"]
                xp_needed = int((new_level ** XP_MULTIPLIER) * 100)

                while new_xp >= xp_needed and new_level < MAX_LEVEL:
                    new_xp -= xp_needed
                    new_level += 1
                    xp_needed = int((new_level ** XP_MULTIPLIER) * 100)
                    logger.info(f"Level up! New level: {new_level}")

                new_hp = min(max(0, profile["hp"] + hp_change), MAX_HP)

                update_fields = []
                params = []

                if xp_gained != 0:
                    update_fields.append("xp = ?")
                    params.append(new_xp)
                if hp_change != 0:
                    update_fields.append("hp = ?")
                    params.append(new_hp)
                if new_status is not None:
                    update_fields.append("status = ?")
                    params.append(new_status)
                if new_class is not None:
                    update_fields.append("class = ?")
                    params.append(new_class)
                if new_level != profile["level"]:
                    update_fields.append("level = ?")
                    params.append(new_level)

                update_fields.append("last_update = ?")
                params.append(date.today().isoformat())

                if update_fields:
                    query = f"UPDATE user_profile SET {', '.join(update_fields)} WHERE id = 1"
                    cursor.execute(query, params)
                    conn.commit()

                return self.get_user_profile()

            except sqlite3.Error as e:
                conn.rollback()
                logger.error(f"Failed to update user stats: {e}")
                raise DatabaseError(f"Failed to update user stats: {e}") from e

    # Vocabulary Methods
    def add_vocab(self, word: str, meaning: str, tags: Optional[List[str]] = None) -> bool:
        try:
            tags_str = ",".join(tags) if tags else ""
            next_review = date.today() + timedelta(days=1)
            self._execute(
                """
                INSERT INTO vocab (word, meaning, tags, next_review)
                VALUES (?, ?, ?, ?) ON CONFLICT(word) DO
                UPDATE SET
                    meaning = excluded.meaning,
                    tags = COALESCE (excluded.tags, tags)
                """,
                (word, meaning, tags_str, next_review)
            )
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"Word already exists: {word}")
            return False

    def get_due_vocab(self, limit: int = VOCAB_REVIEW_LIMIT) -> List[Dict[str, Any]]:
        today = date.today().isoformat()
        rows = self._fetch_all("""
                               SELECT *
                               FROM vocab
                               WHERE next_review <= ?
                               ORDER BY next_review ASC LIMIT ?
                               """, (today, limit))
        return [dict(row) for row in rows]

    def get_review_candidates(self, mode: str = "new", limit: int = 5) -> List[Dict[str, Any]]:
        today = date.today().isoformat()
        if mode.lower() == "new":
            rows = self._fetch_all("""
                                   SELECT *
                                   FROM vocab
                                   WHERE last_reviewed IS NULL
                                   ORDER BY created_at ASC LIMIT ?
                                   """, (limit,))
        else:
            rows = self._fetch_all("""
                                   SELECT *
                                   FROM vocab
                                   WHERE next_review <= ?
                                     AND last_reviewed IS NOT NULL
                                   ORDER BY next_review ASC, learning_level ASC LIMIT ?
                                   """, (today, limit))
        return [dict(row) for row in rows]

    def update_vocab_mastery(self, word: str, is_remembered: bool) -> bool:
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT learning_level, correct_count, wrong_count FROM vocab WHERE word = ?", (word,))
                result = cursor.fetchone()

                if not result:
                    logger.warning(f"Word not found: {word}")
                    return False

                current_level = result["learning_level"]
                correct_count = result["correct_count"]
                wrong_count = result["wrong_count"]

                if is_remembered:
                    new_level = min(current_level + 1, 10)
                    correct_count += 1
                else:
                    new_level = max(0, current_level - 1)
                    wrong_count += 1

                days_to_add = self._calculate_next_review_interval(new_level)
                next_review = date.today() + timedelta(days=days_to_add)

                cursor.execute("""
                               UPDATE vocab
                               SET learning_level = ?,
                                   correct_count  = ?,
                                   wrong_count    = ?,
                                   next_review    = ?,
                                   last_reviewed  = ?
                               WHERE word = ?
                               """,
                               (new_level, correct_count, wrong_count, next_review, date.today().isoformat(), word))

                conn.commit()
                logger.info(f"Updated word: {word} (new level: {new_level})")
                return True

            except sqlite3.Error as e:
                conn.rollback()
                logger.error(f"Failed to update word mastery: {e}")
                return False

    @staticmethod
    def _calculate_next_review_interval(level: int) -> int:
        if level == 0:
            return 1
        elif level == 1:
            return 3
        elif level == 2:
            return 7
        elif level == 3:
            return 14
        elif level == 4:
            return 30
        elif level == 5:
            return 60
        elif level == 6:
            return 90
        else:
            return 180


# Singleton instance
_db_instance = None


def get_database() -> DatabaseManager:
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance


# Backward compatibility functions
def init_db(): get_database()


def get_connection(): return get_database()._get_connection()


def get_due_vocab(limit: int = 10): return get_database().get_due_vocab(limit)


def get_review_candidates(mode: str = "new", limit: int = 5): return get_database().get_review_candidates(mode, limit)


def add_vocab(word: str, meaning: str, tags: list = None): return get_database().add_vocab(word, meaning, tags)


def update_vocab_mastery(word: str, is_remembered: bool): return get_database().update_vocab_mastery(word,
                                                                                                     is_remembered)
# ... (các hàm wrapper cũ: init_db, get_connection, vocab...)

# --- THÊM 2 HÀM NÀY ĐỂ CỨU BOT_EVOLVE ---
def get_user_profile(): return get_database().get_user_profile()

def update_user_stats(xp_gained: int = 0, hp_change: int = 0, new_status: str = None, new_class: str = None):
    # Lưu ý: Hàm này trả về Dict (Profile mới), không phải (success, msg)
    return get_database().update_user_stats(xp_gained, hp_change, new_status, new_class)
# ----------------------------------------