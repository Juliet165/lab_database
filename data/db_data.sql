-- Adding data into specializations table
INSERT INTO specializations (name, description)
VALUES 
('Ïðèêëàäíàÿ èíôîðìàòèêà', 'Ðàçðàáîòêà è ïðîåêòèðîâàíèå ÏÎ.'),
('Èíôîðìàòèêà', 'Ìàòåìàòèêà è ðàçðàáîòêà ÏÎ.');

-- Adding data into groups table
INSERT INTO groups (course_number, group_number, specialization_id, student_count)
VALUES 
(1, 11, 1, 22), 
(2, 13, 1, 28);  

-- Adding data into students table
INSERT INTO students (full_name, birth_date, group_id, enrollment_date, average_grade)
VALUES 
('Êàíîïëè÷ Þëèÿ', '2005-05-16', 2, '2022-09-01', 9.00),  
('Ñàìñîíîâà Âèêòîðèÿ', '2005-06-09', 1, '2022-09-01', 7.98),
('Ãîðåëèê Ìàðèÿ', '2004-08-24', 2, '2022-09-01', 9.25);  

