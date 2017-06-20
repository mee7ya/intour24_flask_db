SELECT e.id, e.name, e.description, e.duration, p.price_for_children, p.price_for_adult,
p.price_for_enfant, pp.name, c.name,
e.average_rating, array_agg(DISTINCT ep.name), e.images, p.id, pp.id, c.id, array_agg(DISTINCT ep.id),
o.id, o.name, o.phone, o.address, o.logo, o.accreditation, e.capacity, e.link_to_site,
array_agg(DISTINCT ep.icon), c.icon
FROM excursions e
LEFT JOIN prices p
ON e.price_id = p.id
LEFT JOIN picking_places pp
ON e.picking_place_id = pp.id
LEFT JOIN category c
ON e.category_id = c.id
LEFT JOIN excursions_excursion_property eep
ON e.id = eep.excursion_id
LEFT JOIN excursion_property ep
ON ep.id = eep.excursion_property_id
LEFT JOIN operator o
ON o.id = e.operator_id
WHERE e.id = %s
GROUP BY e.id, p.price_for_children, p.price_for_adult, p.price_for_enfant, p.id, pp.id, c.id,
pp.name, e.average_rating, c.name, o.id;
