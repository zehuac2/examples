//
//  BasicRenderingViewController.swift
//  BasicRendering
//
//  Created by Zehua Chen on 5/20/21.
//

import AppKit
import Foundation
import GameplayKit
import Metal
import MetalKit
import MetalMath
import SampleKit

extension simd_float4x4 {
  @inlinable
  static func _look(at target: SIMD3<Float32>, from eye: SIMD3<Float32>, up: SIMD3<Float32>) -> Self
  {
    let zaxis = normalize(target - eye)
    let xaxis = normalize(cross(zaxis, up))
    let yaxis = cross(zaxis, xaxis)

    return simd_float4x4(rows: [
      [xaxis.x, xaxis.y, xaxis.z, -eye.x],
      [yaxis.x, yaxis.y, yaxis.z, -eye.y],
      [zaxis.x, zaxis.y, zaxis.z, -eye.z],
      [0, 0, 0, 1],
    ])
  }
}

class BasicRenderingViewController: NSViewController, MTKViewDelegate {
  var wireframe: Bool = false
  var device: MTLDevice!
  var mtkView: MTKView!

  var _rendererPipeline: RenderPipeline!
  var _camera: Camera!
  var _meshRenderer: MeshRenderer!
  var _entities: [GKEntity] = []

  override func loadView() {
    mtkView = MTKView()
    mtkView.device = MTLCreateSystemDefaultDevice()
    mtkView.delegate = self
    mtkView.depthStencilPixelFormat = .depth32Float
    mtkView.clearDepth = 1.0

    view = mtkView

    device = mtkView.device
  }

  override func viewDidLoad() {
    super.viewDidLoad()

    let allocator = MTKMeshBufferAllocator(device: device)
    let mesh = MDLMesh.newBox(
      withDimensions: [1, 1, 1], segments: [1, 1, 1], geometryType: .triangles,
      inwardNormals: false, allocator: allocator)

    _rendererPipeline = RenderPipeline(mtkView: mtkView, mesh: mesh)

    let cameraEntity = GKEntity()
    cameraEntity.addComponent(Transform(scale: [1, 1, 1], position: [0, 0, 0]))
    _camera = Camera(rotation: [0, 0], renderPipeline: _rendererPipeline)
    cameraEntity.addComponent(_camera)

    _entities.append(cameraEntity)

    let meshEntity = GKEntity()
    meshEntity.addComponent(Transform(scale: [0.4, 0.4, 0.4], position: [0, 0, 0.5]))

    _meshRenderer = MeshRenderer(
      mesh: mesh, renderPipeline: _rendererPipeline, drawWireframe: wireframe)
    meshEntity.addComponent(_meshRenderer)

    _entities.append(meshEntity)
  }

  override func mouseDragged(with event: NSEvent) {
    super.mouseDragged(with: event)

    _camera.rotation.x += Float32(event.deltaY)
    _camera.rotation.y += Float32(event.deltaX)

    _camera.rotation.x = Float32(CGFloat(_camera.rotation.x).truncatingRemainder(dividingBy: 360))
    _camera.rotation.y = Float32(CGFloat(_camera.rotation.y).truncatingRemainder(dividingBy: 360))
  }

  func draw(in view: MTKView) {
    _meshRenderer.wireframe = wireframe
    _rendererPipeline.beginFrame(mtkView: mtkView)

    for entity in _entities {
      entity.update(deltaTime: 0)
    }

    _rendererPipeline.endFrame(mtkView: mtkView)
  }

  func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {
    _rendererPipeline.drawableSize = size
  }
}
