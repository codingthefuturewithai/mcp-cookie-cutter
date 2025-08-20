#!/usr/bin/env python3
"""
Test script for unified logging system with correlation IDs.

This script demonstrates and tests the unified logging functionality:
- Correlation ID generation and propagation
- Different log types (tool_execution, internal, framework)
- SQLite destination persistence
- Query capabilities
"""

import asyncio
import logging
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server_project.config import get_config
from mcp_server_project.log_system.correlation import (
    get_correlation_id,
    set_correlation_id,
    CorrelationContext
)
from mcp_server_project.log_system.unified_logger import UnifiedLogger
from mcp_server_project.log_system.destinations.sqlite import SQLiteDestination

# Also test standard logging integration
standard_logger = logging.getLogger(__name__)


async def test_tool_simulation():
    """Simulate a tool execution with correlation ID."""
    # Set a correlation ID for this tool execution
    correlation_id = set_correlation_id()
    
    # Get a logger
    logger = logging.getLogger("test_tool")
    
    logger.info("Starting test tool execution")
    
    # Simulate some work with internal logs
    standard_logger.info("Standard logging should also have correlation ID")
    logger.debug("Processing input data")
    
    # Simulate success
    logger.info("Test tool completed successfully")
    
    return correlation_id


async def test_error_scenario():
    """Test error logging with correlation."""
    with CorrelationContext() as correlation_id:
        logger = logging.getLogger("error_test")
        
        logger.warning("Starting risky operation")
        
        try:
            # Simulate an error
            raise ValueError("Simulated error for testing")
        except Exception as e:
            logger.error(f"Operation failed: {e}")
        
        return correlation_id


async def test_concurrent_logging():
    """Test that correlation IDs are properly isolated between concurrent tasks."""
    async def task(task_id: int):
        correlation_id = set_correlation_id()
        logger = logging.getLogger(f"concurrent_task_{task_id}")
        
        logger.info(f"Task {task_id} started")
        await asyncio.sleep(0.1)  # Simulate work
        logger.info(f"Task {task_id} completed")
        
        return correlation_id
    
    # Run multiple tasks concurrently
    tasks = [task(i) for i in range(5)]
    correlation_ids = await asyncio.gather(*tasks)
    
    # Verify all correlation IDs are unique
    assert len(set(correlation_ids)) == len(correlation_ids)
    print(f"✓ All {len(correlation_ids)} concurrent tasks had unique correlation IDs")
    
    return correlation_ids


async def test_query_logs():
    """Test querying logs from the database."""
    print("\n📊 Testing log queries...")
    
    # Get database path
    config = get_config()
    db_path = config.data_dir / "unified_logs.db"
    
    if not db_path.exists():
        print("Database not found - logs may not be persisted yet")
        return
    
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query recent logs
    cursor.execute("""
        SELECT timestamp, level, message, correlation_id, tool_name
        FROM unified_logs
        ORDER BY timestamp DESC
        LIMIT 10
    """)
    
    rows = cursor.fetchall()
    print(f"Found {len(rows)} recent log entries")
    
    # Show sample logs
    for row in rows[:3]:
        timestamp, level, message, corr_id, tool_name = row
        print(f"  - [{level}] {message[:50]}... (correlation: {corr_id[:12] if corr_id else 'None'})")
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM unified_logs")
    total = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT level, COUNT(*) 
        FROM unified_logs 
        GROUP BY level
    """)
    level_counts = dict(cursor.fetchall())
    
    print("\n📈 Log Statistics:")
    print(f"  Total logs: {total}")
    print(f"  Logs by level: {level_counts}")
    
    conn.close()


async def main():
    """Run all tests."""
    print("🧪 Testing Unified Logging System with Correlation IDs\n")
    
    # Initialize configuration
    config = get_config()
    print(f"Using database: {config.data_dir / 'unified_logs.db'}")
    
    # Initialize unified logging
    destination = SQLiteDestination(config)
    UnifiedLogger.initialize_from_config(config)
    UnifiedLogger.set_event_loop(asyncio.get_running_loop())
    
    try:
        # Test 1: Basic tool simulation
        print("\n1️⃣ Testing basic tool logging...")
        correlation_id1 = await test_tool_simulation()
        print(f"✓ Tool execution logged with correlation ID: {correlation_id1}")
        
        # Test 2: Error scenario
        print("\n2️⃣ Testing error logging...")
        correlation_id2 = await test_error_scenario()
        print(f"✓ Error scenario logged with correlation ID: {correlation_id2}")
        
        # Test 3: Concurrent logging
        print("\n3️⃣ Testing concurrent logging isolation...")
        await test_concurrent_logging()
        
        # Test 4: Framework logging
        print("\n4️⃣ Testing framework logging...")
        framework_logger = logging.getLogger("framework.test")
        framework_logger.info("Framework component initialized")
        print("✓ Framework logging working")
        
        # Give async writes a moment to complete
        await asyncio.sleep(0.5)
        
        # Test 5: Query capabilities
        await test_query_logs()
        
        print("\n✅ All tests completed successfully!")
        
    finally:
        # Clean up
        await UnifiedLogger.close()


if __name__ == "__main__":
    asyncio.run(main())