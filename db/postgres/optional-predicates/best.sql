create or replace function find_test_records(
  p_id int default null,
  p_name text default null
)
returns setof test as $$
declare
  predicates text[];
  final_query text;
begin
  -- build an array of where clauses
  if p_id is not null then
    predicates := array_append(predicates, 'id = $1');
  end if;

  if p_name is not null then
    predicates := array_append(predicates, 'name = $2');
  end if;

  -- join them with and
  final_query := 'select * from test';
  if array_length(predicates, 1) > 0 then
    final_query := final_query || ' where ' || array_to_string(predicates, ' and ');
  end if;

  return query execute final_query using p_id, p_name;
end;
$$ language plpgsql;

-- filters by id only
select * from find_test_records(p_id => 1);
-- filters by name only
select * from find_test_records(p_name => 'test 1');
-- no filters (returns all)
select * from find_test_records();
