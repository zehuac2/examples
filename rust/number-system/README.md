# Number System Converter

A Rust implementation of a number system converter that can convert decimal
numbers to any base representation.

## Features

- Convert decimal numbers to any base (binary, ternary, etc.)
- Efficient division algorithm with remainder calculation
- Comprehensive test suite

## Usage

To run the example:

```bash
cargo run --bin number-system
```

To run tests:

```bash
cargo test
```

## Example Output

```
0 (base 2) = 0
5 (base 2) = 1 0 1
5 (base 3) = 1 2
```

## Implementation Details

The implementation includes:

- `divide()`: A function that performs division and returns both quotient (by
  modifying the input) and remainder
- `to_xnary()`: Converts a decimal number to any base representation
- `print_xnary()`: Prints the converted number in a readable format

This is a Rust port of the original C++ implementation, maintaining the same
algorithm while leveraging Rust's memory safety and ownership features.
