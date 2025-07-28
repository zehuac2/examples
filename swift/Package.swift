// swift-tools-version: 6.1
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
  name: "SwiftExamples",
  products: [
    .executable(name: "non-copyable", targets: ["non-copyable"]),
    .executable(name: "pack-iteration", targets: ["pack-iteration"]),
  ],
  targets: [
    .executableTarget(name: "non-copyable"),
    .executableTarget(name: "pack-iteration"),
  ],
)
