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