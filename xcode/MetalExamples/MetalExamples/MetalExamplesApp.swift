//
//  MetalExamplesApp.swift
//  MetalExamples
//
//  Created by Zehua Chen on 8/13/25.
//

import SwiftUI

class AppDelegate: NSObject, NSApplicationDelegate {
  func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
    return true
  }
}

@main
struct MetalExamplesApp: App {
  @NSApplicationDelegateAdaptor
  var delegate: AppDelegate

  @State
  var wireframe: Bool = false

  @State
  var scale: Float = 1

  var body: some Scene {
    WindowGroup {
      BasicRenderingView(wireframe: wireframe)
        .frame(minWidth: 400, minHeight: 400)
    }
    .commands {
      CommandMenu("Options") {
        Toggle("Wireframe", isOn: $wireframe)
      }
    }
  }
}
