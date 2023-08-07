# 샘플 유저를 만드는 SQL 구문

아이디:  user1
비밀번호: pwd1

INSERT INTO user (id, _id, pwd_hash, name, gender, birthdate, phone, mail, rq_terms, op_terms, sign_date)
VALUES ('778913ae-0c2e-44eb-993e-394b1380c5cb', 'user1', 'pbkdf2:sha256:600000$5JGg6LfZf0iHCC3L$d6571f5621461d69e60ca827e2d5b0bada624bbbb2d2978286e4682686e307ee', '정재영', 'Male', '1998-05-29 00:00:00', '01050926683', 'hanol98@naver.com', 1, 1, '2023-07-03 00:00:01')

-------------------------------------------------------------------------------------------
-유저 삭제

DELETE FROM user 
Where _id = 'user1'