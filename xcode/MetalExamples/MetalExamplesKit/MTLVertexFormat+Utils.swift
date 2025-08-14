//
//  MTLVertexFormat+Utils.swift
//  SampleKit
//
//  Created by Zehua Chen on 5/21/21.
//

import Metal
import ModelIO

extension MTLVertexFormat {
  public init(_ mdl: MDLVertexFormat) {
    switch mdl {
    case .float3:
      self = .float3
    case .float2:
      self = .float2
    default:
      fatalError()
    }
  }
}
