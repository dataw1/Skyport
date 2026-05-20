INSERT INTO parkingi (nazwa, pojemnosc_total, cena_bazowa) VALUES 
('Krótkoterminowy', 100, 15.00),
('Długoterminowy', 300, 45.00),
('Premium', 50, 65.00)
ON CONFLICT (nazwa) DO NOTHING;

