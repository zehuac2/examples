//
//  Transform.swift
//  BasicRendering
//
//  Created by Zehua Chen on 5/23/21.
//

import GameplayKit
import MetalMath
import simd

final class Transform: GKComponent {
  var scale: SIMD3<Float32> = [1, 1, 1]
  var position: SIMD3<Float32> = [0, 0, 0]

  var matrix: float4x4 {
    return .translate(position) * .scale(scale)
  }

  required init?(coder: NSCoder) {
    super.init(coder: coder)
  }

  init(scale: SIMD3<Float32>, position: SIMD3<Float32>) {
    super.init()

    self.scale = scale
    self.position = position
  }
}
