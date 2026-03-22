BEGIN;


-- =====================================
-- SQUAT
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = 'Lower your hips as if sitting back into a chair, keeping your chest up and back straight.',
        gif_url = ''
    WHERE name = 'Squat'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT 'Squat', 'Lower your hips as if sitting back into a chair, keeping your chest up and back straight.', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{
  "mode": "reps",
  "description": "Lower your hips as if sitting back into a chair, keeping your chest up and back straight.",
  "repConfig": {
    "primaryJoints": [
      24,
      26,
      28
    ],
    "startThreshold": 160,
    "midThreshold": 90,
    "type": "descending"
  },
  "rules": [
    {
      "id": "S-01",
      "name": "Knee Angle",
      "minAngle": 60,
      "maxAngle": 90,
      "joints": [
        24,
        26,
        28
      ],
      "errorCondition": "angle < 60 || angle > 90",
      "message": "Squat depth is off! Stay between 60-90 degrees."
    },
    {
      "id": "S-02",
      "name": "Torso Angle",
      "minAngle": 150,
      "maxAngle": 180,
      "joints": [
        12,
        24,
        26
      ],
      "errorCondition": "angle < 150",
      "message": "Keep your chest up! Don''t lean forward."
    }
  ]
}'::jsonb, TRUE
FROM exercises WHERE name = 'Squat'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;


-- =====================================
-- PUSH UP
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = 'Lower your body until your chest nearly touches the floor, keeping your elbows tucked and body straight.',
        gif_url = ''
    WHERE name = 'Push-up'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT 'Push-up', 'Lower your body until your chest nearly touches the floor, keeping your elbows tucked and body straight.', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{
  "mode": "reps",
  "description": "Lower your body until your chest nearly touches the floor, keeping your elbows tucked and body straight.",
  "repConfig": {
    "primaryJoints": [
      11,
      13,
      15
    ],
    "startThreshold": 160,
    "midThreshold": 70,
    "type": "descending"
  },
  "rules": [
    {
      "id": "P-01",
      "name": "Body Line Angle",
      "joints": [
        12,
        24,
        28
      ],
      "minAngle": 170,
      "maxAngle": 180,
      "errorCondition": "angle < 170",
      "message": "Straighten your body! Don''t let your hips sag."
    },
    {
      "id": "P-02",
      "name": "Elbow Angle",
      "minAngle": 60,
      "maxAngle": 90,
      "joints": [
        12,
        14,
        16
      ],
      "errorCondition": "angle < 60 || angle > 90",
      "message": "Adjust your depth! Elbows should be 60-90 degrees."
    }
  ]
}'::jsonb, TRUE
FROM exercises WHERE name = 'Push-up'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;


-- =====================================
-- PLANK
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = 'Maintain a push-up position with your body in a straight line to build core stability.',
        gif_url = ''
    WHERE name = 'Plank'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT 'Plank', 'Maintain a push-up position with your body in a straight line to build core stability.', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{
  "mode": "hold",
  "description": "Maintain a push-up position with your body in a straight line to build core stability.",
  "holdConfig": {
    "primaryJoints": [
      12,
      24,
      28
    ]
  },
  "rules": [
    {
      "id": "PL-01",
      "name": "Core Stability",
      "joints": [
        12,
        24,
        28
      ],
      "minAngle": 170,
      "maxAngle": 185,
      "errorCondition": "angle < 170",
      "message": "Lower your hips! Your body should be a straight line."
    }
  ]
}'::jsonb, TRUE
FROM exercises WHERE name = 'Plank'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;


-- =====================================
-- BICEP CURL
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = 'Curl the weight toward your shoulder while keeping your upper arm stationary.',
        gif_url = ''
    WHERE name = 'Bicep-Curl'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT 'Bicep-Curl', 'Curl the weight toward your shoulder while keeping your upper arm stationary.', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{
  "mode": "reps",
  "description": "Curl the weight toward your shoulder while keeping your upper arm stationary.",
  "repConfig": {
    "primaryJoints": [
      12,
      14,
      16
    ],
    "startThreshold": 160,
    "midThreshold": 40,
    "type": "descending"
  },
  "rules": [
    {
      "id": "BC-01",
      "name": "Full Extension",
      "joints": [
        12,
        14,
        16
      ],
      "minAngle": 30,
      "maxAngle": 160,
      "errorCondition": "angle > 160",
      "message": "Don''t lock your elbows! Maintain muscle tension."
    },
    {
      "id": "BC-02",
      "name": "Contraction",
      "joints": [
        12,
        14,
        16
      ],
      "minAngle": 30,
      "maxAngle": 160,
      "errorCondition": "angle < 30",
      "message": "Don''t over-flex! Maintain controlled movement."
    }
  ]
}'::jsonb, TRUE
FROM exercises WHERE name = 'Bicep-Curl'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;


