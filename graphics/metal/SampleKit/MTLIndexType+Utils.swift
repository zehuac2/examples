//
//  MTLIndexType+Utils.swift
//  SampleKit
//
//  Created by Zehua Chen on 5/20/21.
//

import Metal
import ModelIO

extension MTLIndexType {
  public init(_ indexBitDepth: MDLIndexBitDepth) {
    switch indexBitDepth {
    case .uInt16:
      self = .uint16
    case .uInt32:
      self = .uint32
    default:
      fatalError()
    }
  }
}
