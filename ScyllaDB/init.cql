-- Removes the keyspace 'forum', allowing for all data to be wiped and reinstated after running this CQL file
DROP KEYSPACE IF EXISTS forum;

-- Create a new keyspace 'forum'
CREATE KEYSPACE IF NOT EXISTS forum
WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor': '3'
};

-- Use the new keyspace 'forum'
USE forum;

-- Ensure 'forum' has no tables (even though dropping keyspace wipes all objects)
DROP TABLE IF EXISTS entity_tables;
DROP TABLE IF EXISTS users;

-- Create master table 'entity_tables'
CREATE TABLE IF NOT EXISTS entity_tables (
    entity_name     VARCHAR ,
    unique_id       UUID    ,
    forum_id        INT     ,
    thread_id       INT     ,
    post_id         INT     ,
    forum_topic     VARCHAR ,
    forum_creator   VARCHAR ,
    thread_topic    VARCHAR ,
    thread_creator  VARCHAR ,
    thread_time     VARCHAR ,
    thread_created  VARCHAR ,
    thread_epoch    INT     ,
    post_creator    VARCHAR ,
    post_text       VARCHAR ,
    post_time       VARCHAR ,
    PRIMARY KEY (unique_id)
);

-- Create 'users' table
CREATE TABLE IF NOT EXISTS users (
    username        VARCHAR ,
    password        VARCHAR ,
    PRIMARY KEY (username)
);

-- Drop index 'entities' if exists
DROP INDEX IF EXISTS entities;

-- Create index 'entities' to be able to query on entity_name as secondary index
CREATE INDEX IF NOT EXISTS entities ON entity_tables (entity_name);

-- Insert 'forum' data
INSERT INTO entity_tables (entity_name, unique_id, forum_id, forum_topic, forum_creator) VALUES
    ('forums', uuid(), 1, 'HTMl', 'Alexander Truong');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, forum_topic, forum_creator) VALUES
    ('forums', uuid(), 2, 'CSS', 'Brian Truong');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, forum_topic, forum_creator) VALUES
    ('forums', uuid(), 3, 'PHP', 'Vivian Tran');

-- Insert 'thread' data
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, thread_topic, thread_creator, thread_time, thread_created, thread_epoch) VALUES
    ('threads', uuid(), 1, 1, 'How does one make an HTML file?', 'MrQuestions', 'Sat, 15 Sep 2018 15:52:28 PST', 'Sat, 15 Sep 2018 15:42:28 PST', 3);
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, thread_topic, thread_creator, thread_time, thread_created, thread_epoch) VALUES
    ('threads', uuid(), 1, 2, 'What IDE do you use?', 'DunceyMcDunce', 'Sat, 15 Sep 2018 16:32:10 PST', 'Sat, 15 Sep 2018 17:55:28 PST', 4);
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, thread_topic, thread_creator, thread_time, thread_created, thread_epoch) VALUES
    ('threads', uuid(), 1, 3, 'someone please help', 'FranticPerson', 'Sat, 15 Sep 2018 18:43:28 PST', 'Sat, 15 Sep 2018 17:11:11 PST', 6);
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, thread_topic, thread_creator, thread_time, thread_created, thread_epoch) VALUES
    ('threads', uuid(), 2, 1, 'What does CSS stand for?', 'MrCSSPro', 'Sat, 15 Sep 2018 15:42:28 PST', 'Sat, 15 Sep 2018 13:25:59 PST', 1);
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, thread_topic, thread_creator, thread_time, thread_created, thread_epoch) VALUES
    ('threads', uuid(), 2, 2, 'why use a .css file?', 'ImTheSmartest', 'Sat, 15 Sep 2018 16:42:28 PST', 'Sat, 15 Sep 2018 14:42:28 PST', 5);
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, thread_topic, thread_creator, thread_time, thread_created, thread_epoch) VALUES
    ('threads', uuid(), 3, 1, 'Is PHP better than SQL?', 'MissAwesome', 'Sat, 15 Sep 2018 15:44:28 PST', 'Sat, 15 Sep 2018 15:42:28 PST', 2);
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, thread_topic, thread_creator, thread_time, thread_created, thread_epoch) VALUES
    ('threads', uuid(), 3, 2, 'php sux', 'PHPHater', 'Sat, 15 Sep 2018 19:42:28 PST', 'Sat, 15 Sep 2018 17:42:28 PST', 7);

