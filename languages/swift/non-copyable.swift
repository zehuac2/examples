struct Peter: ~Copyable {
  var id: Int

  consuming func die() {
    print("Peter \(id) died")
  }

  borrowing func foo() {
    withUnsafePointer(to: self) { pointer in
      print("foo(): Peter is \(pointer)")
    }
  }

  // boo is borrowing by default.
  func boo() {
    withUnsafePointer(to: self) { pointer in
      print("boo(): Peter is \(pointer)")
    }
  }
}

func kill(_ peter: consuming Peter) {
  peter.die()
}

func run() {
  let peter = Peter(id: 1)

  peter.foo()
  peter.foo()

  peter.boo()
  peter.boo()

  kill(peter)
  // kill(peter)
  // ^- error: peter is already consumed
}

run()
