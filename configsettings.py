"""
Project Mnemosyne - Configuration Management
Event-sourced architecture configuration with memory-conscious defaults.
"""
import os
import json
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum
import logging

class Environment(Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"
    TEST = "test"

@dataclass
class MemoryThresholds:
    """Memory optimization targets - crystalline lattice approach"""
    CRITICAL_RAM_PERCENT: float = 85.0  # Mission success criterion
    TARGET_REDUCTION_PERCENT: float = 25.0  # 25% RAM reduction target
    STREAM_BUFFER_SIZE: int = 100  # Events in memory buffer
    EVENT_CHUNK_SIZE: int = 50  # Events per Firestore batch
    OPPORTUNITY_MESH_NODES: int = 100  # Max concurrent opportunity evaluations

@dataclass
class ScoutConfig:
    """Capital-efficient crypto scout configuration"""
    MIN_OPPORTUNITY_AMOUNT: float = 0.10  # $0.10 minimum
    MAX_TEST_TRADE: float = 1.00  # $1.00 maximum (mission requirement)
    EXCHANGES: list = field(default_factory=lambda: ["binance", "kraken", "coinbase"])
    EVALUATION_INTERVAL_SECONDS: int = 30
    PROFITABILITY_THRESHOLD: float = 0.015  # 1.5% minimum profit

@dataclass
class FirebaseConfig:
    """Firebase configuration - PRIMARY state management"""
    project_id: Optional[str] = None
    credential_path: str = "./config/firebase_key.json"
    database_url: Optional[str] = None
    collections: Dict[str, str] = field(default_factory=lambda: {
        "events": "event_stream",
        "opportunities": "latent_opportunity_mesh",
        "trades": "scout_executions",
        "metrics": "memory_metrics"
    })

@dataclass
class OpenClawConfig:
    """Legacy OpenClaw interface configuration"""
    enable_legacy_buffers: bool = False  # Default: disabled for memory efficiency
    migration_batch_size: int = 1000
    retention_days: int = 7  # Aggressive data retention policy

class ConfigManager:
    """Singleton configuration manager with validation"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.environment = Environment(os.getenv("MNEMOSYNE_ENV", "dev"))
        self.memory = MemoryThresholds()
        self.scout = ScoutConfig()
        self.firebase = FirebaseConfig()
        self.openclaw = OpenClawConfig()
        
        # Load Firebase config if exists
        self._load_firebase_config()
        
        # Initialize logging
        self._setup_logging()
        
        self._initialized = True
    
    def _load_firebase_config(self):
        """Load Firebase configuration safely"""
        try:
            if os.path.exists(self.firebase.credential_path):
                with open(self.firebase.credential_path, 'r') as