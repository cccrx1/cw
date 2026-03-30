from typing import Any, Dict, Optional
from datetime import datetime
import uuid


class Response:
    @staticmethod
    def success(data: Any = None, message: str = "ok") -> Dict[str, Any]:
        return {
            "code": 0,
            "message": message,
            "data": data,
            "request_id": f"req_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def error(code: int, message: str) -> Dict[str, Any]:
        return {
            "code": code,
            "message": message,
            "data": None,
            "request_id": f"req_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.now().isoformat()
        }