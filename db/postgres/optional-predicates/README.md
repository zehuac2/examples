# Optional Predicates

This folder demonstrates how to implement DB controllers that expose optional predicates.

```java
public final class TestController {
  public static class Filters {
    @Nullable Integer id;
    @Nullable String name;
  }

  public List<Test> find(Filters filters) {
    // ...
  }
}
```
