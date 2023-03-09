//
//  MeshRenderer.swift
//  BasicRendering
//
//  Created by Zehua Chen on 5/23/21.
//

import GameplayKit
import Metal
import MetalKit
import ModelIO
import SampleKit

final class MeshRenderer: GKComponent {
  var mesh: MDLMesh?
  var renderPipeline: RenderPipeline?
  var wireframe: Bool = false

  fileprivate var _transform: Transform?

  required init?(coder: NSCoder) {
    super.init(coder: coder)
  }

  init(mesh: MDLMesh?, renderPipeline: RenderPipeline?, drawWireframe: Bool) {
    super.init()

    self.mesh = mesh
    self.renderPipeline = renderPipeline
    self.wireframe = drawWireframe
  }

  override func didAddToEntity() {
    super.didAddToEntity()

    _transform = entity?.component(ofType: Transform.self)
  }

  override func update(deltaTime seconds: TimeInterval) {
    super.update(deltaTime: seconds)

    guard let transform = _transform else { return }
    guard let mesh = self.mesh else { return }
    guard let submeshes = mesh.submeshes else { return }
    guard let renderPipeline = self.renderPipeline else { return }

    let encoder = renderPipeline.commandEncoder

    _setTransform(transform.matrix, encoder: encoder)
    _setBuffer(for: mesh, transform: transform.matrix, encoder: encoder)

    for i in 0..<submeshes.count {
      _drawSubmesh(submeshes.object(at: i) as! MDLSubmesh, encoder: encoder)
    }
  }

  fileprivate func _setTransform(_ transform: float4x4, encoder: MTLRenderCommandEncoder) {
    encoder.setVertexBytes(
      [transform], length: MemoryLayout<float4x4>.size, index: Int(SHADER_INDEX_TRANSFORM))
  }

  fileprivate func _setBuffer(
    for mesh: MDLMesh, transform: float4x4, encoder: MTLRenderCommandEncoder
  ) {
    guard let positionAttr = mesh.vertexDescriptor.attributeNamed(MDLVertexAttributePosition) else {
      return
    }

    let buffer = mesh.vertexBuffers[positionAttr.bufferIndex] as! MTKMeshBuffer

    encoder.setVertexBuffer(buffer.buffer, offset: 0, index: Int(SHADER_INDEX_POSITION))
  }

  fileprivate func _drawSubmesh(_ submesh: MDLSubmesh, encoder: MTLRenderCommandEncoder) {
    encoder.drawIndexedPrimitives(
      type: wireframe ? .lineStrip : .triangle,
      indexCount: submesh.indexCount,
      indexType: MTLIndexType(submesh.indexType),
      indexBuffer: (submesh.indexBuffer as! MTKMeshBuffer).buffer,
      indexBufferOffset: 0)
  }
}
