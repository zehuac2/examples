prepare query as
select * from test
where
  --could not determine data type of parameter $1
  $1 is not null and id = $1
  or $2 is not null and name = $2;

execute query (1, null);
execute query (null, 'test 1');
execute query (null, null);
execute query (2, 'test 2');
