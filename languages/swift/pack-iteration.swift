protocol PlanItem {
  var total: Int { get }
}

struct MonthlyPlanItem: PlanItem {
  var total: Int = 1
}

struct WeeklyPlanItem: PlanItem {
  var total: Int = 2
}

@resultBuilder
struct PlanBuilder {
  static func buildBlock<each T: PlanItem>(_ values: repeat each T) -> String {
    var count = 0

    for item in repeat each values {
      count += item.total
    }

    return "Total \(count)"
  }
}

@PlanBuilder
func plan() -> String {
  MonthlyPlanItem()
  MonthlyPlanItem()
  WeeklyPlanItem()
}

print(plan())
