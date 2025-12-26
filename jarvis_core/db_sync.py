import subprocess
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def sync_database_with_git() -> bool:
    """
    Sync database với git: pull trước khi commit để tránh conflict
    Returns: True nếu thành công, False nếu thất bại
    """
    try:
        repo_root = Path(__file__).resolve().parent.parent
        
        logger.info("Pulling latest changes from git...")
        result = subprocess.run(
            ["git", "pull", "--rebase"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            logger.warning(f"Git pull failed: {result.stderr}")
            return False
        
        logger.info("Git pull successful")
        return True
        
    except subprocess.TimeoutExpired:
        logger.error("Git pull timed out after 30 seconds")
        return False
    except Exception as e:
        logger.error(f"Failed to sync with git: {e}")
        return False

def commit_and_push_database(commit_message: str = "Auto-sync database") -> bool:
    """
    Commit và push database changes
    Returns: True nếu thành công, False nếu thất bại
    """
    try:
        repo_root = Path(__file__).resolve().parent.parent
        
        subprocess.run(
            ["git", "add", "data/jarvis.db"],
            cwd=str(repo_root),
            check=True,
            capture_output=True,
            timeout=10
        )
        
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            if "nothing to commit" in result.stdout.lower():
                logger.info("No changes to commit")
                return True
            logger.warning(f"Git commit failed: {result.stderr}")
            return False
        
        result = subprocess.run(
            ["git", "push"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            logger.error(f"Git push failed: {result.stderr}")
            return False
            
        logger.info("Database successfully synced to git")
        return True
        
    except subprocess.TimeoutExpired:
        logger.error("Git operation timed out")
        return False
    except Exception as e:
        logger.error(f"Failed to commit/push database: {e}")
        return False

def safe_database_update(update_func, commit_msg: str = "Auto-sync database"):
    """
    Wrapper function để safely update database với git sync
    
    Usage:
        def my_update():
            db.add_user(...)
        
        safe_database_update(my_update, "Added new user")
    """
    try:
        if not sync_database_with_git():
            logger.warning("Git pull failed, continuing with update anyway")
        
        result = update_func()
        
        if not commit_and_push_database(commit_msg):
            logger.warning("Failed to sync database to git")
        
        return result
        
    except Exception as e:
        logger.error(f"Database update failed: {e}")
        raise
