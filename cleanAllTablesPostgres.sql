DO
$$
DECLARE
    r RECORD;
BEGIN
    -- Desactiva restricciones de clave externa temporalmente
    EXECUTE 'SET session_replication_role = replica';

    -- Trunca cada tabla
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'TRUNCATE TABLE public.' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE';
    END LOOP;

    -- Reactiva restricciones de clave externa
    EXECUTE 'SET session_replication_role = DEFAULT';
END;
$$;
--Ejecutar dentro de postgres para limpioar la dbcompleta
