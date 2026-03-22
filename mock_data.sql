
BEGIN;

-- 0) Clean slate 
TRUNCATE TABLE
  workout_reminders,
  session_summaries,
  session_exercises,
  workout_sessions,
  workout_plan_items,
  workout_plans,
  exercise_rules,
  exercises,
  user_profiles,
  users
RESTART IDENTITY CASCADE;

-- USERS 
INSERT INTO users (email, password_hash) VALUES
('melis.sezer@demo.com',   '$2b$12$demo_hash_melis'),
('beren.unveren@demo.com', '$2b$12$demo_hash_beren'),
('betul.saglam@demo.com',  '$2b$12$demo_hash_betul'),
('aylin.sahin@demo.com',   '$2b$12$demo_hash_aylin');

-- USER PROFILES
INSERT INTO user_profiles (user_id, height_cm, weight_kg, age, gender) VALUES
(1, 168, 58, 22, 'female'),
(2, 172, 62, 22, 'female'),
(3, 165, 55, 22, 'female'),
(4, 170, 60, 22, 'female');

-- EXERCISES
INSERT INTO exercises (name, description, gif_url) VALUES
('Squat', 'Bodyweight squat focusing on hip hinge and knee tracking.', 'https://cdn.example.com/gifs/squat.gif'),
('Push-up', 'Upper body strength; keep body in a straight line.', 'https://cdn.example.com/gifs/pushup.gif'),
('Plank', 'Core endurance; neutral spine, tight glutes.', 'https://cdn.example.com/gifs/plank.gif'),
('Lunge', 'Single-leg strength; avoid knee valgus.', 'https://cdn.example.com/gifs/lunge.gif'),
('Glute-Bridge', 'Posterior chain activation; squeeze glutes at top.', 'https://cdn.example.com/gifs/glute_bridge.gif'),
('Jumping-Jack', 'Cardio warm-up; controlled pace.', 'https://cdn.example.com/gifs/jumping_jack.gif'),
('Mountain Climber', 'Core + cardio; keep hips stable.', 'https://cdn.example.com/gifs/mountain_climber.gif'),
('Sit-up', 'Core; avoid pulling neck.', 'https://cdn.example.com/gifs/situp.gif');

-- EXERCISE RULES
INSERT INTO exercise_rules (exercise_id, rules_json, is_active) VALUES
(1, '{
  "rules": [
    {"id":"S-01","metric":"knee_angle","joints":["hip","knee","ankle"],"range":[60,95],"error_msg":"Go deeper while keeping knees aligned."},
    {"id":"S-02","metric":"knee_valgus","joints":["hip","knee","ankle"],"range":[0,10],"error_msg":"Do not let knees cave inward."}
  ]
}'::jsonb, TRUE),

(2, '{
  "rules": [
    {"id":"P-01","metric":"body_line_angle","joints":["shoulder","hip","ankle"],"range":[170,180],"error_msg":"Keep a straight line from shoulders to ankles."},
    {"id":"P-02","metric":"elbow_angle_bottom","joints":["shoulder","elbow","wrist"],"range":[70,100],"error_msg":"Lower until elbows reach ~90 degrees."}
  ]
}'::jsonb, TRUE),

(3, '{
  "rules": [
    {"id":"PL-01","metric":"hip_sag","joints":["shoulder","hip","ankle"],"range":[0,8],"error_msg":"Avoid sagging hips; tighten core and glutes."}
  ]
}'::jsonb, TRUE),

(4, '{
  "rules": [
    {"id":"L-01","metric":"front_knee_angle","joints":["hip","knee","ankle"],"range":[70,110],"error_msg":"Control depth; keep knee stacked over ankle."}
  ]
}'::jsonb, TRUE);

-- WORKOUT PLANS 
-- user1: 2 plans, user2: 1 plan, user3: 1 plan, user4: 1 plan
INSERT INTO workout_plans (user_id, plan_name, deleted_at) VALUES
(1, 'Full Body Beginner (A)', NULL),      -- plan_id = 1
(1, 'Core + Mobility (B)', NULL),         -- plan_id = 2
(2, 'Lower Body Strength', NULL),         -- plan_id = 3
(3, 'Cardio + Core', NULL),               -- plan_id = 4
(4, 'Upper + Core Starter', NULL);        -- plan_id = 5

