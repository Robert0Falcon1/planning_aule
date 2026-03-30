-- ICE Planning Aule - Database Initialization
-- Eseguito automaticamente al primo avvio MySQL

-- Imposta charset e collation corretti
ALTER DATABASE planning_aule CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Le tabelle vengono create automaticamente da SQLAlchemy al primo avvio del backend
-- Questo file può essere usato per seed data iniziali se necessario

-- Esempio: inserire sedi di default
-- INSERT INTO sedi (nome) VALUES 
--     ('Torino'),
--     ('Cuneo'),
--     ('Asti'),
--     ('Novara'),
--     ('Biella');
