--
-- Create database
--

-- CREATE DATABASE IF NOT EXISTS game_of_thrones;
-- USE game_of_thrones;


--
-- Drop tables
-- turn off FK checks temporarily to eliminate drop order issues
--

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS culture, house, relation_type, character_info, episode, 
                     biological_type, character_family_tie, character_title, character_aliase;
SET FOREIGN_KEY_CHECKS=1;


--
-- cultures
--

CREATE TABLE IF NOT EXISTS culture
  (
    culture_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    culture_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (culture_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/jelly/Development/18fall_code/si664_code/final-proj/finalproj/scripts/output/character_culture.csv'
INTO TABLE culture
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    -- FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    -- LINES TERMINATED BY '\r\n'
    (culture_name);

--
-- houses
--

CREATE TABLE IF NOT EXISTS house
  (
    house_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    house_name VARCHAR(100) NOT NULL UNIQUE,
    house_img_file_name VARCHAR(100) UNIQUE,
    PRIMARY KEY (house_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/jelly/Development/18fall_code/si664_code/final-proj/finalproj/scripts/output/character_house.csv'
INTO TABLE house
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    -- FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    -- LINES TERMINATED BY '\r\n'
    (house_name);

--
-- Load houses icon image file name from external file.
-- create temporary table to store houses icon img file name.
--

CREATE TEMPORARY TABLE temp_house_icon
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    house_name VARCHAR(100) NOT NULL UNIQUE,
    icon_file_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/jelly/Development/18fall_code/si664_code/final-proj/finalproj/scripts/input/csv/house_icon_img_ref.csv'
INTO TABLE temp_house_icon
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    -- FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    -- LINES TERMINATED BY '\n'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (house_name, icon_file_name);

-- update house_img_file_name in house table
UPDATE house h
RIGHT JOIN temp_house_icon thi 
    ON thi.house_name = h.house_name
SET h.house_img_file_name = thi.icon_file_name;


--
-- create table for relation type between characters
--

CREATE TABLE relation_type
  (
    relation_type_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    relation_type_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (relation_type_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO relation_type (relation_type_name) VALUES
    ('father'), ('mother'), ('descendant'), ('spouse');



-- 
-- create table for episode, didn't use this table in the website
--

CREATE TABLE episode
    (
      episode_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
      episode_name VARCHAR(100) NOT NULL UNIQUE,
      season_num INTEGER NOT NULL,
      episode_num INTEGER NOT NULL,
      PRIMARY KEY (episode_id)
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/jelly/Development/18fall_code/si664_code/final-proj/finalproj/scripts/input/csv/overview.csv'
INTO TABLE episode
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    -- FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    -- LINES TERMINATED BY '\n'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (@dummy, season_num, episode_num, episode_name);


--
-- Load character img file name from external file. 
-- create temporary table for character img file name
--

CREATE TEMPORARY TABLE temp_character_img_ref
    (
        id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        character_name VARCHAR(100) NOT NULL UNIQUE,
        img_file_name VARCHAR(100) NOT NULL,
        PRIMARY KEY (id)
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/jelly/Development/18fall_code/si664_code/final-proj/finalproj/scripts/input/csv/character_img_url_ref.csv'
INTO TABLE temp_character_img_ref
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    -- LINES TERMINATED BY '\n'
    LINES TERMINATED BY '\r\n'
    (character_name, img_file_name);

--
-- Load the first file of character info from external file. 
-- create temporary table for character info
--

CREATE TEMPORARY TABLE temp_character_info
    (
        character_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        full_name VARCHAR(100) NOT NULL,
        is_main_character INT NOT NULL,
        brief_intro TEXT,
        full_intro TEXT NOT NULL,
        character_url VARCHAR(255) NOT NULL UNIQUE,
        PRIMARY KEY (character_id)

    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/jelly/Development/18fall_code/si664_code/final-proj/finalproj/scripts/input/csv/character_full.csv'
INTO TABLE temp_character_info
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    -- FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    -- LINES TERMINATED BY '\n'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (@dummy, @dummy, full_name, character_url, full_intro, brief_intro, is_main_character)

    SET brief_intro = IF(brief_intro = '', NULL, brief_intro);  

--
-- Load the second file of character info from external file. 
-- create temporary table for character more info
--


CREATE TEMPORARY TABLE temp_character_more_info
    (
        character_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        full_name VARCHAR(100) NOT NULL,
        culture_name VARCHAR(100) NOT NULL,
        house_name VARCHAR(100) NOT NULL,
        is_male INT NOT NUll,
        PRIMARY KEY (character_id)
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/jelly/Development/18fall_code/si664_code/final-proj/finalproj/scripts/input/csv/character_more_info.csv'
INTO TABLE temp_character_more_info
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    -- FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    -- LINES TERMINATED BY '\n'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (full_name, culture_name, house_name, is_male);
 

--
-- create table for character info
--

CREATE TABLE IF NOT EXISTS character_info
    (
        character_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        full_name VARCHAR(100) NOT NULL,
        is_male INT NOT NULL,
        is_main_character INT NOT NULL,
        brief_intro TEXT,
        full_intro TEXT NOT NULL,
        character_url VARCHAR(255),
        character_img_file_name VARCHAR(100) UNIQUE,
        house_id INTEGER,
        culture_id INTEGER,
        PRIMARY KEY (character_id),
        FOREIGN KEY (house_id) REFERENCES house(house_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (culture_id) REFERENCES culture(culture_id)
        ON DELETE CASCADE ON UPDATE CASCADE

    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

--
-- assemble character info data in table temp_character_info 
-- and temp_character_more_info together into character_info
-- 

INSERT IGNORE INTO character_info (full_name, is_male, is_main_character,
                                   brief_intro, full_intro, character_url, character_img_file_name,
                                   house_id, culture_id)
SELECT tci.full_name,
       tcmi.is_male,
       tci.is_main_character,
       tci.brief_intro,
       tci.full_intro,
       tci.character_url,
       tcir.img_file_name,
       h.house_id,
       c.culture_id
FROM temp_character_info tci
    LEFT JOIN temp_character_img_ref tcir
        ON tcir.character_name = tci.full_name
    LEFT JOIN temp_character_more_info tcmi
        ON tcmi.full_name = tci.full_name
    LEFT JOIN culture c
        ON tcmi.culture_name = c.culture_name
    LEFT JOIN house h
        ON tcmi.house_name = h.house_name
ORDER BY tci.character_id;


--
-- create table biological_type
--


CREATE TABLE IF NOT EXISTS biological_type
    (
        biological_type_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        biological_type_name VARCHAR(100) NOT NULL,
        PRIMARY KEY (biological_type_id)
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO biological_type (biological_type_name) VALUES
    ('adoptive'), ('biological'), ('legal');


--
-- create temporary table and load daata for character_family_tie
--


CREATE TEMPORARY TABLE temp_character_family_tie
    (
        id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        character1_name VARCHAR(100) NOT NULL,
        character2_name VARCHAR(100) NOT NULL,
        relation_name VARCHAR(100) NOT NULL,
        biological_type_name VARCHAR(100),
        PRIMARY KEY (id)
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE '/Users/jelly/Development/18fall_code/si664_code/final-proj/finalproj/scripts/input/csv/family_tie_full_final.csv'
INTO TABLE temp_character_family_tie
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    -- FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    -- LINES TERMINATED BY '\n'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (character1_name, character2_name, relation_name, biological_type_name);


--
-- create table character_family_tie
--

CREATE TABLE IF NOT EXISTS character_family_tie
    (
        family_tie_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        character1_id INTEGER NOT NULL,
        character2_id INTEGER NOT NULL,
        relation_type_id INTEGER,
        biological_type_id INTEGER,
        PRIMARY KEY (family_tie_id),
        FOREIGN KEY (character1_id) REFERENCES character_info(character_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (character2_id) REFERENCES character_info(character_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (relation_type_id) REFERENCES relation_type(relation_type_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (biological_type_id) REFERENCES biological_type(biological_type_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO character_family_tie
       (
         character1_id,
         character2_id,
         relation_type_id,
         biological_type_id
       )
SELECT c1.character_id, c2.character_id, r.relation_type_id, b.biological_type_id
    FROM temp_character_family_tie tcft
        INNER JOIN character_info c1
            ON tcft.character1_name = c1.full_name
        INNER JOIN character_info c2
            ON tcft.character2_name = c2.full_name
        INNER JOIN relation_type r
            ON tcft.relation_name = r.relation_type_name
        LEFT JOIN biological_type b
            ON tcft.biological_type_name = b.biological_type_name
    ORDER BY c1.character_id;


--
-- create temporary table and load data for character_title and character_aliase
--

CREATE TEMPORARY TABLE temp_character_title
    (
        id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        character_name VARCHAR(100) NOT NULL,
        title_name VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
        
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


CREATE TEMPORARY TABLE temp_character_aliase
    (
        id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        character_name VARCHAR(100) NOT NULL,
        aliase VARCHAR(100) NOT NULL,
        PRIMARY KEY (id)
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


LOAD DATA LOCAL INFILE '/Users/jelly/Development/18fall_code/si664_code/final-proj/finalproj/scripts/input/csv/character_title.csv'
INTO TABLE temp_character_title
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    -- FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    -- LINES TERMINATED BY '\n'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (character_name, title_name);

LOAD DATA LOCAL INFILE '/Users/jelly/Development/18fall_code/si664_code/final-proj/finalproj/scripts/input/csv/character_aliase.csv'
INTO TABLE temp_character_aliase
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    -- FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    -- LINES TERMINATED BY '\n'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (character_name, aliase);


--
-- create table and load data for character_aliase and character_title
--

CREATE TABLE IF NOT EXISTS character_title
    (
        character_title_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        character_id INTEGER NOT NULL,
        title_name VARCHAR(255) NOT NULL,
        PRIMARY KEY (character_title_id),
        FOREIGN KEY (character_id) REFERENCES character_info(character_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
        
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS character_aliase
    (
        character_aliase_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        character_id INTEGER NOT NULL,
        aliase VARCHAR(100) NOT NULL,
        PRIMARY KEY (character_aliase_id),
        FOREIGN KEY (character_id) REFERENCES character_info(character_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;



INSERT IGNORE INTO character_title
       (
         character_id,
         title_name
       )
SELECT c.character_id, tct.title_name
    FROM temp_character_title tct
        INNER JOIN character_info c
            ON tct.character_name = c.full_name;


INSERT IGNORE INTO character_aliase
       (
         character_id,
         aliase
       )
SELECT c.character_id, tca.aliase
    FROM temp_character_aliase tca
        INNER JOIN character_info c
            ON tca.character_name = c.full_name;



DROP TEMPORARY TABLE temp_house_icon, temp_character_img_ref, 
                     temp_character_info, temp_character_more_info, 
                     temp_character_family_tie, temp_character_aliase,
                     temp_character_title;
