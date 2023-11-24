import sqlite3

def init_db(db_path='quiz_game.db'):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL to create tables
    create_topics_table = """
    CREATE TABLE IF NOT EXISTS Topics (
        topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_name TEXT NOT NULL
    );
    """

    create_questions_table = """
    CREATE TABLE IF NOT EXISTS Questions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INTEGER,
        question_text TEXT NOT NULL,
        FOREIGN KEY (topic_id) REFERENCES Topics(topic_id)
    );
    """

    create_answers_table = """
    CREATE TABLE IF NOT EXISTS Answers (
        answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        answer_text TEXT NOT NULL,
        is_correct BOOLEAN NOT NULL CHECK (is_correct IN (0, 1)),
        FOREIGN KEY (question_id) REFERENCES Questions(question_id)
    );
    """

    # Execute the queries to create tables
    cursor.execute(create_topics_table)
    cursor.execute(create_questions_table)
    cursor.execute(create_answers_table)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# This allows the script to be imported without executing the init_db function automatically
if __name__ == '__main__':
    init_db()
