CREATE TABLE IF NOT EXISTS Forums (
  forum_id        INTEGER NOT NULL  ,
  name            TEXT    ,
  creator         TEXT    ,
  PRIMARY KEY (forum_id)  ,
  FOREIGN KEY (creator) REFERENCES Users(username)
);

CREATE TABLE IF NOT EXISTS Threads (
  forum_id        INTEGER ,
  thread_id       INTEGER ,
  title           TEXT    ,
  thread_text     TEXT    ,
  creator         TEXT    ,
  thread_time     TEXT    ,
  created_time    TEXT    ,
  unix_time       REAL    ,
  PRIMARY KEY (thread_id) ,
  FOREIGN KEY (creator) REFERENCES Users(username)  ,
  FOREIGN KEY (forum_id) REFERENCES Forums(forum_id)
);

CREATE TABLE IF NOT EXISTS Posts (
  forum_id        INTEGER ,
  thread_id       INTEGER ,
  post_num        INTEGER ,
  author          TEXT    ,
  text_post       TEXT    ,
  post_time       TEXT    ,
  PRIMARY KEY (post_num)  ,
  FOREIGN KEY (author) REFERENCES Users(username)     ,
  FOREIGN KEY (forum_id) REFERENCES Forums(forum_id)  ,
  FOREIGN KEY (thread_id) REFERENCES Threads(thread_id)
);

CREATE TABLE IF NOT EXISTS Users (
  username        TEXT COLLATE NOCASE   ,
  password        TEXT    ,
  PRIMARY KEY (username)
);

CREATE UNIQUE INDEX Forums_List ON Forums (name);
CREATE INDEX Threads_List ON Threads (title);
CREATE INDEX Posts_List ON Posts (text_post);
CREATE UNIQUE INDEX Usernames ON Users (username);

INSERT INTO Users (username, password)
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

INSERT INTO Forums (forum_id, name, creator)
VALUES
  (1, 'HTML', 'Alexander Truong'),
  (2, 'CSS', 'Brian Truong'),
  (3, 'PHP', 'Vivian Tran');

INSERT INTO Threads (forum_id, thread_id, title, thread_text, creator, created_time, thread_time, unix_time)
VALUES
  (1, 1, 'How does one make an HTML file?', 'Do we just use a text file or what?', 'MrQuestions', 'Sat, 15 Sep 2018 15:42:28 PST', 'Sat, 15 Sep 2018 15:52:28 PST', 10000),
  (1, 2, 'What IDE do you use?', 'Just curious on what everyone uses', 'DunceyMcDunce', 'Sat, 15 Sep 2018 16:32:10 PST', 'Sat, 15 Sep 2018 17:55:28 PST', 10001),
  (1, 3, 'someone please help', 'i dont know how to make a link', 'FranticPerson', 'Sat, 15 Sep 2018 17:11:11 PST', 'Sat, 15 Sep 2018 18:43:28 PST', 10002),
  (2, 4, 'What does CSS stand for?', 'Learning HTML and wanted to know what CSS stood for', 'MrCSSPro', 'Sat, 15 Sep 2018 13:25:59 PST', 'Sat, 15 Sep 2018 15:42:28 PST', 10003),
  (2, 5, 'why use a .css file?', 'can''t you just style in your HTML file?', 'ImTheSmartest', 'Sat, 15 Sep 2018 14:42:28 PST', 'Sat, 15 Sep 2018 16:42:28 PST', 10004),
  (3, 6, 'Is PHP better than SQL?', 'Never learned SQL and thinking about switching, but would like more info', 'MissAwesome', 'Sat, 15 Sep 2018 15:42:28 PST', 'Sat, 15 Sep 2018 15:44:28 PST', 10005),
  (3, 7, 'php sux', 'it is so terrible', 'PHPHater', 'Sat, 15 Sep 2018 17:42:28 PST', 'Sat, 15 Sep 2018 19:42:28 PST', 10006);

INSERT INTO Posts (forum_id, thread_id, post_num, author, text_post, post_time)
VALUES
  (1, 1, 1, 'MrAnswers', 'For linux, just run the command ''touch filename.html''', 'Sat, 15 Sep 2018 15:50:28 PST'),
  (1, 1, 2, 'MrQuestions', 'k thnx', 'Sat, 15 Sep 2018 15:52:28 PST'),
  (1, 2, 3, 'AnotherDuncey', 'just use a text editor lol', 'Sat, 15 Sep 2018 16:55:28 PST'),
  (1, 2, 4, 'DunceyMcDunce', 'like notepad++?', 'Sat, 15 Sep 2018 17:42:28 PST'),
  (1, 2, 5, 'AnotherDuncey', 'yes', 'Sat, 15 Sep 2018 17:55:28 PST'),
  (1, 3, 6, 'NonfranticLady', 'Did you check the HTML documentation?', 'Sat, 15 Sep 2018 18:42:28 PST'),
  (1, 3, 7, 'FranticPerson', 'nevermind i ifugred it out lol', 'Sat, 15 Sep 2018 18:43:28 PST'),
  (2, 4, 8, 'NonProCSSGuy', 'Cascading Style Sheets. Are you sure you''re a pro?', 'Sat, 15 Sep 2018 14:42:28 PST'),
  (2, 4, 9, 'MrCSSPro', '... maybe', 'Sat, 15 Sep 2018 15:42:28 PST'),
  (2, 5, 10, 'NotTheSmartest', 'It provides an easier way to style your HTML than in HTML itself', 'Sat, 15 Sep 2018 15:42:28 PST'),
  (2, 5, 11, 'ImTheSmartest', 'I see. Thanks!', 'Sat, 15 Sep 2018 16:42:28 PST'),
  (3, 6, 12, 'PHPHater', 'of course sql is so much better', 'Sat, 15 Sep 2018 15:43:28 PST'),
  (3, 6, 13, 'MissAwesome', 'I think your name shows you''re biased', 'Sat, 15 Sep 2018 15:44:28 PST'),
  (3, 7, 14, 'DunceyMcDunce', 'that''s not very constructive', 'Sat, 15 Sep 2018 18:42:28 PST'),
  (3, 7, 15, 'PHPHater', 'neither are you LUL', 'Sat, 15 Sep 2018 19:42:28 PST');
