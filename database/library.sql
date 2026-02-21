CREATE TABLE Librarian (
    librarian_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    roll_no VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    batch VARCHAR(10),
    faculty VARCHAR(10),
    email VARCHAR(50) UNIQUE
);
CREATE TABLE Author (
    author_id SERIAL PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL
);
CREATE TABLE Books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    total_copies INT NOT NULL CHECK (total_copies >= 0),
    available_copies INT NOT NULL CHECK (available_copies >= 0),
    author_id INT,
    CONSTRAINT fk_author
        FOREIGN KEY (author_id)
        REFERENCES Author(author_id)
        ON DELETE SET NULL
);
CREATE TABLE Semester (
    semester_id SERIAL PRIMARY KEY,
    semester_no INT NOT NULL,
    batch VARCHAR(10),
    faculty VARCHAR(10)
);
CREATE TABLE Book_Semester (
    book_id INT,
    semester_id INT,
    PRIMARY KEY (book_id, semester_id),
    CONSTRAINT fk_book
        FOREIGN KEY (book_id)
        REFERENCES Books(book_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_semester
        FOREIGN KEY (semester_id)
        REFERENCES Semester(semester_id)
        ON DELETE CASCADE
);
CREATE TABLE Issued_Book (
    issue_id SERIAL PRIMARY KEY,
    issue_date DATE NOT NULL,
    return_date DATE,
    status VARCHAR(10),
    user_id INT,
    book_id INT,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_issued_book
        FOREIGN KEY (book_id)
        REFERENCES Books(book_id)
        ON DELETE CASCADE
);
INSERT INTO Librarian (name, email, password)
VALUES ('Admin', 'admin@gmail.com', 'admin1234');
INSERT INTO Librarian (name, email, password)
values ('Naresh','naresh@gmail.com','Naresh123@');

select * from Books
ALTER TABLE Books
ADD COLUMN book_number VARCHAR(50) UNIQUE;

select * from Books
select * from Users