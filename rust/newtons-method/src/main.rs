use std::f32;

/// Trait for functions that can be solved using Newton's method
trait SolvableFunction {
    fn call(&self, x: f32) -> f32;
}

/// Implementation for closures
impl<F> SolvableFunction for F
where
    F: Fn(f32) -> f32,
{
    fn call(&self, x: f32) -> f32 {
        self(x)
    }
}

/// Newton's method solver
struct Newtons {
    tolerance: f32,
    epsilon: f32,
    max_iteration: usize,
}

impl Newtons {
    fn new() -> Self {
        Self {
            tolerance: 0.1,
            epsilon: 0.001,
            max_iteration: 20,
        }
    }

    /// Perform Newton's method
    ///
    /// # Arguments
    /// * `guess` - Initial guess for the solution
    /// * `f` - The function to find the root of
    /// * `f_derivative` - The derivative of the function
    ///
    /// # Returns
    /// * `Some(f32)` - The root if found within tolerance and max iterations
    /// * `None` - If no solution found within the constraints
    fn solve<F, D>(&self, guess: f32, f: &F, f_derivative: &D) -> Option<f32>
    where
        F: SolvableFunction,
        D: SolvableFunction,
    {
        let mut x0 = guess;

        for _ in 0..self.max_iteration {
            let y = f.call(x0);
            let y_derivative = f_derivative.call(x0);

            if y_derivative.abs() < self.epsilon {
                break;
            }

            let x1 = x0 - y / y_derivative;

            if (x1 - x0).abs() <= self.tolerance {
                return Some(x1);
            }

            x0 = x1;
        }

        None
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let f = |x: f32| x * x - 2.0;
    let f_derivative = |x: f32| 2.0 * x;

    let newtons = Newtons::new();
    let result = newtons.solve(2.0, &f, &f_derivative);

    match result {
        Some(value) => {
            println!("result = {}", value);

            if (f(value) - 0.0).abs() > newtons.tolerance {
                println!("result incorrect");
                std::process::exit(1);
            }
        }
        None => {
            std::process::exit(1);
        }
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_newtons_method_square_root() {
        let f = |x: f32| x * x - 2.0;
        let f_derivative = |x: f32| 2.0 * x;

        let newtons = Newtons::new();
        let result = newtons.solve(2.0, &f, &f_derivative);

        assert!(result.is_some());
        let value = result.unwrap();

        // Check that the result is approximately sqrt(2)
        let expected = 2.0_f32.sqrt();
        assert!((value - expected).abs() < 0.1);

        // Check that f(result) is close to 0
        assert!(f(value).abs() < newtons.tolerance);
    }

    #[test]
    fn test_newtons_method_custom_function() {
        // Find root of x^3 - x - 2 = 0 (should be around 1.52)
        let f = |x: f32| x * x * x - x - 2.0;
        let f_derivative = |x: f32| 3.0 * x * x - 1.0;

        let newtons = Newtons::new();
        let result = newtons.solve(2.0, &f, &f_derivative);

        assert!(result.is_some());
        let value = result.unwrap();

        // Check that f(result) is close to 0
        assert!(f(value).abs() < newtons.tolerance);
    }

    #[test]
    fn test_newtons_method_no_convergence() {
        // Function with derivative that becomes too small
        let f = |x: f32| x * x + 1.0; // No real roots
        let f_derivative = |x: f32| 2.0 * x;

        let mut newtons = Newtons::new();
        newtons.max_iteration = 5; // Limit iterations

        let result = newtons.solve(0.0, &f, &f_derivative);

        // Should not converge for this function
        assert!(result.is_none());
    }
}
