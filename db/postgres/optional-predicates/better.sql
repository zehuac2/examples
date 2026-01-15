/*
Possible performance issues
Planner have to build a generic plan so it can't use indexes and might have to a full table scan.
It is best to synthesize the query in the application code.
*/
prepare query as
select * from test
where
  (cast($1 as int) is null or id = $1)
  and (cast($2 as text) is null or name = $2);

execute query (1, null);
execute query (null, 'test 1');
execute query (null, null);
execute query (2, 'test 2');
