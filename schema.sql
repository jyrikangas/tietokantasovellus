CREATE TABLE quizs (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE quiz (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizs,
    qnumber INTEGER,
    question TEXT,
    answer TEXT,
    wronganswer_1 TEXT,
    wronganswer_2 TEXT,
    wronganswer_3 TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);

CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizs,
    user_id INTEGER REFERENCES users,
    rights INTEGER,
    wrongs INTEGER
);

CREATE TABLE resultsStorage (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizs,
    user_id INTEGER REFERENCES users,
    rights INTEGER,
    wrongs INTEGER,
    correctPercent INTEGER
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizs,
    user_id INTEGER REFERENCES users,
    comment TEXT
);