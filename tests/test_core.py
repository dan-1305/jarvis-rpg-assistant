import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis_core.database import DatabaseManager
from jarvis_core.key_manager import KeyManager
import tempfile
import os

@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_path = temp_file.name
    temp_file.close()
    
    db = DatabaseManager(temp_path)
    yield db
    
    if os.path.exists(temp_path):
        os.unlink(temp_path)

@pytest.fixture
def key_manager():
    """Create a key manager instance for testing"""
    return KeyManager(api_keys=["test-key-1", "test-key-2", "test-key-3"])

class TestDatabaseManager:
    
    def test_init_creates_tables(self, temp_db):
        """Test that database initialization creates all required tables"""
        with temp_db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ['users', 'vocabulary', 'user_vocabulary', 'tasks', 'user_stats']
            for table in expected_tables:
                assert table in tables, f"Table {table} not created"
    
    def test_add_user(self, temp_db):
        """Test adding a new user"""
        user_id = 12345
        username = "testuser"
        
        temp_db.add_user(user_id, username)
        
        user = temp_db.get_user(user_id)
        assert user is not None
        assert user['user_id'] == user_id
        assert user['username'] == username
    
    def test_get_nonexistent_user(self, temp_db):
        """Test getting a user that doesn't exist"""
        user = temp_db.get_user(99999)
        assert user is None
    
    def test_update_user_stats(self, temp_db):
        """Test updating user stats"""
        user_id = 12345
        temp_db.add_user(user_id, "testuser")
        
        temp_db.update_user_stats(user_id, level=5, xp=100, hp=80)
        
        stats = temp_db.get_user_stats(user_id)
        assert stats['level'] == 5
        assert stats['xp'] == 100
        assert stats['hp'] == 80
    
    def test_add_task(self, temp_db):
        """Test adding a task"""
        user_id = 12345
        temp_db.add_user(user_id, "testuser")
        
        task_id = temp_db.add_task(
            user_id=user_id,
            task_name="Test Task",
            description="Test Description",
            priority="high"
        )
        
        assert task_id is not None
        
        tasks = temp_db.get_tasks(user_id)
        assert len(tasks) > 0
        assert tasks[0]['task_name'] == "Test Task"
    
    def test_complete_task(self, temp_db):
        """Test marking a task as complete"""
        user_id = 12345
        temp_db.add_user(user_id, "testuser")
        
        task_id = temp_db.add_task(user_id, "Test Task")
        temp_db.complete_task(task_id)
        
        with temp_db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM tasks WHERE task_id = ?", (task_id,))
            status = cursor.fetchone()[0]
            assert status == "completed"
    
    def test_add_vocabulary(self, temp_db):
        """Test adding vocabulary"""
        vocab_id = temp_db.add_vocabulary(
            word="hello",
            translation="xin chào",
            example="Hello world",
            category="greeting"
        )
        
        assert vocab_id is not None
    
    def test_get_vocabulary_for_learning(self, temp_db):
        """Test getting vocabulary for learning"""
        user_id = 12345
        temp_db.add_user(user_id, "testuser")
        
        for i in range(10):
            temp_db.add_vocabulary(f"word{i}", f"translation{i}")
        
        vocab_list = temp_db.get_vocabulary_for_learning(user_id, limit=5)
        assert len(vocab_list) <= 5
    
    def test_update_vocabulary_progress(self, temp_db):
        """Test updating vocabulary learning progress"""
        user_id = 12345
        temp_db.add_user(user_id, "testuser")
        
        vocab_id = temp_db.add_vocabulary("test", "thử nghiệm")
        
        temp_db.update_vocabulary_progress(user_id, vocab_id, correct=True)
        
        with temp_db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT review_count FROM user_vocabulary WHERE user_id = ? AND vocab_id = ?",
                (user_id, vocab_id)
            )
            result = cursor.fetchone()
            assert result is not None
            assert result[0] > 0
    
    def test_get_user_stats_creates_if_not_exists(self, temp_db):
        """Test that getting stats creates entry if it doesn't exist"""
        user_id = 12345
        temp_db.add_user(user_id, "testuser")
        
        stats = temp_db.get_user_stats(user_id)
        assert stats is not None
        assert stats['level'] == 1
        assert stats['xp'] == 0
        assert stats['hp'] == 100
    
    def test_database_error_handling(self, temp_db):
        """Test that database errors are properly handled"""
        with pytest.raises(Exception):
            temp_db._execute("INVALID SQL QUERY")
    
    def test_transaction_rollback_on_error(self, temp_db):
        """Test that transactions rollback on error"""
        user_id = 12345
        temp_db.add_user(user_id, "testuser")
        
        initial_count = len(temp_db.get_tasks(user_id))
        
        try:
            with temp_db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO tasks (user_id, task_name) VALUES (?, ?)",
                    (user_id, "Test")
                )
                raise Exception("Simulated error")
        except:
            pass
        
        final_count = len(temp_db.get_tasks(user_id))
        assert initial_count == final_count


class TestKeyManager:
    
    def test_init_key_manager(self, key_manager):
        """Test key manager initialization"""
        assert key_manager is not None
    
    def test_add_key(self, key_manager):
        """Test adding a new key"""
        key = "test-key-12345"
        result = key_manager.add_key(key)
        assert result == True
    
    def test_validate_key(self, key_manager):
        """Test validating a key"""
        key = "valid-test-key"
        key_manager.add_key(key)
        
        is_valid = key_manager.validate_key(key)
        assert is_valid == True
    
    def test_validate_invalid_key(self, key_manager):
        """Test validating an invalid key"""
        is_valid = key_manager.validate_key("invalid-key-xyz")
        assert is_valid == False
    
    def test_use_key(self, key_manager):
        """Test using a key"""
        key = "usable-key"
        key_manager.add_key(key)
        
        result = key_manager.use_key(key, user_id=12345)
        assert result == True
    
    def test_cannot_reuse_key(self, key_manager):
        """Test that a key cannot be reused"""
        key = "one-time-key"
        key_manager.add_key(key)
        
        key_manager.use_key(key, user_id=12345)
        
        result = key_manager.use_key(key, user_id=67890)
        assert result == False
    
    def test_get_key_info(self, key_manager):
        """Test getting key information"""
        key = "info-key"
        key_manager.add_key(key)
        
        info = key_manager.get_key_info(key)
        assert info is not None
        assert info['key'] == key
        assert info['is_used'] == False
    
    def test_list_unused_keys(self, key_manager):
        """Test listing unused keys"""
        key_manager.add_key("unused-1")
        key_manager.add_key("unused-2")
        used_key = "used-key"
        key_manager.add_key(used_key)
        key_manager.use_key(used_key, user_id=123)
        
        unused = key_manager.list_unused_keys()
        assert len(unused) >= 2
        assert any(k['key'] == "unused-1" for k in unused)
        assert not any(k['key'] == used_key for k in unused)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=jarvis_core", "--cov-report=html", "--cov-report=term"])
