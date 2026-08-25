-- ============================================================
-- schema.sql — Bug & Test Case Tracker
-- ============================================================

DROP TABLE IF EXISTS bugs;
DROP TABLE IF EXISTS test_cases;

CREATE TABLE test_cases (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    title               TEXT NOT NULL,
    preconditions       TEXT,
    steps               TEXT NOT NULL,
    expected_result     TEXT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'not_run',   -- not_run, passed, failed
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bugs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    title               TEXT NOT NULL,
    description         TEXT,
    severity            TEXT NOT NULL DEFAULT 'medium',    -- low, medium, high, critical
    status              TEXT NOT NULL DEFAULT 'open',       -- open, in_progress, resolved, closed
    steps_to_reproduce  TEXT,
    environment         TEXT,
    test_case_id        INTEGER REFERENCES test_cases(id),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
