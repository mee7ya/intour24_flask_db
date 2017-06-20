SELECT s.*, array_agg(DISTINCT sp.name), array_agg(DISTINCT sp.image)
FROM sights s
LEFT JOIN sights_sight_property ssp
ON s.id = ssp.sight_id
LEFT JOIN sight_property sp
ON ssp.sight_property_id = sp.id
WHERE s.id = %s
GROUP BY s.id
ORDER BY s.id;
