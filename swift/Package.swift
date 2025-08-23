// swift-tools-version: 6.1
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let examples = [
  "non-copyable",
  "pack-iteration",
  "task-group",
]

let targets: [Target] = examples.map { .executableTarget(name: $0) }
let products: [Product] = examples.map { .executable(name: $0, targets: [$0]) }

let package = Package(
  name: "SwiftExamples",
  platforms: [.macOS(.v15)],
  products: products,
  targets: targets
)