-- Insert 'post' data for forums '1'
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 1, 1, 1, 'MrQuestions', 'I am trying to start my own webpage and would like some pointers.', 'Sat, 15 Sep 2018 15:42:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 1, 1, 2, 'MrAnswers', 'Create a new file with a .html extension, eg: on Ubuntu, in terminal, type touch <filename>.html', 'Sat, 15 Sep 2018 15:50:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 1, 1, 3, 'MrQuestions', 'Thank you!', 'Sat, 15 Sep 2018 15:52:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 1, 2, 1, 'DunceyMcDunce', 'Just curious on what everyone uses', 'Sat, 15 Sep 2018 16:32:10 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 1, 2, 2, 'AnotherDuncey', 'just use a text editor', 'Sat, 15 Sep 2018 16:55:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 1, 2, 3, 'DunceyMcDunce', 'like notepad++?', 'Sat, 15 Sep 2018 17:42:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 1, 2, 4, 'AnotherDuncey', 'yes', 'Sat, 15 Sep 2018 17:55:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 1, 3, 1, 'FranticPerson', 'i dont know how to make a link', 'Sat, 15 Sep 2018 17:11:11 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 1, 3, 2, 'NonfranticLady', 'Did you check the HTML documentation?', 'Sat, 15 Sep 2018 18:42:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 1, 3, 3, 'FranticPerson', 'nevermind i figured it out lol', 'Sat, 15 Sep 2018 18:43:28 PST');

-- Insert 'post' data for forums '2'
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 2, 1, 1, 'MrCSSPro', 'Learning HTML and wanted to know what CSS stood for', 'Sat, 15 Sep 2018 13:25:59 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 2, 1, 2, 'NonProCSSGuy', 'Cascading Style Sheets. Are you sure you''re a pro?', 'Sat, 15 Sep 2018 14:42:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 2, 1, 3, 'MrCSSPro', '... maybe', 'Sat, 15 Sep 2018 15:42:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 2, 2, 1, 'ImTheSmartest', 'can''t you just style in your HTML file?', 'Sat, 15 Sep 2018 14:42:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 2, 2, 2, 'NotTheSmartest', 'It provides an easier way to style your HTML than in HTML itself', 'Sat, 15 Sep 2018 15:42:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 2, 2, 3, 'ImTheSmartest', 'I see. Thanks!', 'Sat, 15 Sep 2018 16:42:28 PST');

-- Insert 'post' data for forums '3'
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 3, 1, 1, 'MissAwesome', 'Never learned SQL and thinking about switching, but would like more info', 'Sat, 15 Sep 2018 15:42:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 3, 1, 2, 'PHPHater', 'of course sql is so much better', 'Sat, 15 Sep 2018 15:43:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 3, 1, 3, 'MissAwesome', 'I think your name shows you''re biased', 'Sat, 15 Sep 2018 15:44:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 3, 2, 1, 'PHPHater', 'it is so terrible', 'Sat, 15 Sep 2018 17:42:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 3, 2, 2, 'DunceyMcDunce', 'that''s not very constructive', 'Sat, 15 Sep 2018 18:42:28 PST');
INSERT INTO entity_tables (entity_name, unique_id, forum_id, thread_id, post_id, post_creator, post_text, post_time) VALUES
    ('posts', uuid(), 3, 2, 3, 'PHPHater', 'neither are you LUL', 'Sat, 15 Sep 2018 19:42:28 PST');

-- Insert data into 'users' table
INSERT INTO users (username, password) VALUES
  ('Alexander Truong', '12345');
INSERT INTO users (username, password) VALUES
  ('Brian Truong', '23456');
INSERT INTO users (username, password) VALUES
  ('Vivian Tran', '34567');
INSERT INTO users (username, password) VALUES
  ('MrQuestions', '123');
INSERT INTO users (username, password) VALUES
  ('DunceyMcDunce', '123');
INSERT INTO users (username, password) VALUES
  ('FranticPerson', '123');
INSERT INTO users (username, password) VALUES
  ('MrCSSPro', '123');
INSERT INTO users (username, password) VALUES
  ('ImTheSmartest', '123');
INSERT INTO users (username, password) VALUES
  ('MissAwesome', '123');
INSERT INTO users (username, password) VALUES
  ('PHPHater', '123');
INSERT INTO users (username, password) VALUES
  ('MrAnswers', '123');
INSERT INTO users (username, password) VALUES
  ('AnotherDuncey', '123');
INSERT INTO users (username, password) VALUES
  ('NonfranticLady', '123');
INSERT INTO users (username, password) VALUES
  ('NonProCSSGuy', '123');
INSERT INTO users (username, password) VALUES
  ('NotTheSmartest', '123');
