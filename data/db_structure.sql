-- Creating table 'specializations'
CREATE TABLE specializations (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100) NOT NULL,
    description NVARCHAR(MAX) NULL
);

-- Creating table 'groups'
CREATE TABLE groups (
    id INT PRIMARY KEY IDENTITY(1,1),
    course_number INT NOT NULL,
    group_number INT NOT NULL,
    specialization_id INT NOT NULL,
    student_count INT NOT NULL,
    FOREIGN KEY (specialization_id) REFERENCES specializations(id)
);

-- Creating table 'students'
CREATE TABLE students (
    id INT PRIMARY KEY IDENTITY(1,1),
    full_name NVARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    group_id INT NOT NULL,
    record_book_number NVARCHAR(50) NOT NULL,
    enrollment_date DATE NOT NULL,
    average_grade DECIMAL(5,2) NULL,
    FOREIGN KEY (group_id) REFERENCES groups(id)
);
