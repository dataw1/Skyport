CREATE OR REPLACE FUNCTION anuluj_rezerwacje_po_odwolaniu_lotu()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'Odwołany' AND OLD.status IS DISTINCT FROM 'Odwołany' THEN
        UPDATE rezerwacje_lotow
        SET status = 'Anulowana'
        WHERE id_lotu = NEW.id_lotu AND status != 'Anulowana';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_anuluj_rezerwacje_lotu
AFTER UPDATE OF status ON loty
FOR EACH ROW
EXECUTE PROCEDURE anuluj_rezerwacje_po_odwolaniu_lotu();