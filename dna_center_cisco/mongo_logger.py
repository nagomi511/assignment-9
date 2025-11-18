from pymongo import MongoClient
from datetime import datetime
from django.conf import settings

class MongoLogger:
    def __init__(self):
        try:
            self.client = MongoClient(settings.MONGODB_URI)
            self.db = self.client[settings.MONGODB_DB]
            self.collection = self.db['api_logs']
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            self.collection = None
    
    def log_request(self, action, device_ip=None, success=True, error=None):
        """Log API request to MongoDB"""
        if self.collection is None:  # ← CAMBIO AQUÍ: usar "is None"
            print("MongoDB not available - skipping log")
            return False
        
        try:
            log_entry = {
                'timestamp': datetime.now(),
                'action': action,
                'device_ip': device_ip,
                'success': success,
                'error': error
            }
            self.collection.insert_one(log_entry)
            return True
        except Exception as e:
            print(f"Failed to log to MongoDB: {e}")
            return False