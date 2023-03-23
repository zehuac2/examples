using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace Algorithms.Graph
{
    public class DirectedGraph<TVertex, TEdge> :
        IEnumerable<TVertex>,
        IEquatable<DirectedGraph<TVertex, TEdge>>,
        ICloneable
    {
        struct VertexData: IEquatable<VertexData>
        {
            public Dictionary<TVertex, TEdge> Outs;
            public Dictionary<TVertex, TEdge> Ins;

            public static VertexData Default()
            {
                return new VertexData()
                {
                    Outs = new Dictionary<TVertex, TEdge>(),
                    Ins = new Dictionary<TVertex, TEdge>(),
                };
            }

            public bool Equals(VertexData other)
            {
                bool @out = this.Outs.All((KeyValuePair<TVertex, TEdge> pair) =>
                {
                    if (!other.Outs.ContainsKey(pair.Key))
                    {
                        return false;
                    }

                    return pair.Value.Equals(other.Outs[pair.Key]);
                });

                bool @in = this.Ins.All((KeyValuePair<TVertex, TEdge> pair) =>
                {
                    if (!other.Ins.ContainsKey(pair.Key))
                    {
                        return false;
                    }

                    return pair.Value.Equals(other.Ins[pair.Key]);
                });

                return @out && @in;
            }
        }

        Dictionary<TVertex, VertexData> _dictionary = new Dictionary<TVertex, VertexData>();

        /// <summary>
        /// Get a number of vertices
        /// </summary>
        public int VertexCount => _dictionary.Count;

        public void Add(TVertex vertex)
        {
            _dictionary.Add(vertex, VertexData.Default());
        }

        public void Add(TVertex @out, TVertex @in, TEdge e)
        {
            VertexData fromVertex = _dictionary[@out];
            VertexData inVertex = _dictionary[@in];

            fromVertex.Outs.Add(@in, e);
            inVertex.Ins.Add(@out, e);

            _dictionary[@out] = fromVertex;
            _dictionary[@in] = inVertex;
        }

        public Dictionary<TVertex, TEdge> GetOuts(TVertex vertex)
        {
            return _dictionary[vertex].Outs;
        }

        public Dictionary<TVertex, TEdge> GetIns(TVertex vertex)
        {
            return _dictionary[vertex].Ins;
        }

        public bool Contains(TVertex vertex)
        {
            return _dictionary.ContainsKey(vertex);
        }

        public IEnumerator<TVertex> GetEnumerator()
        {
            foreach (var pair in _dictionary)
            {
                yield return pair.Key;
            }
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return this.GetEnumerator();
        }

        public bool Equals(DirectedGraph<TVertex, TEdge> other)
        {
            return _dictionary.All((KeyValuePair<TVertex, VertexData> pair) =>
            {
                if (!other._dictionary.ContainsKey(pair.Key))
                {
                    return false;
                }

                return pair.Value.Equals(other._dictionary[pair.Key]);
            });
        }

        public object Clone()
        {
            var copy = new DirectedGraph<TVertex, TEdge>();

            foreach (var pair in _dictionary)
            {
                var outs = new Dictionary<TVertex, TEdge>();
                var ins = new Dictionary<TVertex, TEdge>();

                foreach (var @out in pair.Value.Outs)
                {
                    outs.Add(@out.Key, @out.Value);
                }

                foreach (var @in in pair.Value.Ins)
                {
                    ins.Add(@in.Key, @in.Value);
                }

                copy._dictionary.Add(pair.Key, new VertexData()
                {
                    Outs = outs,
                    Ins = ins,
                });
            }

            return copy;
        }
    }
}
