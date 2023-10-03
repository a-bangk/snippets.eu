Useful SQL commands


Delete all unused tags
```sql
delete from notetag where id in(
SELECT n.id
FROM notetag n
left JOIN associate_notetag_note ann 
ON n.id = ann.notetag_id
where ann.note_id is Null
);
```
