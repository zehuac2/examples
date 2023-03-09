//
//  BasicRenderingApp.swift
//  BasicRendering
//
//  Created by Zehua Chen on 5/20/21.
//

import AppKit
import SwiftUI

class AppDelegate: NSObject, NSApplicationDelegate {
  func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
    return true
  }
}

@main
struct BasicRenderingApp: App {
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