-- WORKOUT PLAN ITEMS
-- Plan 1: Full Body Beginner (A)
INSERT INTO workout_plan_items (plan_id, step_order, exercise_id, target_reps, target_seconds, set_label) VALUES
(1, 1, 6, NULL, 60, 1),   -- Jumping Jack 60s warmup
(1, 2, 1, 12, NULL, 1),   -- Squat 12
(1, 3, 2, 10, NULL, 1),   -- Push-up 10
(1, 4, 4, 10, NULL, 1),   -- Lunge 10
(1, 5, 3, NULL, 30, 1);   -- Plank 30s

-- Plan 2: Core + Mobility (B)
INSERT INTO workout_plan_items (plan_id, step_order, exercise_id, target_reps, target_seconds, set_label) VALUES
(2, 1, 3, NULL, 40, 1),   -- Plank 40s
(2, 2, 7, 20, NULL, 1),   -- Mountain Climber 20
(2, 3, 8, 12, NULL, 1),   -- Sit-up 12
(2, 4, 5, 15, NULL, 1);   -- Glute Bridge 15

-- Plan 3: Lower Body Strength
INSERT INTO workout_plan_items (plan_id, step_order, exercise_id, target_reps, target_seconds, set_label) VALUES
(3, 1, 1, 15, NULL, 1),   -- Squat 15
(3, 2, 4, 12, NULL, 1),   -- Lunge 12
(3, 3, 5, 18, NULL, 1);   -- Glute Bridge 18

-- Plan 4: Cardio + Core
INSERT INTO workout_plan_items (plan_id, step_order, exercise_id, target_reps, target_seconds, set_label) VALUES
(4, 1, 6, NULL, 90, 1),   -- Jumping Jack 90s
(4, 2, 7, 25, NULL, 1),   -- Mountain Climber 25
(4, 3, 3, NULL, 45, 1);   -- Plank 45s

-- Plan 5: Upper + Core Starter 
INSERT INTO workout_plan_items (plan_id, step_order, exercise_id, target_reps, target_seconds, set_label) VALUES
(5, 1, 2, 8,  NULL, 1),   -- Push-up 8
(5, 2, 3, NULL, 30, 1),   -- Plank 30s
(5, 3, 8, 10, NULL, 1);   -- Sit-up 10

-- WORKOUT SESSIONS 
INSERT INTO workout_sessions
(user_id, plan_id, plan_name, session_date, started_at, ended_at, status, overall_accuracy_score)
VALUES
(1, 1, 'Full Body Beginner (A)', '2026-01-14', '2026-01-14 19:05:00', '2026-01-14 19:33:00', 'completed', 86.40), -- session_id=1
(1, 2, 'Core + Mobility (B)',    '2026-01-16', '2026-01-16 20:10:00', '2026-01-16 20:28:00', 'completed', 88.10), -- session_id=2
(2, 3, 'Lower Body Strength',    '2026-01-15', '2026-01-15 18:20:00', '2026-01-15 18:45:00', 'completed', 83.70), -- session_id=3
(3, 4, 'Cardio + Core',          '2026-01-17', '2026-01-17 21:00:00', '2026-01-17 21:26:00', 'completed', 81.20), -- session_id=4
(1, 1, 'Full Body Beginner (A)', '2026-01-19', '2026-01-19 19:00:00', NULL,                   'in_progress', NULL), -- session_id=5
(4, 5, 'Upper + Core Starter',   '2026-01-18', '2026-01-18 18:40:00', '2026-01-18 19:02:00', 'completed', 87.30); -- session_id=6

-- SESSION EXERCISES
-- Session 1 (plan1)
INSERT INTO session_exercises
(session_id, exercise_id, step_order, target_reps, target_seconds, completed_reps, completed_seconds, accuracy_score)
VALUES
(1, 6, 1, NULL, 60, NULL, 60, 92.00),
(1, 1, 2, 12, NULL, 12, NULL, 84.50),
(1, 2, 3, 10, NULL, 9,  NULL, 82.00),
(1, 4, 4, 10, NULL, 10, NULL, 80.00),
(1, 3, 5, NULL, 30, NULL, 28, 93.00);

-- Session 2 (plan2)
INSERT INTO session_exercises
(session_id, exercise_id, step_order, target_reps, target_seconds, completed_reps, completed_seconds, accuracy_score)
VALUES
(2, 3, 1, NULL, 40, NULL, 40, 90.00),
(2, 7, 2, 20, NULL, 20, NULL, 85.50),
(2, 8, 3, 12, NULL, 12, NULL, 86.00),
(2, 5, 4, 15, NULL, 15, NULL, 91.00);

