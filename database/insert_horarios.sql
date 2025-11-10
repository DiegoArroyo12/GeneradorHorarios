USE horarios;

-- Profesores
INSERT INTO profesores (nombre, paterno, materno, correo) 
VALUES  ('Gabriel', 'Ortiz', 'Cordero', 'gabrielortizoic@aragon.unam.mx'),
		('Abel', 'Verde', 'Cruz', 'abelverde53@aragon.unam.mx'),
        ('Sergio', 'Hernandez', 'López', 'sergiohernandezhel@aragon.unam.mx');

-- Salones
INSERT INTO salones (nombre) 
VALUES  ('A214'),
		('A215');

-- Materias
INSERT INTO materias (clave, nombre, semestre) 
VALUES  (1110, 'Álgebra', 1),
		(1109, 'Cálculo Diferencial e Integral', 1);

-- Grupos
INSERT INTO grupos (id_materia, id_profesor, id_salon, turno, grupo) 
VALUES  (1, 1, 1, 'Matutino', 1107),
		(2, 2, 1, 'Matutino', 1107),
        (1, 3, 2, 'Matutino', 1108);
        
-- Horarios de grupos
INSERT INTO horarios_grupo (id_grupo, dia_semana, hora_inicio, hora_fin)
VALUES  (1, 'Martes', '11:00:00', '13:00:00'),
		(1, 'Jueves', '11:00:00', '13:00:00'),
        (2, 'Martes', '09:00:00', '11:00:00'),
        (2, 'Jueves', '09:00:00', '11:00:00'),
        (3, 'Lunes', '07:00:00', '08:30:00'),
        (3, 'Miércoles', '07:00:00', '08:30:00'),
        (3, 'Viernes', '07:00:00', '08:30:00');