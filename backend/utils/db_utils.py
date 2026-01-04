"""
Database utility functions and connection management
"""
import sqlite3
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from config.settings import DB_PATH


class DatabaseError(Exception):
    """Custom database exception"""
    pass


@contextmanager
def get_db_connection():
    """
    Context manager for database connections
    Ensures connections are properly closed
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise DatabaseError(f"Database error: {str(e)}")
    finally:
        conn.close()


def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """
    Execute a SELECT query and return results
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    except DatabaseError as e:
        raise DatabaseError(f"Query execution failed: {str(e)}")


def execute_update(query: str, params: tuple = ()) -> int:
    """
    Execute an INSERT/UPDATE/DELETE query and return affected rows
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    except DatabaseError as e:
        raise DatabaseError(f"Update execution failed: {str(e)}")


def get_by_id(table: str, id: int) -> Optional[Dict[str, Any]]:
    """
    Get a record by ID from a table
    """
    query = f"SELECT * FROM {table} WHERE id = ?"
    results = execute_query(query, (id,))
    return results[0] if results else None
