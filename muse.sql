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

-- Sample Data
-- password = pass
INSERT INTO Users (name, email, password) VALUES ('angie', 'angie@fake.com',
        'd74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1');
INSERT INTO Themes (name) VALUES ('Bubbly');
INSERT INTO Themes (name) VALUES ('Meditative');
INSERT INTO Themes (name) VALUES ('Dubstep');
INSERT INTO Themes (name) VALUES ('Acoustic');
INSERT INTO Themes (name) VALUES ('Weird Al');