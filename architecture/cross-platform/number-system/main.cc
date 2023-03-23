#include <iostream>
#include <vector>
#include <algorithm>

using std::cout;
using std::endl;
using std::vector;

/// @brief divide a number by a divisor
/// @param divided the number to be divided, this value will be the quotient
/// after this function has returned
/// @param divisor the divisor
/// @returns the remainder
size_t divide(size_t &divided, size_t divisor) {
  size_t quotient = divided / divisor;
  size_t remainder = divided - divisor * quotient;

  divided = quotient;

  return remainder;
}

/// @brief convert an int to xnary representation
/// @param x the numbe to be converted
/// @param xnary xnary
/// @returns xnary representation
vector<size_t> to_xnary(size_t x, size_t xnary) {
  vector<size_t> result;

  while (x >= xnary) {
    size_t remainder = divide(x, xnary);
    result.push_back(remainder);
  }

  result.push_back(x);

  std::reverse(result.begin(), result.end());
  return result;
}

void print_xnary(size_t x, size_t xnary) {
  vector<size_t> result;

  result = to_xnary(x, xnary);

  cout << x << " (base " << xnary << ") = ";

  for (size_t num : result) {
    cout << num << " ";
  }

  cout << endl;
}

int main() {
  // 0 (base 2) = 0
  print_xnary(0, 2);

  // 5 (base 2) = 1 0 1
  print_xnary(5, 2);

  // 5 (base 3) = 1 2
  print_xnary(5, 3);

  return 0;
}
