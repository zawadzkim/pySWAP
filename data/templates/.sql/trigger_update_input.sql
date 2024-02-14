CREATE TRIGGER IF NOT EXISTS update_input_iteration
    AFTER INSERT
    ON input_files
    FOR EACH ROW
BEGIN
    UPDATE input_files
    SET iteration_no = (SELECT COUNT(*) FROM input_files WHERE model_id = NEW.model_id)
    WHERE id = NEW.id;
END;