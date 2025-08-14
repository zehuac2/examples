//
//  basic_rendering.metal
//  BasicRendering
//
//  Created by Zehua Chen on 5/20/21.
//

#include <metal_stdlib>
#include "shader_constants.h"

using namespace metal;

struct vertex_in {
  float3 position [[attribute(SHADER_ATTRIBUTE_POSITION)]];
};

struct vertex_out {
  float4 position [[position]];
  float4 color;
};

[[vertex]] vertex_out vertex_func(
    vertex_in input [[stage_in]],
    uint vertex_id [[vertex_id]],
    constant float4x4 *transform [[buffer(SHADER_INDEX_TRANSFORM)]],
    constant float4x4 *view_projection [[buffer(SHADER_INDEX_VIEWPROJECTION)]]) {
  vertex_out output;
  output.color = float4(input.position, 1.0f);
  output.position = view_projection[0] * transform[0] * float4(input.position, 1.0f);

  return output;
}

[[fragment]] float4 fragment_func(vertex_out input [[stage_in]]) {
  return normalize(input.color);
}
