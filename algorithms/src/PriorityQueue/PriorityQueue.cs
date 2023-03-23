using System.Collections.Generic;

namespace Algorithms.PriorityQueue
{
    public class PriorityQueue<T, TPriority>
    {
        IComparer<TPriority> _priorityComparer;
        IComparer<T> _elementComparer;
        List<KeyValuePair<TPriority, T>> _entries = new List<KeyValuePair<TPriority, T>>();

        public int Count => _entries.Count - 1;

        int Root => 1;

        public PriorityQueue() : this(Comparer<TPriority>.Default, Comparer<T>.Default)
        {
        }

        public PriorityQueue(IComparer<TPriority> comparer, IComparer<T> elementComparer)
        {
            _elementComparer = elementComparer;
            _priorityComparer = comparer;
            _entries.Add(new KeyValuePair<TPriority, T>());
        }

        public void Add(T element, TPriority priority)
        {
            _entries.Add(new KeyValuePair<TPriority, T>(priority, element));
            this.HeapifyUp(_entries.Count - 1);
        }

        public KeyValuePair<TPriority, T> Peek()
        {
            return _entries[this.Root];
        }

        public KeyValuePair<TPriority, T> Pop()
        {
            var output = _entries[this.Root];
            this.Swap(this.Root, _entries.Count - 1);
            _entries.RemoveRange(_entries.Count - 1, 1);

            this.HeapifyDown(this.Root);

            return output;
        }

        public void Update(T element, TPriority oldPriority, TPriority newPriority)
        {
            for (int i = this.Root; i < _entries.Count; i++)
            {
                if (_elementComparer.Compare(_entries[i].Value, element) == 0)
                {
                    _entries[i] = new KeyValuePair<TPriority, T>(newPriority, _entries[i].Value);

                    if (_priorityComparer.Compare(newPriority, oldPriority) <= 0)
                    {
                        this.HeapifyUp(i);
                    }
                    else
                    {
                        this.HeapifyDown(i);
                    }

                    return;
                }
            }
        }

        int GetLeftChild(int index) => index * 2;

        int GetRightChild(int index) => index * 2 + 1;

        int GetParent(int index) => index / 2;

        TPriority GetPriority(int index) => _entries[index].Key;

        bool HasChildren(int index)
        {
            int left = this.GetLeftChild(index);
            int right = this.GetRightChild(index);
            int count = _entries.Count;

            return left < count || right < count;
        }

        int MaxPriorityChild(int index)
        {
            if (this.HasChildren(index))
            {
                int left = this.GetLeftChild(index);
                int right = this.GetRightChild(index);

                if (right < _entries.Count)
                {
                    if (_priorityComparer.Compare(this.GetPriority(left), this.GetPriority(right)) <= 0)
                    {
                        return left;
                    }

                    return right;
                }

                return left;
            }

            return 0;
        }

        void Swap(int a, int b)
        {
            var temp = _entries[a];
            _entries[a] = _entries[b];
            _entries[b] = temp;
        }

        void HeapifyUp(int index)
        {
            if (index == this.Root)
            {
                return;
            }

            int parent = this.GetParent(index);

            if (_priorityComparer.Compare(this.GetPriority(index), this.GetPriority(parent)) < 0)
            {
                this.Swap(index, parent);
                this.HeapifyUp(parent);
            }
        }

        void HeapifyDown(int index)
        {
            if (this.HasChildren(index))
            {
                int child = this.MaxPriorityChild(index);

                if (_priorityComparer.Compare(this.GetPriority(index), this.GetPriority(child)) > 0)
                {
                    this.Swap(child, index);
                    this.HeapifyDown(child);
                }
            }
        }
    }
}
