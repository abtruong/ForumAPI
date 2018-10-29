ATTACH DATABASE 'maindb.db' AS 'maindb';
ATTACH DATABASE 'shard_1.db' AS 'posts1';
ATTACH DATABASE 'shard_2.db' AS 'posts2';
ATTACH DATABASE 'shard_0.db' AS 'posts0';

CREATE TABLE IF NOT EXISTS maindb.Forums (
  forum_id        INTEGER NOT NULL  ,
  name            TEXT    ,
  creator         TEXT    ,
  PRIMARY KEY (forum_id)  ,
  FOREIGN KEY (creator) REFERENCES Users(username)
);

CREATE TABLE IF NOT EXISTS maindb.Threads (
  forum_id        INTEGER ,
  thread_num      INTEGER ,
  thread_id       TEXT    ,
  title           TEXT    ,
  thread_text     TEXT    ,
  creator         TEXT    ,
  thread_time     TEXT    ,
  created_time    TEXT    ,
  unix_time       REAL    ,
  PRIMARY KEY (thread_id, thread_num),
  FOREIGN KEY (creator) REFERENCES Users(username)  ,
  FOREIGN KEY (forum_id) REFERENCES Forums(forum_id)
);

CREATE TABLE IF NOT EXISTS maindb.Users (
  username        TEXT COLLATE NOCASE   ,
  password        TEXT    ,
  PRIMARY KEY (username)
);

CREATE TABLE IF NOT EXISTS posts1.Posts (
  shard_key       TEXT    ,
  author          TEXT    ,
  text_post       TEXT    ,
  post_time       TEXT    
);

CREATE TABLE IF NOT EXISTS posts2.Posts (
  shard_key       TEXT    ,
  author          TEXT    ,
  text_post       TEXT    ,
  post_time       TEXT    
);

CREATE TABLE IF NOT EXISTS posts0.Posts (
  shard_key       TEXT    ,
  author          TEXT    ,
  text_post       TEXT    ,
  post_time       TEXT    
);

INSERT INTO maindb.Users (username, password)
VALUES
  ('Alexander Truong', '12345'),
  ('Brian Truong', '23456'),
  ('Vivian Tran', '34567'),
  ('MrQuestions', '123'),
  ('DunceyMcDunce', '123'),
  ('FranticPerson', '123'),
  ('MrCSSPro', '123'),
  ('ImTheSmartest', '123'),
  ('MissAwesome', '123'),
  ('PHPHater', '123'),
  ('MrAnswers', '123'),
  ('AnotherDuncey', '123'),
  ('NonfranticLady', '123'),
  ('NonProCSSGuy', '123'),
  ('NotTheSmartest', '123');

INSERT INTO maindb.Forums (forum_id, name, creator)
VALUES
  (1, 'HTML', 'Alexander Truong'),
  (2, 'CSS', 'Brian Truong'),
  (3, 'PHP', 'Vivian Tran');

INSERT INTO maindb.Threads (forum_id, thread_num, thread_id, title, thread_text, creator, created_time, thread_time, unix_time)
VALUES
  (1, 1, '589a82c2-e373-4b96-a44c-5d6cc39a28d8', 'How does one make an HTML file?', 'Do we just use a text file or what?', 'MrQuestions', 'Sat, 15 Sep 2018 15:42:28 PST', 'Sat, 15 Sep 2018 15:52:28 PST', 10000),
  (1, 2, 'fb1628d7-f2c6-4c66-a2ac-89b8220128fb', 'What IDE do you use?', 'Just curious on what everyone uses', 'DunceyMcDunce', 'Sat, 15 Sep 2018 16:32:10 PST', 'Sat, 15 Sep 2018 17:55:28 PST', 10001),
  (1, 3, 'cf206aed-f0a7-4b88-9704-1ea4366aa54e', 'someone please help', 'i dont know how to make a link', 'FranticPerson', 'Sat, 15 Sep 2018 17:11:11 PST', 'Sat, 15 Sep 2018 18:43:28 PST', 10002),
  (2, 4, '41e30f10-5d72-45ca-b531-c6177339b476', 'What does CSS stand for?', 'Learning HTML and wanted to know what CSS stood for', 'MrCSSPro', 'Sat, 15 Sep 2018 13:25:59 PST', 'Sat, 15 Sep 2018 15:42:28 PST', 10003),
  (2, 5, 'bdacef59-df26-4b9b-8779-333fa53a7f95', 'why use a .css file?', 'can''t you just style in your HTML file?', 'ImTheSmartest', 'Sat, 15 Sep 2018 14:42:28 PST', 'Sat, 15 Sep 2018 16:42:28 PST', 10004),
  (3, 6, '02089b32-6b1e-4193-ad58-1c491ea0079f', 'Is PHP better than SQL?', 'Never learned SQL and thinking about switching, but would like more info', 'MissAwesome', 'Sat, 15 Sep 2018 15:42:28 PST', 'Sat, 15 Sep 2018 15:44:28 PST', 10005),
  (3, 7, '07f603c8-11fa-4a1e-8cba-beb7edfdc03f', 'php sux', 'it is so terrible', 'PHPHater', 'Sat, 15 Sep 2018 17:42:28 PST', 'Sat, 15 Sep 2018 19:42:28 PST', 10006);

