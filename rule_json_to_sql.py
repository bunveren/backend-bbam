import json

# change this path
INPUT_FILE = "D:\\VSCode-Projects\\frontend-bbam\\src\\utils\\rules.json"
OUTPUT_FILE = "insert_exercises.sql"


def escape_sql_string(s):
    return s.replace("'", "''")


def format_json_for_sql(obj):
    json_str = json.dumps(obj, indent=2)
    return escape_sql_string(json_str)


def generate_sql(data):
    sql_parts = []
    sql_parts.append("BEGIN;\n")

    for exercise_name, content in data.items():
        description = content.get("description", "")
        description_sql = escape_sql_string(description)

        rules_json_sql = format_json_for_sql(content)

        section_title = exercise_name.upper().replace("-", " ")

        block = f"""
-- =====================================
-- {section_title}
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = '{description_sql}',
        gif_url = ''
    WHERE name = '{exercise_name}'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT '{exercise_name}', '{description_sql}', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{rules_json_sql}'::jsonb, TRUE
FROM exercises WHERE name = '{exercise_name}'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;
"""
        sql_parts.append(block)

    sql_parts.append("\nCOMMIT;")
    return "\n".join(sql_parts)


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    sql_script = generate_sql(data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(sql_script)

    print(f"SQL script generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()