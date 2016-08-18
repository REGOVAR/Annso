 
--
-- Update refgen database with the list of impacted variants
--

UPDATE refgene_hg19 SET variant_ids=array_agg(v.id)
FROM variant_hg19 v
LEFT JOIN refgene_hg19 rg ON rg.txrange @> int8(v.pos)
GROUP BY v.id
