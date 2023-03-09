//
//  MDLMesh+Utils.swift
//  SampleKit
//
//  Created by Zehua Chen on 5/24/21.
//

import Metal
import MetalKit
import ModelIO

extension MDLMesh {
  public var positionBuffer: MTLBuffer {
    let positionAttr = self.vertexDescriptor.attributeNamed(MDLVertexAttributePosition)!
    return (self.vertexBuffers[positionAttr.bufferIndex] as! MTKMeshBuffer).buffer
  }

  public var positionFormat: MTLVertexFormat {
    let positionAttrData = self.vertexAttributeData(forAttributeNamed: MDLVertexAttributePosition)!
    return MTLVertexFormat(positionAttrData.format)
  }

  public var positionStride: Int {
    let positionAttrData = self.vertexAttributeData(forAttributeNamed: MDLVertexAttributePosition)!
    return positionAttrData.stride
  }
}
