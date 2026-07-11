import sqlite3
import os
from typing import List
from app.schemas import UniversityDetail

# Default database path (relative to the project root)
# Resolves to project_root/assets/yok_atlas.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "assets", "yok_atlas.db")

def get_universities_by_code(department_code: str, db_path: str = DB_PATH) -> List[UniversityDetail]:
    """
    Queries the SQLite database for universities offering a department matching the given department_code.
    Returns a list of UniversityDetail objects sorted by last_min_rank ASC.
    
    If the database file does not exist, or a query error occurs (e.g. table not found),
    returns an empty list [] to ensure graceful degradation.
    """
    if not os.path.exists(db_path):
        print(f"[Warning] Database file not found at: {db_path}")
        return []

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Query to fetch university details matching the department code
        # Sorted by last_min_rank ASC (best rank first)
        query = """
            SELECT university_name, quota, last_min_score, last_min_rank
            FROM yok_atlas_data
            WHERE department_code = ?
            ORDER BY last_min_rank ASC
        """
        cursor.execute(query, (department_code,))
        rows = cursor.fetchall()

        universities = []
        for row in rows:
            universities.append(
                UniversityDetail(
                    university_name=row["university_name"],
                    quota=row["quota"],
                    last_min_score=row["last_min_score"],
                    last_min_rank=row["last_min_rank"]
                )
            )
        conn.close()
        return universities

    except Exception as e:
        print(f"[SQL Error] Failed to retrieve data for department code '{department_code}': {e}")
        return []
