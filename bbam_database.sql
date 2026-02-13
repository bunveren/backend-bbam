
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_profiles (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    height_cm INTEGER,
    weight_kg INTEGER,
    age INTEGER,
    gender VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    gif_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workout_plans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_name VARCHAR(255) NOT NULL,
    deleted_at TIMESTAMP, -- Soft delete için (opsiyonel)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workout_plan_items (
    id SERIAL PRIMARY KEY,
    plan_id INTEGER NOT NULL REFERENCES workout_plans(id) ON DELETE CASCADE,
    step_order INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id) ON DELETE RESTRICT,
    target_reps INTEGER,
    target_seconds INTEGER,
    set_label INTEGER,
    CONSTRAINT unique_plan_step UNIQUE (plan_id, step_order)
);

CREATE TABLE workout_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_id INTEGER REFERENCES workout_plans(id) ON DELETE SET NULL,
    
    -- ÖNEMLİ: Plan silinse bile adı kalır
    plan_name VARCHAR(255),
    
    session_date DATE NOT NULL,
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    duration_minutes INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'planned' 
        CHECK (status IN ('planned', 'in_progress', 'completed', 'cancelled')),
    overall_accuracy_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE session_exercises (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES workout_sessions(id) ON DELETE CASCADE,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id) ON DELETE RESTRICT,
    step_order INTEGER NOT NULL,
    
    -- Hedef
    target_reps INTEGER,
    target_seconds INTEGER,
    
    -- Gerçekleşen 
    completed_reps INTEGER,
    completed_seconds INTEGER,
    accuracy_score DECIMAL(5,2),
    
    CONSTRAINT unique_session_step UNIQUE (session_id, step_order)
);

CREATE TABLE exercise_rules (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER NOT NULL UNIQUE REFERENCES exercises(id) ON DELETE CASCADE,
    rules_json JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE session_summaries (
    session_id INTEGER PRIMARY KEY REFERENCES workout_sessions(id) ON DELETE CASCADE,
    summary_json JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workout_reminders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_id INTEGER REFERENCES workout_plans(id) ON DELETE CASCADE,
    reminder_time TIME NOT NULL,
    recurrence VARCHAR(20) NOT NULL DEFAULT 'once',
    recurrence_days JSONB,
    message TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE user_devices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    -- Frontend tarafından üretilen rastgele UUID (f47ac10b-58cc-...)
    -- Bu ID, AsyncStorage içinde saklanan ID'dir.
    device_uuid VARCHAR(255) NOT NULL,
    expo_token VARCHAR(255) NOT NULL,
    os_type VARCHAR(50) CHECK (os_type IN ('ios', 'android')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_device UNIQUE (user_id, device_uuid)
);
CREATE INDEX idx_user_devices_user_id ON user_devices(user_id);
CREATE INDEX idx_user_devices_device_id ON user_devices(device_uuid);
CREATE INDEX idx_user_devices_token ON user_devices(expo_token);


-- Users
CREATE INDEX idx_users_email ON users(email);

-- Workout Plans
CREATE INDEX idx_workout_plans_user ON workout_plans(user_id);
CREATE INDEX idx_workout_plans_deleted ON workout_plans(deleted_at); -- Soft delete için

-- Plan Items
CREATE INDEX idx_plan_items_plan_order ON workout_plan_items(plan_id, step_order);

-- Sessions 
CREATE INDEX idx_sessions_user_date ON workout_sessions(user_id, session_date DESC);
CREATE INDEX idx_sessions_status ON workout_sessions(status);
CREATE INDEX idx_sessions_plan ON workout_sessions(plan_id);

-- Session Exercises
CREATE INDEX idx_session_exercises_order ON session_exercises(session_id, step_order);
CREATE INDEX idx_session_exercises_exercise ON session_exercises(exercise_id);

-- Exercise Rules
CREATE INDEX idx_exercise_rules_exercise ON exercise_rules(exercise_id);
CREATE INDEX idx_exercise_rules_active ON exercise_rules(is_active);

-- Session Summary 
CREATE INDEX idx_summary_json ON session_summaries USING GIN (summary_json);

-- Reminders
CREATE INDEX idx_reminders_user_active ON workout_reminders(user_id, is_active);


-- Session duration otomatik hesaplama
CREATE OR REPLACE FUNCTION calculate_session_duration()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.ended_at IS NOT NULL AND NEW.started_at IS NOT NULL THEN
        NEW.duration_minutes := EXTRACT(EPOCH FROM (NEW.ended_at - NEW.started_at)) / 60;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_session_duration
BEFORE INSERT OR UPDATE ON workout_sessions
FOR EACH ROW
WHEN (NEW.ended_at IS NOT NULL)
EXECUTE FUNCTION calculate_session_duration();

-- Plan adını session'a kopyala (plan silinirse adı kalır)
CREATE OR REPLACE FUNCTION copy_plan_name_to_session()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.plan_id IS NOT NULL THEN
        SELECT plan_name INTO NEW.plan_name
        FROM workout_plans
        WHERE id = NEW.plan_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_copy_plan_name
BEFORE INSERT ON workout_sessions
FOR EACH ROW
WHEN (NEW.plan_id IS NOT NULL)
EXECUTE FUNCTION copy_plan_name_to_session();
