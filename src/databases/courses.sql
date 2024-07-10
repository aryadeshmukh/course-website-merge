-- Table of courses containing code, name, and link to the course.
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT NOT NULL,
    course_name TEXT NOT NULL,
    course_link TEXT NOT NULL
);

-- Insert courses into the table.
INSERT INTO courses (course_code, course_name, course_link) VALUES
('EECS16B', 'Designing Information Devices and Systems II', 'https://eecs16b.org/'),
('COMPSCI61B', 'Data Structures', 'https://sp24.datastructur.es/'),
('DATAC8', 'Foundations of Data Science', 'https://www.data8.org/sp24/');