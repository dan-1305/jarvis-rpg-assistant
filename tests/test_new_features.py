import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import os

sys.path.insert(0, str(Path(__file__).parent.parent))

class TestConfigModule:
    
    def test_config_module_imports(self):
        """Test that config module can be imported"""
        import jarvis_core.config as config
        
        assert hasattr(config, 'BASE_DIR')
        assert hasattr(config, 'DATA_DIR')
        assert hasattr(config, 'DB_PATH')
    
    def test_config_paths_exist(self):
        """Test that config defines required paths"""
        from jarvis_core.config import BASE_DIR, DATA_DIR, DB_PATH
        
        assert BASE_DIR is not None
        assert DATA_DIR is not None
        assert DB_PATH is not None


class TestKeyManager:
    
    def test_key_manager_basic(self):
        """Test key manager basic functionality"""
        from jarvis_core.key_manager import KeyManager
        
        km = KeyManager(api_keys=["key1", "key2"])
        
        assert km is not None
        assert len(km._keys) == 2
    
    def test_key_rotation(self):
        """Test key rotation mechanism"""
        from jarvis_core.key_manager import KeyManager
        
        km = KeyManager(api_keys=["key1", "key2", "key3"])
        
        key1 = km.get_next_key()
        key2 = km.get_next_key()
        
        assert key1 in ["key1", "key2", "key3"]
        assert key2 in ["key1", "key2", "key3"]


