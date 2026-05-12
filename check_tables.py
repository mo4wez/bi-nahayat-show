# check_schema.py
import sqlite3

DATABASE_PATH = 'db.sqlite3'

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

tables = ['courses_step', 'courses_level', 'courses_question', 
          'courses_userprogress', 'courses_userprogress_completed_questions']

for table in tables:
    print(f"\n{'='*60}")
    print(f"📋 Table: {table}")
    print('='*60)
    
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    
    for col in columns:
        col_id, name, col_type, not_null, default, pk = col
        pk_mark = " [PK]" if pk else ""
        null_mark = " NOT NULL" if not_null else ""
        print(f"  {name:25} {col_type:15}{pk_mark}{null_mark}")
    
    # نمایش foreign keys
    cursor.execute(f"PRAGMA foreign_key_list({table})")
    fks = cursor.fetchall()
    if fks:
        print("\n  🔗 Foreign Keys:")
        for fk in fks:
            print(f"    {fk[3]} -> {fk[2]}.{fk[4]}")

conn.close()
