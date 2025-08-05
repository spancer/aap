from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAnalyzer(ABC):
    @abstractmethod
    async def analyze_performance(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        pass