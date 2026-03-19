BEGIN;

WITH inserted_exercise AS (
    INSERT INTO exercises (name, description, gif_url)
    VALUES ('Squat', '', '')
    RETURNING id
)
INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '[{"id": "S-01", "name": "Knee Angle", "minAngle": 60, "maxAngle": 90, "joints": [24, 26, 28], "errorCondition": "angle < 60 || angle > 90", "message": "Squat depth is off! Stay between 60-90 degrees."}, {"id": "S-02", "name": "Torso Angle", "minAngle": 150, "maxAngle": 180, "joints": [12, 24, 26], "errorCondition": "angle < 150", "message": "Keep your chest up! Don''t lean forward."}]'::jsonb, TRUE FROM inserted_exercise;

WITH inserted_exercise AS (
    INSERT INTO exercises (name, description, gif_url)
    VALUES ('Push-up', '', '')
    RETURNING id
)
INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '[{"id": "P-01", "name": "Body Line Angle", "joints": [12, 24, 28], "minAngle": 170, "maxAngle": 180, "errorCondition": "angle < 170", "message": "Straighten your body! Don''t let your hips sag."}, {"id": "P-02", "name": "Elbow Angle", "minAngle": 60, "maxAngle": 90, "joints": [12, 14, 16], "errorCondition": "angle < 60 || angle > 90", "message": "Adjust your depth! Elbows should be 60-90 degrees."}]'::jsonb, TRUE FROM inserted_exercise;

WITH inserted_exercise AS (
    INSERT INTO exercises (name, description, gif_url)
    VALUES ('Plank', '', '')
    RETURNING id
)
INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '[{"id": "PL-01", "name": "Core Stability", "joints": [12, 24, 28], "minAngle": 170, "maxAngle": 185, "errorCondition": "angle < 170", "message": "Lower your hips! Your body should be a straight line."}]'::jsonb, TRUE FROM inserted_exercise;

WITH inserted_exercise AS (
    INSERT INTO exercises (name, description, gif_url)
    VALUES ('Bicep-Curl', '', '')
    RETURNING id
)
INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '[{"id": "BC-01", "name": "Full Extension", "joints": [12, 14, 16], "minAngle": 30, "maxAngle": 160, "errorCondition": "angle > 160", "message": "Don''t lock your elbows! Maintain muscle tension."}, {"id": "BC-02", "name": "Contraction", "joints": [12, 14, 16], "minAngle": 30, "maxAngle": 160, "errorCondition": "angle < 30", "message": "Don''t over-flex! Maintain controlled movement."}]'::jsonb, TRUE FROM inserted_exercise;

WITH inserted_exercise AS (
    INSERT INTO exercises (name, description, gif_url)
    VALUES ('Lunge', '', '')
    RETURNING id
)
INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '[{"id": "L-01", "name": "Front Knee Angle", "minAngle": 80, "maxAngle": 100, "joints": [24, 26, 28], "errorCondition": "angle < 80", "message": "Front knee is too far forward! Keep it around 90 degrees."}, {"id": "L-02", "name": "Torso Upright", "minAngle": 160, "maxAngle": 180, "joints": [12, 24, 26], "errorCondition": "angle < 160", "message": "Keep your torso upright! You are leaning too far forward."}]'::jsonb, TRUE FROM inserted_exercise;

WITH inserted_exercise AS (
    INSERT INTO exercises (name, description, gif_url)
    VALUES ('Jumping-Jack', '', '')
    RETURNING id
)
INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '[{"id": "JJ-01", "name": "Arm Width", "joints": [11, 0, 12], "minAngle": 60, "maxAngle": 180, "errorCondition": "angle < 60", "message": "Clap your hands at the top! Bring your arms higher."}]'::jsonb, TRUE FROM inserted_exercise;

WITH inserted_exercise AS (
    INSERT INTO exercises (name, description, gif_url)
    VALUES ('Shoulder-Press', '', '')
    RETURNING id
)
INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '[{"id": "SP-01", "name": "Elbow Flare", "joints": [12, 14, 16], "minAngle": 70, "maxAngle": 180, "errorCondition": "angle < 70", "message": "Don''t drop your elbows too low! Keep them at 90 degrees or slightly above."}]'::jsonb, TRUE FROM inserted_exercise;

WITH inserted_exercise AS (
    INSERT INTO exercises (name, description, gif_url)
    VALUES ('Glute-Bridge', '', '')
    RETURNING id
)
INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '[{"id": "GB-01", "name": "Hip Extension", "joints": [12, 24, 26], "minAngle": 160, "maxAngle": 190, "errorCondition": "angle < 160", "message": "Squeeze your glutes! Push your hips higher toward the ceiling."}]'::jsonb, TRUE FROM inserted_exercise;

COMMIT;