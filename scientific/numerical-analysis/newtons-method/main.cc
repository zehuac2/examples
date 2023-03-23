#include <exception>
#include <iostream>
#include <optional>
#include <type_traits>

using std::cout;
using std::endl;
using std::optional;
using std::size_t;

template <typename T>
concept floating_point = std::is_floating_point_v<T>;

template <typename T>
concept solvable_function = requires(T t) {
  { t(1.0f) } -> floating_point;
};

struct newtons {
  float tolerance = 0.1f;
  float epsilon = 0.001f;

  size_t max_iteration = 20;

  /**
   * @brief Perform newton's method
   * @param f function
   * @param f_derivative derivative of f
   */
  template <solvable_function FuncT, solvable_function FuncDerivativeT>
  optional<float> solve(float guess, const FuncT &f,
                        const FuncDerivativeT &f_derivative) {
    float x0 = guess;
    float x1 = x0;

    for (size_t i = 0; i < max_iteration; i++) {
      float y = f(x0);
      float y_derivative = f_derivative(x0);

      if (std::abs(y_derivative) < epsilon) {
        break;
      }

      x1 = x0 - y / y_derivative;

      if (std::abs(x1 - x0) <= tolerance) {
        return x1;
      }

      x0 = x1;
    }

    return std::nullopt;
  }
};

int main() {
  const auto f = [=](float x) -> float { return x * x - 2; };
  const auto f_derivative = [=](float x) -> float { return 2 * x; };

  newtons newtons;
  optional<float> result = newtons.solve(2.0f, f, f_derivative);

  if (!result) {
    return 1;
  }

  cout << "result = " << result.value() << endl;

  if (std::abs(f(result.value()) - 0.0f) > newtons.tolerance) {
    cout << "result incorrect" << endl;
    return 1;
  }

  return 0;
}
