"""
-- ESKI EGZERSIZLER DBNIZDE VARSA BUNU SQL SCRIPTINDEN SONRA CALISTIRIN TEK SEFERLIK
BEGIN;


UPDATE workout_plan_items SET exercise_id = 9 WHERE exercise_id = 1;   -- Squat
UPDATE workout_plan_items SET exercise_id = 10 WHERE exercise_id = 2;  -- Push-up
UPDATE workout_plan_items SET exercise_id = 11 WHERE exercise_id = 3;  -- Plank
UPDATE workout_plan_items SET exercise_id = 13 WHERE exercise_id = 4;  -- Lunge
UPDATE workout_plan_items SET exercise_id = 16 WHERE exercise_id = 5;  -- Glute Bridge -> Glute-Bridge
UPDATE workout_plan_items SET exercise_id = 14 WHERE exercise_id = 6;  -- Jumping Jack -> Jumping-Jack

UPDATE session_exercises SET exercise_id = 9 WHERE exercise_id = 1;
UPDATE session_exercises SET exercise_id = 10 WHERE exercise_id = 2;
UPDATE session_exercises SET exercise_id = 11 WHERE exercise_id = 3;
UPDATE session_exercises SET exercise_id = 13 WHERE exercise_id = 4;
UPDATE session_exercises SET exercise_id = 16 WHERE exercise_id = 5;
UPDATE session_exercises SET exercise_id = 14 WHERE exercise_id = 6;

DELETE FROM exercises WHERE id IN (1, 2, 3, 4, 5, 6);

COMMIT;
"""
import json
import os

def escape_sql(text):
    if text is None: return "NULL"
    if not isinstance(text, str): return str(text)
    return text.replace("'", "''")

def generate_sql(json_path, output_path="insert_exercises.sql"):
    if not os.path.exists(json_path): return

    with open(json_path, 'r', encoding='utf-8') as f: data = json.load(f)
    sql_statements = ["BEGIN;\n"]
    items_to_process = data.items() if isinstance(data, dict) else [(item.get('name', 'noname'), item) for item in data]

    for name_key, details in items_to_process:
        name = escape_sql(name_key)
        description = escape_sql(details.get('description', 'No description provided.'))
        gif_url = escape_sql(details.get('gif_url', ''))
        formatted_json = json.dumps(details, indent=2, ensure_ascii=False)
        full_config_escaped = escape_sql(formatted_json)

        stmt = f"""
DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = '{description}', 
        gif_url = '{gif_url}' 
    WHERE name = '{name}';
    
    UPDATE exercise_rules 
    SET rules_json = '{full_config_escaped}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = '{name}');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = '{name}') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('{name}', '{description}', '{gif_url}') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{full_config_escaped}'::jsonb, TRUE);
    END IF;
END $$;
"""
        sql_statements.append(stmt)

    sql_statements.append("\nCOMMIT;")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(sql_statements)

if __name__ == "__main__":
    generate_sql("C:\\frontend-bbam\\src\\utils\\rules.json")