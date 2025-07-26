# Newton's Method in Rust

This is a Rust implementation of Newton's method for finding roots of functions,
migrated from the C++ version.

## Overview

Newton's method is an iterative numerical technique for finding roots of
real-valued functions. Given a function f(x) and its derivative f'(x), the
method uses the iteration:

```
x_{n+1} = x_n - f(x_n) / f'(x_n)
```

## Features

- Generic trait-based design for function types
- Configurable tolerance, epsilon, and maximum iterations
- Comprehensive error handling
- Unit tests included

## Usage

```rust
let f = |x: f32| x * x - 2.0;           // Function: x² - 2
let f_derivative = |x: f32| 2.0 * x;    // Derivative: 2x

let newtons = Newtons::new();
let result = newtons.solve(2.0, &f, &f_derivative);

match result {
    Some(root) => println!("Root found: {}", root),
    None => println!("No convergence"),
}
```

## Running

```bash
cargo run --bin newtons-method
```

## Testing

```bash
cargo test
```

## Key Differences from C++ Version

1. **Memory Safety**: Rust's ownership system prevents common C++ pitfalls
2. **Error Handling**: Uses `Option<f32>` instead of `std::optional<float>`
3. **Trait System**: Uses traits instead of C++ concepts for generic programming
4. **Pattern Matching**: Uses `match` for more expressive control flow
5. **Testing**: Built-in testing framework with `#[cfg(test)]`
