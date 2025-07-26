/// Divide a number by a divisor, modifying the dividend to be the quotient
///
/// # Arguments
/// * `divided` - The number to be divided, will be modified to contain the quotient
/// * `divisor` - The divisor
///
/// # Returns
/// The remainder
fn divide(divided: &mut usize, divisor: usize) -> usize {
    let quotient = *divided / divisor;
    let remainder = *divided - divisor * quotient;

    *divided = quotient;

    remainder
}

/// Convert an integer to x-nary representation
///
/// # Arguments
/// * `x` - The number to be converted
/// * `xnary` - The base for conversion
///
/// # Returns
/// Vector containing the x-nary representation (most significant digit first)
fn to_xnary(mut x: usize, xnary: usize) -> Vec<usize> {
    let mut result = Vec::new();

    while x >= xnary {
        let remainder = divide(&mut x, xnary);
        result.push(remainder);
    }

    result.push(x);

    // Reverse to get most significant digit first
    result.reverse();
    result
}

/// Print the x-nary representation of a number
///
/// # Arguments
/// * `x` - The number to convert and print
/// * `xnary` - The base for conversion
fn print_xnary(x: usize, xnary: usize) {
    let result = to_xnary(x, xnary);

    print!("{} (base {}) = ", x, xnary);

    for num in &result {
        print!("{} ", num);
    }

    println!();
}

fn main() {
    // 0 (base 2) = 0
    print_xnary(0, 2);

    // 5 (base 2) = 1 0 1
    print_xnary(5, 2);

    // 5 (base 3) = 1 2
    print_xnary(5, 3);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_divide() {
        let mut dividend = 10;
        let remainder = divide(&mut dividend, 3);
        assert_eq!(dividend, 3);
        assert_eq!(remainder, 1);
    }

    #[test]
    fn test_to_xnary_binary() {
        assert_eq!(to_xnary(0, 2), vec![0]);
        assert_eq!(to_xnary(5, 2), vec![1, 0, 1]);
        assert_eq!(to_xnary(8, 2), vec![1, 0, 0, 0]);
    }

    #[test]
    fn test_to_xnary_ternary() {
        assert_eq!(to_xnary(5, 3), vec![1, 2]);
        assert_eq!(to_xnary(9, 3), vec![1, 0, 0]);
    }

    #[test]
    fn test_to_xnary_decimal() {
        assert_eq!(to_xnary(123, 10), vec![1, 2, 3]);
        assert_eq!(to_xnary(0, 10), vec![0]);
    }
}
