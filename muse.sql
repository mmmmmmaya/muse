CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    name varchar(100) NOT NULL,
    email varchar(50) NOT NULL UNIQUE,
    password varchar(64) NOT NULL,
    zipcode varchar(10),
    country varchar(2)
);

CREATE TABLE Themes (
    id SERIAL PRIMARY KEY,
    name varchar(25) NOT NULL UNIQUE
);

CREATE TABLE Recordings (
    id SERIAL PRIMARY KEY,
    name varchar(200) DEFAULT 'Untitled',
    public boolean NOT NULL DEFAULT True,
    user_id int REFERENCES Users(id) NOT NULL,
    created_at timestamp DEFAULT now()
);

CREATE TABLE KeyPresses (
    id SERIAL PRIMARY KEY,
    recording_id int REFERENCES Recordings(id) NOT NULL,
    key_pressed varchar(1) NOT NULL,
    time_to_next_key int,
    theme int REFERENCES Themes(id) NOT NULL
);

CREATE TABLE Views (
    id SERIAL PRIMARY KEY,
    recording_id int REFERENCES Recordings(id) NOT NULL,
    ip_address inet,
    viewed_at timestamp DEFAULT now()
);

CREATE TABLE Konami (
    id SERIAL PRIMARY KEY,
    direction varchar(5) NOT NULL,
    time_to_next_arrow int
);

-- Sample Data
-- password = pass
INSERT INTO Users (name, email, password) VALUES ('angie', 'angie@fake.com',
        'ede5ed2940003794f2f9631bbcdf0e02eae79006d035843cefb34d92ce056c62');
INSERT INTO Themes (name) VALUES ('Symphony');
INSERT INTO Themes (name) VALUES ('Meditative');
INSERT INTO Themes (name) VALUES ('Dubstep');
INSERT INTO Themes (name) VALUES ('Acoustic');
INSERT INTO Themes (name) VALUES ('Chiptune');

-- Konami Data
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 428);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 410);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 416);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 347);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 236);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 261);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 286);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 195);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 259);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 183);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 267);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 165);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 267);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 309);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 92);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 177);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 473);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 298);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 184);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 296);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 105);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 441);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 282);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 327);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 123);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 349);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 134);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 236);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 242);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 277);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 214);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 240);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 317);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 108);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 199);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 151);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 197);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 190);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 237);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 310);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 415);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 264);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 105);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 212);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 304);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 163);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 270);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 331);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 272);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 244);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 284);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 247);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 265);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 154);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 319);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 308);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 315);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 270);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 217);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 194);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 476);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 297);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 304);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 237);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 354);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 462);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 446);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 396);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 191);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 623);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 170);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 275);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 264);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 156);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 299);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 160);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 305);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 127);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 607);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 164);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 299);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 279);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 111);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 182);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 1379);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 189);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 278);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 235);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 150);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 347);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 150);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 265);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 188);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 543);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 144);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('right', 330);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 265);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('up', 187);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', 324);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('left', 588);
INSERT INTO Konami (direction, time_to_next_arrow) VALUES('down', NULL);
