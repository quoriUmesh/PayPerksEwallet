import uuid
from datetime import datetime, timedelta
import threading
from db_queries import DatabaseManager


class SessionManager:
    def __init__(self,db, db_path: str = "sessions.db", timeout_minutes: int = 5):
        """
        Initialize session manager
        
        Args:
            db_path: Path to SQLite database file
            timeout_minutes: Session timeout in minutes
        """
        self.db_path = db_path
        self.timeout_minutes = timeout_minutes
        self.lock = threading.Lock()
        self.db = db

    
    def create_session(self, user_id: int) -> str:
        """
        Create a new session for the user
        
        Args:
            user_id: User ID from the database
            
        Returns:
            session_id: Unique session identifier
        """
        with self.lock:
            try:
                session_id = str(uuid.uuid4())
                now = datetime.now()
                expiry = now + timedelta(minutes=self.timeout_minutes)
                self.db.insert_session(user_id,session_id,now,expiry)
                print(session_id)
                return session_id, expiry
            except Exception as e:
                print(f"Session creation error: {e}")
                return None
    
    
    def refresh_session(self, session_id: str):
        """
        Update session's last seen timestamp and extend expiry
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            try:
                db = DatabaseManager()
                now = datetime.now()
                expiry = now + timedelta(minutes=self.timeout_minutes)
                db.update_session(session_id,expiry)
                db.close()
                print('session refreshed')
                return expiry
            except Exception as e:
                print(f"Session refresh error: {e}")
                return False