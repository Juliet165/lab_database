-- ������� ������ � ������� specializations
INSERT INTO specializations (name, description)
VALUES 
('���������� �����������', '���������� � �������������� ��.'),
('�����������', '���������� � ���������� ��.');

-- ������� ������ � ������� groups
INSERT INTO groups (course_number, group_number, specialization_id, student_count)
VALUES 
(1, 11, 1, 22), 
(2, 13, 1, 28);  

-- ������� ������ � ������� students
INSERT INTO students (full_name, birth_date, group_id, enrollment_date, average_grade)
VALUES 
('�������� ����', '2005-05-16', 2, '2022-09-01', 9.00),  
('��������� ��������', '2005-06-09', 1, '2022-09-01', 7.98),
('������� �����', '2004-08-24', 2, '2022-09-01', 9.25);  

