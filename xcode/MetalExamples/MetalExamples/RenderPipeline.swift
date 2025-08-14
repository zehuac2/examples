//
//  Renderer.swift
//  BasicRendering
//
//  Created by Zehua Chen on 5/24/21.
//

import Metal
import MetalKit

private func _createVertexDescriptor(for mesh: MDLMesh) -> MTLVertexDescriptor {
  let vertexDesc = MTLVertexDescriptor()
  let positionAttr = MTLVertexAttributeDescriptor()
  positionAttr.format = mesh.positionFormat
  positionAttr.bufferIndex = Int(SHADER_INDEX_POSITION)
  positionAttr.offset = 0

  vertexDesc.attributes[Int(SHADER_ATTRIBUTE_POSITION)] = positionAttr

  let positionLayout = MTLVertexBufferLayoutDescriptor()
  positionLayout.stride = mesh.positionStride

  vertexDesc.layouts[Int(SHADER_ATTRIBUTE_POSITION)] = positionLayout

  return vertexDesc
}

class RenderPipeline {
  var device: MTLDevice
  var commandEncoder: MTLRenderCommandEncoder { _commandEncoder }
  var drawableSize: CGSize

  fileprivate var _depthStencilState: MTLDepthStencilState
  fileprivate var _commandQueue: MTLCommandQueue
  fileprivate var _pipelineState: MTLRenderPipelineState

  fileprivate var _commandBuffer: MTLCommandBuffer!
  fileprivate var _commandEncoder: MTLRenderCommandEncoder!

  init?(mtkView: MTKView, mesh: MDLMesh) {
    self.device = mtkView.device!
    drawableSize = mtkView.drawableSize

    let renderPipelineDesc = MTLRenderPipelineDescriptor()

    let library = device.makeDefaultLibrary()!
    let vertexFunction = library.makeFunction(name: "vertex_func")!

    let fragmentFunction = library.makeFunction(name: "fragment_func")!

    renderPipelineDesc.vertexFunction = vertexFunction
    renderPipelineDesc.fragmentFunction = fragmentFunction

    renderPipelineDesc.vertexDescriptor = _createVertexDescriptor(for: mesh)
    renderPipelineDesc.colorAttachments[0].pixelFormat = mtkView.colorPixelFormat

    renderPipelineDesc.depthAttachmentPixelFormat = mtkView.depthStencilPixelFormat

    _pipelineState = try! device.makeRenderPipelineState(descriptor: renderPipelineDesc)

    _commandQueue = device.makeCommandQueue()!

    mtkView.clearColor = MTLClearColor(red: 0, green: 0, blue: 0, alpha: 1)

    let depthDesc = MTLDepthStencilDescriptor()
    depthDesc.depthCompareFunction = .lessEqual
    depthDesc.isDepthWriteEnabled = true

    _depthStencilState = device.makeDepthStencilState(descriptor: depthDesc)!
  }

  func beginFrame(mtkView: MTKView) {
    _commandBuffer = _commandQueue.makeCommandBuffer()!
    _commandEncoder =
      _commandBuffer.makeRenderCommandEncoder(descriptor: mtkView.currentRenderPassDescriptor!)!

    _commandEncoder.setRenderPipelineState(_pipelineState)
    _commandEncoder.setDepthStencilState(_depthStencilState)
  }

  func endFrame(mtkView: MTKView) {
    _commandEncoder.endEncoding()

    _commandBuffer.present(mtkView.currentDrawable!)
    _commandBuffer.commit()
  }
}