-- =====================================
-- LUNGE
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = 'Step forward and lower your hips until both knees are bent at a 90-degree angle, keeping your torso upright and front knee behind toes.',
        gif_url = ''
    WHERE name = 'Lunge'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT 'Lunge', 'Step forward and lower your hips until both knees are bent at a 90-degree angle, keeping your torso upright and front knee behind toes.', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{
  "mode": "reps",
  "description": "Step forward and lower your hips until both knees are bent at a 90-degree angle, keeping your torso upright and front knee behind toes.",
  "repConfig": {
    "primaryJoints": [
      24,
      26,
      28
    ],
    "startThreshold": 170,
    "midThreshold": 100,
    "type": "descending"
  },
  "rules": [
    {
      "id": "L-01",
      "name": "Front Knee Angle",
      "minAngle": 80,
      "maxAngle": 100,
      "joints": [
        24,
        26,
        28
      ],
      "errorCondition": "angle < 80",
      "message": "Front knee is too far forward! Keep it around 90 degrees."
    },
    {
      "id": "L-02",
      "name": "Torso Upright",
      "minAngle": 160,
      "maxAngle": 180,
      "joints": [
        12,
        24,
        26
      ],
      "errorCondition": "angle < 160",
      "message": "Keep your torso upright! You are leaning too far forward."
    }
  ]
}'::jsonb, TRUE
FROM exercises WHERE name = 'Lunge'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;


-- =====================================
-- JUMPING JACK
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = 'Jump while spreading your legs and clapping your hands overhead, then return to starting position.',
        gif_url = ''
    WHERE name = 'Jumping-Jack'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT 'Jumping-Jack', 'Jump while spreading your legs and clapping your hands overhead, then return to starting position.', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{
  "mode": "reps",
  "description": "Jump while spreading your legs and clapping your hands overhead, then return to starting position.",
  "repConfig": {
    "primaryJoints": [
      11,
      0,
      12
    ],
    "startThreshold": 60,
    "midThreshold": 150,
    "type": "ascending"
  },
  "rules": [
    {
      "id": "JJ-01",
      "name": "Arm Width",
      "joints": [
        11,
        0,
        12
      ],
      "minAngle": 60,
      "maxAngle": 180,
      "errorCondition": "angle < 60",
      "message": "Clap your hands at the top! Bring your arms higher."
    }
  ]
}'::jsonb, TRUE
FROM exercises WHERE name = 'Jumping-Jack'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;


-- =====================================
-- SHOULDER PRESS
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = 'Push the weights directly overhead until your arms are fully extended, then lower them back to shoulder level while keeping your core engaged.',
        gif_url = ''
    WHERE name = 'Shoulder-Press'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT 'Shoulder-Press', 'Push the weights directly overhead until your arms are fully extended, then lower them back to shoulder level while keeping your core engaged.', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{
  "mode": "reps",
  "description": "Push the weights directly overhead until your arms are fully extended, then lower them back to shoulder level while keeping your core engaged.",
  "repConfig": {
    "primaryJoints": [
      12,
      14,
      16
    ],
    "startThreshold": 80,
    "midThreshold": 160,
    "type": "ascending"
  },
  "rules": [
    {
      "id": "SP-01",
      "name": "Elbow Flare",
      "joints": [
        12,
        14,
        16
      ],
      "minAngle": 70,
      "maxAngle": 180,
      "errorCondition": "angle < 70",
      "message": "Don''t drop your elbows too low! Keep them at 90 degrees or slightly above."
    }
  ]
}'::jsonb, TRUE
FROM exercises WHERE name = 'Shoulder-Press'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;


-- =====================================
-- GLUTE BRIDGE
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = 'Lie on your back and lift your hips toward the ceiling by squeezing your glutes.',
        gif_url = ''
    WHERE name = 'Glute-Bridge'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT 'Glute-Bridge', 'Lie on your back and lift your hips toward the ceiling by squeezing your glutes.', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{
  "mode": "reps",
  "description": "Lie on your back and lift your hips toward the ceiling by squeezing your glutes.",
  "repConfig": {
    "primaryJoints": [
      12,
      24,
      26
    ],
    "startThreshold": 110,
    "midThreshold": 160,
    "type": "ascending"
  },
  "rules": [
    {
      "id": "GB-01",
      "name": "Hip Extension",
      "joints": [
        12,
        24,
        26
      ],
      "minAngle": 160,
      "maxAngle": 190,
      "errorCondition": "angle < 160",
      "message": "Squeeze your glutes! Push your hips higher toward the ceiling."
    }
  ]
}'::jsonb, TRUE
FROM exercises WHERE name = 'Glute-Bridge'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;


