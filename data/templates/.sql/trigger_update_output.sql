CREATE TRIGGER IF NOT EXISTS update_output_iteration
    AFTER INSERT
    ON output_files
    FOR EACH ROW
BEGIN
    UPDATE output_files
    SET iteration_no = (SELECT COUNT(*) FROM output_files WHERE model_id = NEW.model_id)
    WHERE id = NEW.id;
END;