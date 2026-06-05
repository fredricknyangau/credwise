"""
Raw SQL for quizzes.
"""

GET_QUIZ_BY_MODULE = """
SELECT id, module_id, title, created_at
FROM quizzes
WHERE module_id = $1;
"""

GET_QUIZ_BY_ID = """
SELECT id, module_id, title, created_at
FROM quizzes
WHERE id = $1;
"""

INSERT_QUIZ = """
INSERT INTO quizzes (id, module_id, title)
VALUES ($1, $2, $3)
RETURNING id, module_id, title, created_at;
"""

GET_QUESTIONS_BY_QUIZ = """
SELECT id, quiz_id, question, options, correct_answer, created_at
FROM quiz_questions
WHERE quiz_id = $1
ORDER BY created_at ASC;
"""

INSERT_QUESTION = """
INSERT INTO quiz_questions (id, quiz_id, question, options, correct_answer)
VALUES ($1, $2, $3, $4::jsonb, $5)
RETURNING id, quiz_id, question, options, correct_answer, created_at;
"""

INSERT_QUIZ_ATTEMPT = """
INSERT INTO quiz_attempts (id, user_id, quiz_id, score, answers, completed_at)
VALUES ($1, $2, $3, $4, $5::jsonb, NOW())
RETURNING id, user_id, quiz_id, score, completed_at;
"""

GET_ATTEMPTS_BY_USER_QUIZ = """
SELECT id, user_id, quiz_id, score, completed_at
FROM quiz_attempts
WHERE user_id = $1 AND quiz_id = $2
ORDER BY completed_at DESC;
"""

GET_BEST_SCORE_FOR_USER_QUIZ = """
SELECT MAX(score) AS best_score
FROM quiz_attempts
WHERE user_id = $1 AND quiz_id = $2;
"""
