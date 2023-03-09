//
//  Camera.swift
//  BasicRendering
//
//  Created by Zehua Chen on 5/24/21.
//

import GameplayKit
import simd

class Camera: GKComponent {
  var rotation: SIMD2<Float32> = [0, 0]
  var renderPipeline: RenderPipeline?

  required init?(coder: NSCoder) {
    super.init(coder: coder)
  }

  init(rotation: SIMD2<Float32>, renderPipeline: RenderPipeline?) {
    super.init()

    self.rotation = rotation
    self.renderPipeline = renderPipeline
  }

  fileprivate var _transform: Transform?

  override func didAddToEntity() {
    _transform = entity?.component(ofType: Transform.self)
  }

  override func update(deltaTime seconds: TimeInterval) {
    super.update(deltaTime: seconds)

    guard let renderPipeline = self.renderPipeline else { return }
    guard let transform = _transform else { return }

    let position = transform.position

    let eyePoint =
      simd_float4x4.rotateY(rotation.y.radian, around: [0, 0, 0.5])
      * SIMD4<Float32>([position.x, position.y, position.z, 1])

    let lookat = simd_float4x4.look(
      at: [0, 0, 0.5],
      from: SIMD3<Float32>(eyePoint),
      up: [0, 1, 0])

    let aspect = 1 / Float32(renderPipeline.drawableSize.width / renderPipeline.drawableSize.height)

    let projection = simd_float4x4.perspective(
      fovY: Float32(90).radian,
      aspect: aspect,
      nearZ: 0.1,
      farZ: 100)

    renderPipeline.commandEncoder.setVertexBytes(
      [projection * lookat],
      length: MemoryLayout<float4x4>.size,
      index: Int(SHADER_INDEX_VIEWPROJECTION))
  }
}
