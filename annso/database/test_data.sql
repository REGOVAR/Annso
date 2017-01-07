


INSERT INTO public.analysis(id, name, setting, creation_date, update_date)
VALUES (10000, 'Test Annso Normal', '{"fields": [2, 4, 5, 6, 7, 8, 9, 11, 22, 16], "filter": ["AND", [["==",["field",4], ["value", 1]], [">", ["field", 9], ["value", 50]]]]}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);





INSERT INTO public.sample(id, name, is_mosaic) VALUES
    (10010, 'TA-Normal-01', False),
    (10011, 'TA-Normal-02', False),
    (10012, 'TA-Normal-03', False);

INSERT INTO public.analysis_sample(analysis_id, sample_id, nickname) VALUES
    (10000, 10010, 'Papa'),
    (10000, 10011, 'Maman'),
    (10000, 10012, 'Fille');



INSERT INTO public.attribute(analysis_id, sample_id, name, value) VALUES
    (10000, 10010, 'Is Control', 'Y'),
    (10000, 10011, 'Is Control', 'Y'),
    (10000, 10012, 'Is Control', 'N'),
    (10000, 10010, 'Sex', 'M'),
    (10000, 10011, 'Sex', 'F'),
    (10000, 10012, 'Sex', 'F');


INSERT INTO public.variant_hg19(id, chr, pos, ref, alt) VALUES
-- Homo => Homo
    (20000000, '1', 1, 'A', 'T'), -- *
    (20000001, '2', 1, 'A', 'T'), -- p,m
    (20000002, '2', 2, 'A', 'T'), -- p,f
    (20000003, '2', 3, 'A', 'T'), -- m,f
    (20000004, '3', 1, 'A', 'T'), -- p
    (20000005, '3', 2, 'A', 'T'), -- m
    (20000006, '3', 3, 'A', 'T'), -- f
-- Hetero ref => Hetero ref
    (20000007, '1', 101, 'A', 'C'), -- *
    (20000008, '2', 101, 'A', 'C'), -- p,m
    (20000009, '2', 102, 'A', 'C'), -- p,f
    (20000010, '2', 103, 'A', 'C'), -- m,f
    (20000011, '3', 101, 'A', 'C'), -- p
    (20000012, '3', 102, 'A', 'C'), -- m
    (20000013, '3', 103, 'A', 'C'), -- f
-- Hetero alt
    (20000014, '1', 201, 'C', 'G'), -- a1 : *
    (20000015, '1', 201, 'C', 'A'), -- a2 : *
    (20000016, '2', 201, 'C', 'G'), -- a1 : p,m
    (20000017, '2', 201, 'C', 'A'), -- a2 : p,m
    (20000018, '2', 202, 'C', 'G'), -- a1 : p,f
    (20000019, '2', 202, 'C', 'A'), -- a2 : p,f
    (20000020, '2', 203, 'C', 'G'), -- a1 : m,f
    (20000021, '2', 203, 'C', 'A'), -- a2 : m,f
    (20000022, '3', 201, 'C', 'G'), -- a1 : p
    (20000023, '3', 201, 'C', 'A'), -- a2 : p
    (20000024, '3', 202, 'C', 'G'), -- a1 : m
    (20000025, '3', 202, 'C', 'A'), -- a2 : m
    (20000026, '3', 203, 'C', 'G'), -- a1 : f
    (20000027, '3', 203, 'C', 'A'); -- a2 : f


INSERT INTO public.sample_variant_hg19(sample_id, variant_id, chr, pos, ref, alt, genotype, deepth) VALUES
-- N-Papa
    (10010, 20000000, '1', 1, 'A', 'T', 1, 100),
    (10010, 20000001, '2', 1, 'A', 'T', 1, 100),
    (10010, 20000002, '2', 2, 'A', 'T', 1, 100),
    (10010, 20000004, '3', 1, 'A', 'T', 1, 100),

    (10010, 20000007, '1', 101, 'A', 'C', 2, 50),
    (10010, 20000008, '2', 101, 'A', 'C', 2, 50),
    (10010, 20000009, '2', 102, 'A', 'C', 2, 50),
    (10010, 20000011, '3', 101, 'A', 'C', 2, 50),

    (10010, 20000016, '2', 201, 'C', 'G', 2, 50), -- a1 : p,m
    (10010, 20000017, '2', 201, 'C', 'A', 2, 50), -- a2 : p,m
    (10010, 20000018, '2', 202, 'C', 'G', 2, 50), -- a1 : p,f
    (10010, 20000019, '2', 202, 'C', 'A', 2, 50), -- a2 : p,f
    (10010, 20000022, '3', 201, 'C', 'G', 2, 50), -- a1 : p
    (10010, 20000023, '3', 201, 'C', 'A', 2, 50), -- a2 : p

-- N-Maman
    (10011, 20000000, '1', 1, 'A', 'T', 1, 100),
    (10011, 20000001, '2', 1, 'A', 'T', 1, 100),
    (10011, 20000003, '2', 3, 'A', 'T', 1, 100),
    (10011, 20000005, '3', 2, 'A', 'T', 1, 100),

    (10011, 20000007, '1', 101, 'A', 'C', 2, 50),
    (10011, 20000008, '2', 101, 'A', 'C', 2, 50),
    (10011, 20000010, '2', 103, 'A', 'C', 2, 50),
    (10011, 20000012, '3', 102, 'A', 'C', 2, 50),

    (10011, 20000016, '2', 201, 'C', 'G', 2, 50), -- a1 : p,m
    (10011, 20000017, '2', 201, 'C', 'A', 2, 50), -- a2 : p,m
    (10011, 20000020, '2', 203, 'C', 'G', 2, 50), -- a1 : m,f
    (10011, 20000021, '2', 203, 'C', 'A', 2, 50), -- a2 : m,f
    (10011, 20000024, '3', 202, 'C', 'G', 2, 50), -- a1 : m
    (10011, 20000025, '3', 202, 'C', 'A', 2, 50), -- a2 : m


-- N-Fille
    (10012, 20000000, '1', 1, 'A', 'T', 1, 100),
    (10012, 20000002, '2', 2, 'A', 'T', 1, 100),
    (10012, 20000003, '2', 3, 'A', 'T', 1, 100),
    (10012, 20000006, '3', 3, 'A', 'T', 1, 100),

    (10012, 20000007, '1', 101, 'A', 'C', 2, 50),
    (10012, 20000009, '2', 102, 'A', 'C', 2, 50),
    (10012, 20000010, '2', 103, 'A', 'C', 2, 50),
    (10012, 20000013, '3', 103, 'A', 'C', 2, 50),

    (10012, 20000018, '2', 202, 'C', 'G', 2, 50), -- a1 : p,f
    (10012, 20000019, '2', 202, 'C', 'A', 2, 50), -- a2 : p,f
    (10012, 20000020, '2', 203, 'C', 'G', 2, 50), -- a1 : m,f
    (10012, 20000021, '2', 203, 'C', 'A', 2, 50), -- a2 : m,f
    (10012, 20000026, '3', 203, 'C', 'G', 2, 50), -- a1 : f
    (10012, 20000027, '3', 203, 'C', 'A', 2, 50); -- a2 : f