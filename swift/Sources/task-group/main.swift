func demoTaskGroup() async {
  await withTaskGroup(of: [String].self) { group in
    group.addTask { ["Start"] }

    while let result = await group.next() {
      let tid = getThreadId()
      print("\(tid): \(result)")

      if result.count == 1 {
        group.addTask { ["Hello", "World"] }
      }

      if result.count == 2 {
        group.addTask { ["Goodbye", "World", "!"] }
      }
    }
  }
}

await demoTaskGroup()
