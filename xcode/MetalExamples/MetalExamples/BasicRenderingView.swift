//
//  RenderingView.swift
//  BasicRendering
//
//  Created by Zehua Chen on 5/20/21.
//

import AppKit
import SwiftUI

struct BasicRenderingView: NSViewControllerRepresentable {
  typealias NSViewControllerType = BasicRenderingViewController

  var wireframe: Bool

  func makeNSViewController(context: Context) -> BasicRenderingViewController {
    return BasicRenderingViewController()
  }

  func updateNSViewController(_ nsViewController: BasicRenderingViewController, context: Context) {
    nsViewController.wireframe = wireframe
  }
}