-- Session 3 (plan3)
INSERT INTO session_exercises
(session_id, exercise_id, step_order, target_reps, target_seconds, completed_reps, completed_seconds, accuracy_score)
VALUES
(3, 1, 1, 15, NULL, 14, NULL, 82.00),
(3, 4, 2, 12, NULL, 12, NULL, 80.50),
(3, 5, 3, 18, NULL, 18, NULL, 88.00);

-- Session 4 (plan4)
INSERT INTO session_exercises
(session_id, exercise_id, step_order, target_reps, target_seconds, completed_reps, completed_seconds, accuracy_score)
VALUES
(4, 6, 1, NULL, 90, NULL, 90, 89.00),
(4, 7, 2, 25, NULL, 25, NULL, 78.00),
(4, 3, 3, NULL, 45, NULL, 41, 76.50);

-- Session 5 (plan1) in_progress (partial)
INSERT INTO session_exercises
(session_id, exercise_id, step_order, target_reps, target_seconds, completed_reps, completed_seconds, accuracy_score)
VALUES
(5, 6, 1, NULL, 60, NULL, 60, 91.00),
(5, 1, 2, 12, NULL, 12, NULL, 83.00);

-- Session 6 (plan5) 
INSERT INTO session_exercises
(session_id, exercise_id, step_order, target_reps, target_seconds, completed_reps, completed_seconds, accuracy_score)
VALUES
(6, 2, 1, 8,  NULL, 8,  NULL, 86.00),
(6, 3, 2, NULL, 30, NULL, 30, 90.00),
(6, 8, 3, 10, NULL, 10, NULL, 86.00);

-- SESSION SUMMARIES (completed sessions only: 1,2,3,4,6)
INSERT INTO session_summaries (session_id, summary_json) VALUES
(1, '{
  "overall_avg_score": 86.4,
  "total_completed_reps": 43,
  "total_time_seconds": 148,
  "by_exercise": [
    {"exercise_id":6,"exercise_name":"Jumping Jack","target_seconds":60,"completed_seconds":60,"avg_score":92.0,
     "top_errors":[{"code":"JJ-01","name":"pace_inconsistent","count":1}],
     "feedback_sentences":["Great warm-up pace. Keep it consistent."]},
    {"exercise_id":1,"exercise_name":"Squat","target_reps":12,"completed_reps":12,"avg_score":84.5,
     "top_errors":[{"code":"S-02","name":"knees_caving_in","count":2}],
     "feedback_sentences":["Keep knees aligned over toes."]},
    {"exercise_id":2,"exercise_name":"Push-up","target_reps":10,"completed_reps":9,"avg_score":82.0,
     "top_errors":[{"code":"P-01","name":"hip_sagging","count":3}],
     "feedback_sentences":["Maintain a straight body line; tighten your core."]},
    {"exercise_id":4,"exercise_name":"Lunge","target_reps":10,"completed_reps":10,"avg_score":80.0,
     "top_errors":[{"code":"L-01","name":"knee_forward","count":2}],
     "feedback_sentences":["Control your knee position; keep it stacked over ankle."]},
    {"exercise_id":3,"exercise_name":"Plank","target_seconds":30,"completed_seconds":28,"avg_score":93.0,
     "top_errors":[{"code":"PL-01","name":"hip_sag","count":1}],
     "feedback_sentences":["Great form—avoid letting hips drop near the end."]}
  ]
}'::jsonb),

(2, '{
  "overall_avg_score": 88.1,
  "total_completed_reps": 47,
  "total_time_seconds": 40,
  "by_exercise": [
    {"exercise_id":3,"exercise_name":"Plank","target_seconds":40,"completed_seconds":40,"avg_score":90.0,
     "top_errors":[{"code":"PL-01","name":"hip_sag","count":1}],
     "feedback_sentences":["Solid hold—keep glutes engaged."]},
    {"exercise_id":7,"exercise_name":"Mountain Climber","target_reps":20,"completed_reps":20,"avg_score":85.5,
     "top_errors":[{"code":"MC-01","name":"hips_rocking","count":2}],
     "feedback_sentences":["Try to keep hips stable while driving knees."]},
    {"exercise_id":8,"exercise_name":"Sit-up","target_reps":12,"completed_reps":12,"avg_score":86.0,
     "top_errors":[{"code":"SU-01","name":"neck_pull","count":1}],
     "feedback_sentences":["Avoid pulling your neck; use your core."]},
    {"exercise_id":5,"exercise_name":"Glute Bridge","target_reps":15,"completed_reps":15,"avg_score":91.0,
     "top_errors":[{"code":"GB-01","name":"low_hip_extension","count":1}],
     "feedback_sentences":["Squeeze glutes fully at the top."]}
  ]
}'::jsonb),

