import re
from typing import List


def _is_full_match(s: str, expression: str) -> bool:
  """
  Check if string matches the regular expression pattern completely.

  Args:
      s: String to check
      expression: Regular expression pattern

  Returns:
      True if string fully matches the pattern
  """
  return bool(re.fullmatch(expression, s))


def is_in_language_star_recursive(s: str, language: str) -> bool:
  """
  Check if string belongs to the Kleene star of a language using recursive approach.

  Args:
      s: String to check
      language: Regular expression pattern defining the language

  Returns:
      True if string is in the Kleene star of the language
  """
  if len(s) == 0:
    return True

  if _is_full_match(s, language):
    return True

  for i in range(len(s) - 1):
    if _is_full_match(s[: i + 1], language) and is_in_language_star_recursive(
      s[i + 1 :], language
    ):
      return True

  return False


def is_in_language_star_iterative(s: str, language: str) -> bool:
  """
  Check if string belongs to the Kleene star of a language using iterative approach.

  Args:
      s: String to check
      language: Regular expression pattern defining the language

  Returns:
      True if string is in the Kleene star of the language
  """
  results = [False] * (len(s) + 1)
  results[len(s)] = True

  for i in range(len(s) - 1, -1, -1):
    results[i] = False

    for j in range(i + 1, len(s) + 1):
      # Extract slice from i to j (exclusive)
      slice_str = s[i:j]

      if _is_full_match(slice_str, language) and results[j]:
        results[i] = True
        break

  return results[0]
