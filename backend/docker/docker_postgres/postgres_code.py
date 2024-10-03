import psycopg2
from psycopg2 import sql
import json
import hashlib
from typing import Dict, Any, Optional, Tuple

# Define connection parameters
connection_params = {
    'dbname': 'cv_database',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'localhost',  # or '127.0.0.1'
    'port': 5432
}

def connect_to_db(params: Dict[str, Any]) -> psycopg2.extensions.connection:
    """
    Connects to the PostgreSQL database using the provided parameters.

    Args:
        params (Dict[str, Any]): A dictionary of connection parameters (dbname, user, password, host, port).

    Returns:
        psycopg2.extensions.connection: Connection object if successful, None otherwise.
    """
    try:
        conn = psycopg2.connect(**params)
        print("Connection successful")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
        
def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


# Create a table with specified columns
def create_resume_jd_table(conn):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS resume_jd_match (
        record_id SERIAL PRIMARY KEY,
        resume_text TEXT NOT NULL,
        jd_text TEXT NOT NULL,
        resume_text_hash VARCHAR(64) NOT NULL,
        jd_text_hash VARCHAR(64) NOT NULL,
        record_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        match_score_json JSON NOT NULL,
        resume_info_json JSON NOT NULL,
        jd_info_json JSON NOT NULL
    );
    '''
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_query)
            conn.commit()
            print("Table created successfully")
    except Exception as e:
        print(f"Error creating table: {e}")
        conn.rollback()


def record_exists(
    conn: psycopg2.extensions.connection, 
    resume_text: str, 
    jd_text: str
) -> Optional[Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]]:
    """
    Checks if a record with the same combination of resume_text_hash and jd_text_hash exists in the table.
    If exists, retrieves match_score_json, resume_info_json, and jd_info_json.

    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        resume_hash (str): Hash of the resume text.
        jd_hash (str): Hash of the job description text.

    Returns:
        Optional[Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]]: Tuple containing match_score_json, resume_info_json,
        and jd_info_json if the record exists, otherwise None.
    """
    select_query = '''
    SELECT match_score_json, resume_info_json, jd_info_json 
    FROM resume_jd_match 
    WHERE resume_text_hash = %s AND jd_text_hash = %s;
    '''

    print(select_query)
    # Hash the resume and JD texts
    resume_hash = hash_text(resume_text)
    jd_hash = hash_text(jd_text)

    try:
        with conn.cursor() as cursor:
            cursor.execute(select_query, (resume_hash, jd_hash))
            result = cursor.fetchone()
            if result:
                match_score_json, resume_info_json, jd_info_json = result
                return (
                    json.loads(match_score_json), 
                    json.loads(resume_info_json), 
                    json.loads(jd_info_json)
                )
            return None
    except Exception as e:
        print(f"Error checking for existing record: {e}")
        return None
    
def print_all_records(conn: psycopg2.extensions.connection) -> None:
    query = "SELECT * FROM resume_jd_match;"
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            print(result)
    except Exception as e:
        print(f"Error checking for existing records: {e}")

def insert_record(
    conn: psycopg2.extensions.connection, 
    resume_text: str, 
    jd_text: str, 
    match_score: Dict[str, Any], 
    resume_info: Dict[str, Any], 
    jd_info: Dict[str, Any]
) -> Optional[Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]]:
    """
    Inserts a new record into the 'resume_jd_match' table if it doesn't already exist.
    If the record exists, returns the existing match_score_json, resume_info_json, and jd_info_json.

    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        resume_text (str): Text of the resume.
        jd_text (str): Text of the job description.
        match_score (Dict[str, Any]): JSON object with the match score details.
        resume_info (Dict[str, Any]): JSON object with details about the resume (skills, experience, etc.).
        jd_info (Dict[str, Any]): JSON object with details about the job description.

    Returns:
        Optional[Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]]: Tuple containing match_score_json, resume_info_json,
        and jd_info_json if the record already exists, otherwise None.
    """
    # Hash the resume and JD texts
    resume_hash = hash_text(resume_text)
    jd_hash = hash_text(jd_text)

    # Insert the record
    insert_query = '''
    INSERT INTO resume_jd_match (resume_text, jd_text, resume_text_hash, jd_text_hash, match_score_json, resume_info_json, jd_info_json)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    '''
    try:
        with conn.cursor() as cursor:
            # Convert match_score, resume_info, and jd_info to JSON format
            match_score_json = json.dumps(match_score)
            resume_info_json = json.dumps(resume_info)
            jd_info_json = json.dumps(jd_info)
            
            # Execute the insert query
            cursor.execute(insert_query, (resume_text, jd_text, resume_hash, jd_hash, match_score_json, resume_info_json, jd_info_json))
            conn.commit()
            print("Record inserted successfully")
    except Exception as e:
        print(f"Error inserting record: {e}")
        conn.rollback()
    
    return None


def delete_record(conn: psycopg2.extensions.connection, record_id: int) -> None:
    """
    Deletes a record from the 'resume_jd_match' table by its record_id.

    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        record_id (int): The ID of the record to delete.

    Returns:
        None
    """
    delete_query = '''
    DELETE FROM resume_jd_match WHERE record_id = %s;
    '''
    try:
        with conn.cursor() as cursor:
            cursor.execute(delete_query, (record_id,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Record with ID {record_id} deleted successfully")
            else:
                print(f"No record found with ID {record_id}")
    except Exception as e:
        print(f"Error deleting record: {e}")
        conn.rollback()

# Main function
if __name__ == '__main__':
    # Connect to the PostgreSQL database
    conn = connect_to_db(connection_params)
    
    if conn:
        # create table if not exists
        create_resume_jd_table(conn)
         # Example data to insert
        resume_text = "John Doe is a software engineer with expertise in Python, AI, and ML."
        jd_text = "Looking for a software engineer with skills in Python and machine learning."

        match_score = {"score": 0.85, "confidence": 0.90}
        resume_info = {"name": "John Doe", "skills": ["Python", "AI", "ML"], "experience": "5 years"}
        jd_info = {"job_title": "Software Engineer", "skills_required": ["Python", "ML"]}

        # Insert the record into the database
        insert_record(conn, resume_text, jd_text, match_score, resume_info, jd_info)

        # Delete a record by record_id (uncomment to test deletion)
        # record_id_to_delete = 1  # Change this ID to the one you want to delete
        # delete_record(conn, record_id_to_delete)

        # Close the connection
        conn.close()