-- =====================================
-- LATERAL RAISE
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = 'Lift arms out to the sides until they are level with shoulders.',
        gif_url = ''
    WHERE name = 'Lateral-Raise'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT 'Lateral-Raise', 'Lift arms out to the sides until they are level with shoulders.', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{
  "mode": "reps",
  "description": "Lift arms out to the sides until they are level with shoulders.",
  "repConfig": {
    "primaryJoints": [
      14,
      12,
      24
    ],
    "startThreshold": 20,
    "midThreshold": 85,
    "type": "ascending"
  },
  "rules": [
    {
      "id": "LR-01",
      "name": "Arm Height",
      "joints": [
        14,
        12,
        24
      ],
      "minAngle": 0,
      "maxAngle": 100,
      "message": "Don''t lift too high! Stop at shoulder level."
    }
  ]
}'::jsonb, TRUE
FROM exercises WHERE name = 'Lateral-Raise'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;


-- =====================================
-- SIDE PLANK
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = 'Maintain a sided straight line to build core stability.',
        gif_url = ''
    WHERE name = 'Side-Plank'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT 'Side-Plank', 'Maintain a sided straight line to build core stability.', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{
  "mode": "hold",
  "description": "Maintain a sided straight line to build core stability.",
  "holdConfig": {
    "primaryJoints": [
      12,
      24,
      28
    ]
  },
  "rules": [
    {
      "id": "SPL-01",
      "name": "Hip Alignment",
      "joints": [
        12,
        24,
        28
      ],
      "minAngle": 170,
      "maxAngle": 190,
      "message": "Keep your hips high! Your body should be a straight diagonal."
    }
  ]
}'::jsonb, TRUE
FROM exercises WHERE name = 'Side-Plank'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;


-- =====================================
-- SIT UP
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = 'Lie on your back with knees bent, then lift your torso toward your knees while keeping your core engaged.',
        gif_url = ''
    WHERE name = 'Sit-up'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT 'Sit-up', 'Lie on your back with knees bent, then lift your torso toward your knees while keeping your core engaged.', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{
  "mode": "reps",
  "description": "Lie on your back with knees bent, then lift your torso toward your knees while keeping your core engaged.",
  "repConfig": {
    "primaryJoints": [
      12,
      24,
      26
    ],
    "startThreshold": 150,
    "midThreshold": 45,
    "type": "descending"
  },
  "rules": [
    {
      "id": "SU-01",
      "name": "Torso Range",
      "joints": [
        12,
        24,
        26
      ],
      "minAngle": 40,
      "maxAngle": 160,
      "errorCondition": "angle < 40",
      "message": "Don''t over-flex! Keep the movement controlled."
    }
  ]
}'::jsonb, TRUE
FROM exercises WHERE name = 'Sit-up'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;


-- =====================================
-- MOUNTAIN CLIMBER
-- =====================================
WITH upsert AS (
    UPDATE exercises
    SET description = 'From a plank position, alternate bringing your knees toward your chest as if running in place.',
        gif_url = ''
    WHERE name = 'Mountain Climber'
    RETURNING id
)
INSERT INTO exercises (name, description, gif_url)
SELECT 'Mountain Climber', 'From a plank position, alternate bringing your knees toward your chest as if running in place.', ''
WHERE NOT EXISTS (SELECT 1 FROM upsert);

INSERT INTO exercise_rules (exercise_id, rules_json, is_active)
SELECT id, '{
  "mode": "reps",
  "description": "From a plank position, alternate bringing your knees toward your chest as if running in place.",
  "repConfig": {
    "primaryJoints": [
      24,
      26,
      28
    ],
    "startThreshold": 160,
    "midThreshold": 80,
    "type": "descending"
  },
  "rules": [
    {
      "id": "MC-01",
      "name": "Knee Drive",
      "joints": [
        24,
        26,
        28
      ],
      "minAngle": 70,
      "maxAngle": 100,
      "message": "Bring your knee closer to your chest for a full rep!"
    }
  ]
}'::jsonb, TRUE
FROM exercises WHERE name = 'Mountain Climber'
ON CONFLICT (exercise_id)
DO UPDATE SET 
    rules_json = EXCLUDED.rules_json,
    is_active = TRUE;


COMMIT;