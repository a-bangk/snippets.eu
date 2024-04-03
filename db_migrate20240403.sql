CREATE OR REPLACE VIEW snippet_view AS
WITH nt AS (
  SELECT 
    ann.note_id, 
    GROUP_CONCAT(nt.tag ORDER BY tag ASC SEPARATOR '; ') AS tags
  FROM 
    associate_notetag_note ann 
    JOIN notetag nt ON nt.id = ann.notetag_id 
  GROUP BY 
    ann.note_id
), 
s AS (
  SELECT 
    asn.note_id, 
    GROUP_CONCAT(s.title SEPARATOR ', ') AS sources, 
    s.id, 
    s.url 
  FROM 
    associate_source_note asn 
    JOIN source s ON s.id = asn.source_id 
  GROUP BY 
    asn.note_id
) 
SELECT 
  n.id as note_id,
  s.id as source_id, 
  n.content as content,
  n.update_epoch as note_update_epoch, 
  nt.tags as tags,
  s.sources as sources, 
  s.url as url, 
  u.username username, 
  u.id as user_id
FROM 
  note n 
  LEFT JOIN nt ON nt.note_id = n.id 
  LEFT JOIN s ON s.note_id = n.id 
  JOIN user u ON n.user_id = u.id;
