using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;

namespace CS
{
    /// <summary>
    /// Mimic Behavior of <c>UnityEngine.Events.UnityEvent</c>
    /// </summary>
    public class UnityEvent
    {
        List<Action> _actions = new List<Action>();
        bool _invoking = false;

        List<Action> _additions = new List<Action>();
        List<Action> _removals = new List<Action>();

        public void AddListener(Action action)
        {
            if (_invoking)
            {
                _additions.Add(action);
                return;
            }

            _actions.Add(action);
        }

        public void RemoveListener(Action action)
        {
            if (_invoking)
            {
                _removals.Add(action);
                return;
            }

            _actions.Remove(action);
        }

        public void Invoke()
        {
            _invoking = true;

            foreach (var action in _actions)
            {
                action();
            }

            _invoking = false;

            foreach (var addition in _additions)
            {
                _actions.Add(addition);
            }

            foreach (var removal in _removals)
            {
                _actions.Remove(removal);
            }
        }
    }

    public struct DependencyTask<T>
    {
        public class Awaiter : INotifyCompletion
        {
            public bool IsCompleted { get; set; } = false;

            Func<T> _result;
            Action _continuation = () => { };
            UnityEvent _unityEvent;

            public Awaiter(UnityEvent unityEvent, Func<T> result)
            {
                _result = result;
                _unityEvent = unityEvent;
            }

            public void OnCompleted(Action continuation)
            {
                _continuation = continuation;
            }

            public T GetResult()
            {
                return _result();
            }

            public void Invoke()
            {
                _unityEvent.RemoveListener(this.Invoke);
                _continuation();
            }
        }

        Func<T> _result;
        UnityEvent _unityEvent;

        public DependencyTask(UnityEvent unityEvent, Func<T> result)
        {
            _unityEvent = unityEvent;
            _result = result;
        }

        public Awaiter GetAwaiter()
        {
            var awaiter = new Awaiter(_unityEvent, _result);
            _unityEvent.AddListener(awaiter.Invoke);

            return awaiter;
        }
    }

    public class Program
    {
        static async void Foo(UnityEvent unityEvent)
        {
            var task = new DependencyTask<int>(unityEvent, () => 17);

            Console.WriteLine("Before Task");
            int value = await task;

            Console.WriteLine("After Task");

            Console.WriteLine(value);
        }

        static void Main(string[] args)
        {
            UnityEvent unityEvent = new UnityEvent();
            Foo(unityEvent);

            unityEvent.Invoke();
        }
    }
}