(3, '{
  "overall_avg_score": 83.7,
  "total_completed_reps": 44,
  "total_time_seconds": 0,
  "by_exercise": [
    {"exercise_id":1,"exercise_name":"Squat","target_reps":15,"completed_reps":14,"avg_score":82.0,
     "top_errors":[{"code":"S-01","name":"depth_insufficient","count":2}],
     "feedback_sentences":["Go a bit deeper while keeping balance."]},
    {"exercise_id":4,"exercise_name":"Lunge","target_reps":12,"completed_reps":12,"avg_score":80.5,
     "top_errors":[{"code":"L-01","name":"knee_forward","count":2}],
     "feedback_sentences":["Keep your front knee controlled."]},
    {"exercise_id":5,"exercise_name":"Glute Bridge","target_reps":18,"completed_reps":18,"avg_score":88.0,
     "top_errors":[{"code":"GB-01","name":"low_hip_extension","count":1}],
     "feedback_sentences":["Good bridges—aim full extension each rep."]}
  ]
}'::jsonb),

(4, '{
  "overall_avg_score": 81.2,
  "total_completed_reps": 25,
  "total_time_seconds": 176,
  "by_exercise": [
    {"exercise_id":6,"exercise_name":"Jumping Jack","target_seconds":90,"completed_seconds":90,"avg_score":89.0,
     "top_errors":[{"code":"JJ-01","name":"pace_inconsistent","count":2}],
     "feedback_sentences":["Keep steady rhythm for better cardio efficiency."]},
    {"exercise_id":7,"exercise_name":"Mountain Climber","target_reps":25,"completed_reps":25,"avg_score":78.0,
     "top_errors":[{"code":"MC-01","name":"hips_rocking","count":4}],
     "feedback_sentences":["Keep hips stable; slow down if needed."]},
    {"exercise_id":3,"exercise_name":"Plank","target_seconds":45,"completed_seconds":41,"avg_score":76.5,
     "top_errors":[{"code":"PL-01","name":"hip_sag","count":3}],
     "feedback_sentences":["Try shorter sets with perfect form, then build duration."]}
  ]
}'::jsonb),

(6, '{
  "overall_avg_score": 87.3,
  "total_completed_reps": 18,
  "total_time_seconds": 30,
  "by_exercise": [
    {"exercise_id":2,"exercise_name":"Push-up","target_reps":8,"completed_reps":8,"avg_score":86.0,
     "top_errors":[{"code":"P-01","name":"hip_sagging","count":1}],
     "feedback_sentences":["Good push-ups—keep core tight for perfect line."]},
    {"exercise_id":3,"exercise_name":"Plank","target_seconds":30,"completed_seconds":30,"avg_score":90.0,
     "top_errors":[{"code":"PL-01","name":"hip_sag","count":0}],
     "feedback_sentences":["Strong plank hold—nice neutral spine."]},
    {"exercise_id":8,"exercise_name":"Sit-up","target_reps":10,"completed_reps":10,"avg_score":86.0,
     "top_errors":[{"code":"SU-01","name":"neck_pull","count":1}],
     "feedback_sentences":["Keep chin slightly tucked; avoid pulling the neck."]}
  ]
}'::jsonb);

-- WORKOUT REMINDERS
INSERT INTO workout_reminders
(user_id, plan_id, reminder_time, recurrence, recurrence_days, message, is_active, created_at)
VALUES
(1, 1, '19:00', 'weekly', '["Mon","Wed","Fri"]'::jsonb, 'Time for Full Body Beginner (A)!', TRUE, NOW() - INTERVAL '7 days'),
(1, 2, '20:00', 'weekly', '["Tue","Thu"]'::jsonb, 'Core + Mobility (B) session reminder.', TRUE, NOW() - INTERVAL '7 days'),
(2, 3, '18:00', 'weekly', '["Mon","Thu"]'::jsonb, 'Lower Body Strength day!', TRUE, NOW() - INTERVAL '7 days'),
(3, 4, '21:00', 'weekly', '["Sat"]'::jsonb, 'Cardio + Core session today.', TRUE, NOW() - INTERVAL '7 days'),
(4, 5, '19:30', 'weekly', '["Sun","Wed"]'::jsonb, 'Upper + Core Starter reminder.', TRUE, NOW() - INTERVAL '7 days');

COMMIT;
