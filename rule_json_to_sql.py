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
    if isinstance(data, dict):
        items_to_process = data.items()
    else:
        items_to_process = [(item.get('name', 'Adsız'), item) for item in data]

    for name_key, details in items_to_process:
        name = escape_sql(name_key)
        description = escape_sql(details.get('description', ''))
        gif_url = escape_sql(details.get('gif_url', ''))
        
        rules_dict = details.get('rules', {})
        rules_json_str = json.dumps(rules_dict, ensure_ascii=False)
        rules_json_escaped = escape_sql(rules_json_str)

        stmt = f"""
WITH inserted_exercise AS (
    INSERT INTO exercises (name, description, gif_url)
    VALUES ('{name}', '{description}', '{gif_url}')
    RETURNING id
)
INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{rules_json_escaped}'::jsonb, TRUE FROM inserted_exercise;
"""
        sql_statements.append(stmt)

    sql_statements.append("\nCOMMIT;")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(sql_statements)

if __name__ == "__main__":
    generate_sql("C:\\frontend-bbam\\src\\utils\\rules.json")