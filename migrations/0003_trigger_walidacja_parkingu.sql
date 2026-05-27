CREATE OR REPLACE FUNCTION waliduj_daty_rezerwacji_parkingu()
RETURNS TRIGGER AS $$
BEGIN

    IF NEW.data_wyjazdu <= NEW.data_przyjazdu THEN
        RAISE EXCEPTION 'Błąd walidacji: Data wyjazdu musi być późniejsza niż data przyjazdu.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_waliduj_daty_parkingu
BEFORE INSERT OR UPDATE ON rezerwacje_parkingu
FOR EACH ROW
EXECUTE PROCEDURE waliduj_daty_rezerwacji_parkingu();