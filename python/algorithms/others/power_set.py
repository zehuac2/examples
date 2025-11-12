from typing import List, TypeVar, Sequence

T = TypeVar('T')


def get_power_set(set_: Sequence[T]) -> List[List[T]]:
  output: List[List[T]] = []
  if len(set_) == 0:
    output.append([])
    return output
  set_head = set_[0]
  set_rest = set_[1:]
  for power_set in get_power_set(set_rest):
    buffer = [set_head]
    buffer.extend(power_set)
    output.append(buffer)
    output.append(power_set)
  return output