INSERT INTO posts1.Posts (shard_key, author, text_post, post_time)
VALUES
  ('589a82c2-e373-4b96-a44c-5d6cc39a28d8', 'MrAnswers', 'For linux, just run the command ''touch filename.html''', 'Sat, 15 Sep 2018 15:50:28 PST'),
  ('589a82c2-e373-4b96-a44c-5d6cc39a28d8', 'MrQuestions', 'k thnx', 'Sat, 15 Sep 2018 15:52:28 PST'),
  ('41e30f10-5d72-45ca-b531-c6177339b476', 'NonProCSSGuy', 'Cascading Style Sheets. Are you sure you''re a pro?', 'Sat, 15 Sep 2018 14:42:28 PST'),
  ('41e30f10-5d72-45ca-b531-c6177339b476', 'MrCSSPro', '... maybe', 'Sat, 15 Sep 2018 15:42:28 PST'),
  ('07f603c8-11fa-4a1e-8cba-beb7edfdc03f', 'DunceyMcDunce', 'that''s not very constructive', 'Sat, 15 Sep 2018 18:42:28 PST'),
  ('07f603c8-11fa-4a1e-8cba-beb7edfdc03f', 'PHPHater', 'neither are you LUL', 'Sat, 15 Sep 2018 19:42:28 PST');

INSERT INTO posts2.Posts (shard_key, author, text_post, post_time)
VALUES
  ('fb1628d7-f2c6-4c66-a2ac-89b8220128fb', 'AnotherDuncey', 'just use a text editor lol', 'Sat, 15 Sep 2018 16:55:28 PST'),
  ('fb1628d7-f2c6-4c66-a2ac-89b8220128fb', 'DunceyMcDunce', 'like notepad++?', 'Sat, 15 Sep 2018 17:42:28 PST'),
  ('fb1628d7-f2c6-4c66-a2ac-89b8220128fb', 'AnotherDuncey', 'yes', 'Sat, 15 Sep 2018 17:55:28 PST'),
  ('bdacef59-df26-4b9b-8779-333fa53a7f95', 'NotTheSmartest', 'It provides an easier way to style your HTML than in HTML itself', 'Sat, 15 Sep 2018 15:42:28 PST'),
  ('bdacef59-df26-4b9b-8779-333fa53a7f95', 'ImTheSmartest', 'I see. Thanks!', 'Sat, 15 Sep 2018 16:42:28 PST');

INSERT INTO posts0.Posts (shard_key, author, text_post, post_time)
VALUES
  ('cf206aed-f0a7-4b88-9704-1ea4366aa54e', 'NonfranticLady', 'Did you check the HTML documentation?', 'Sat, 15 Sep 2018 18:42:28 PST'),
  ('cf206aed-f0a7-4b88-9704-1ea4366aa54e', 'FranticPerson', 'nevermind i figured it out lol', 'Sat, 15 Sep 2018 18:43:28 PST'),
  ('02089b32-6b1e-4193-ad58-1c491ea0079f', 'PHPHater', 'of course sql is so much better', 'Sat, 15 Sep 2018 15:43:28 PST'),
  ('02089b32-6b1e-4193-ad58-1c491ea0079f', 'MissAwesome', 'I think your name shows you''re biased', 'Sat, 15 Sep 2018 15:44:28 PST');
