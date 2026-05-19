#!/usr/bin/env python3
"""
Builds the MASTER unified n8n workflow JSON
Combines all 4 workflows into ONE production-grade system
ONLY uses genuinely free tools
"""

import json

def build_master_workflow():
    """Build complete unified workflow"""
    
    workflow = {
        "name": "MASTER Job Automation System (Fully Free)",
        "nodes": [],
        "connections": {},
        "settings": {"executionOrder": "v1"},
        "staticData": None,
        "tags": ["job-automation", "ai-powered", "production"],
        "triggerCount": 0,
        "updatedAt": "2024-01-20T00:00:00.000Z",
        "versionId": "1.0.0"
    }
    
    # ========================================
    # SECTION 1: TRIGGER NODES
    # ========================================
    
    # Node 1: Schedule Trigger (Daily)
    workflow["nodes"].append({
        "parameters": {
            "rule": {
                "interval": [{
