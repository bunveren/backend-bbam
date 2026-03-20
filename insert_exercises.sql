BEGIN;

DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = 'Lower your hips as if sitting back into a chair, keeping your chest up and back straight.', 
        gif_url = '' 
    WHERE name = 'Squat';
    
    UPDATE exercise_rules 
    SET rules_json = '{
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
}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = 'Squat');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = 'Squat') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('Squat', 'Lower your hips as if sitting back into a chair, keeping your chest up and back straight.', '') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{
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
}'::jsonb, TRUE);
    END IF;
END $$;

DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = 'Lower your body until your chest nearly touches the floor, keeping your elbows tucked and body straight.', 
        gif_url = '' 
    WHERE name = 'Push-up';
    
    UPDATE exercise_rules 
    SET rules_json = '{
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
}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = 'Push-up');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = 'Push-up') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('Push-up', 'Lower your body until your chest nearly touches the floor, keeping your elbows tucked and body straight.', '') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{
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
}'::jsonb, TRUE);
    END IF;
END $$;

DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = 'Maintain a push-up position with your body in a straight line to build core stability.', 
        gif_url = '' 
    WHERE name = 'Plank';
    
    UPDATE exercise_rules 
    SET rules_json = '{
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
}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = 'Plank');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = 'Plank') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('Plank', 'Maintain a push-up position with your body in a straight line to build core stability.', '') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{
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
}'::jsonb, TRUE);
    END IF;
END $$;

DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = 'Curl the weight toward your shoulder while keeping your upper arm stationary.', 
        gif_url = '' 
    WHERE name = 'Bicep-Curl';
    
    UPDATE exercise_rules 
    SET rules_json = '{
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
}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = 'Bicep-Curl');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = 'Bicep-Curl') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('Bicep-Curl', 'Curl the weight toward your shoulder while keeping your upper arm stationary.', '') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{
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
}'::jsonb, TRUE);
    END IF;
END $$;

DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = 'Step forward and lower your hips until both knees are bent at a 90-degree angle, keeping your torso upright and front knee behind toes.', 
        gif_url = '' 
    WHERE name = 'Lunge';
    
    UPDATE exercise_rules 
    SET rules_json = '{
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
}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = 'Lunge');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = 'Lunge') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('Lunge', 'Step forward and lower your hips until both knees are bent at a 90-degree angle, keeping your torso upright and front knee behind toes.', '') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{
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
}'::jsonb, TRUE);
    END IF;
END $$;

DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = 'Jump while spreading your legs and clapping your hands overhead, then return to starting position.', 
        gif_url = '' 
    WHERE name = 'Jumping-Jack';
    
    UPDATE exercise_rules 
    SET rules_json = '{
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
}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = 'Jumping-Jack');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = 'Jumping-Jack') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('Jumping-Jack', 'Jump while spreading your legs and clapping your hands overhead, then return to starting position.', '') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{
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
}'::jsonb, TRUE);
    END IF;
END $$;

DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = 'Push the weights directly overhead until your arms are fully extended, then lower them back to shoulder level while keeping your core engaged.', 
        gif_url = '' 
    WHERE name = 'Shoulder-Press';
    
    UPDATE exercise_rules 
    SET rules_json = '{
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
}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = 'Shoulder-Press');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = 'Shoulder-Press') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('Shoulder-Press', 'Push the weights directly overhead until your arms are fully extended, then lower them back to shoulder level while keeping your core engaged.', '') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{
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
}'::jsonb, TRUE);
    END IF;
END $$;

DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = 'Lie on your back and lift your hips toward the ceiling by squeezing your glutes.', 
        gif_url = '' 
    WHERE name = 'Glute-Bridge';
    
    UPDATE exercise_rules 
    SET rules_json = '{
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
}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = 'Glute-Bridge');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = 'Glute-Bridge') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('Glute-Bridge', 'Lie on your back and lift your hips toward the ceiling by squeezing your glutes.', '') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{
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
}'::jsonb, TRUE);
    END IF;
END $$;

DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = 'Lift arms out to the sides until they are level with shoulders.', 
        gif_url = '' 
    WHERE name = 'Lateral-Raise';
    
    UPDATE exercise_rules 
    SET rules_json = '{
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
}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = 'Lateral-Raise');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = 'Lateral-Raise') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('Lateral-Raise', 'Lift arms out to the sides until they are level with shoulders.', '') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{
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
}'::jsonb, TRUE);
    END IF;
END $$;

DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = 'Maintain a sided straight line to build core stability.', 
        gif_url = '' 
    WHERE name = 'Side-Plank';
    
    UPDATE exercise_rules 
    SET rules_json = '{
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
}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = 'Side-Plank');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = 'Side-Plank') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('Side-Plank', 'Maintain a sided straight line to build core stability.', '') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{
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
}'::jsonb, TRUE);
    END IF;
END $$;

DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = 'Lie on your back with knees bent, then lift your torso toward your knees while keeping your core engaged.', 
        gif_url = '' 
    WHERE name = 'Sit-up';
    
    UPDATE exercise_rules 
    SET rules_json = '{
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
}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = 'Sit-up');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = 'Sit-up') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('Sit-up', 'Lie on your back with knees bent, then lift your torso toward your knees while keeping your core engaged.', '') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{
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
}'::jsonb, TRUE);
    END IF;
END $$;

DO $$
DECLARE
    ex_id integer;
BEGIN
    UPDATE exercises 
    SET description = 'From a plank position, alternate bringing your knees toward your chest as if running in place.', 
        gif_url = '' 
    WHERE name = 'Mountain Climber';
    
    UPDATE exercise_rules 
    SET rules_json = '{
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
}'::jsonb 
    WHERE exercise_id IN (SELECT id FROM exercises WHERE name = 'Mountain Climber');

    IF NOT EXISTS (SELECT 1 FROM exercises WHERE name = 'Mountain Climber') THEN
        INSERT INTO exercises (name, description, gif_url) 
        VALUES ('Mountain Climber', 'From a plank position, alternate bringing your knees toward your chest as if running in place.', '') 
        RETURNING id INTO ex_id;
        
        INSERT INTO exercise_rules (exercise_id, rules_json, is_active) 
        VALUES (ex_id, '{
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
}'::jsonb, TRUE);
    END IF;
END $$;

COMMIT;