using System;
using System.Collections.Generic;
using System.Linq;

namespace Algorithms.Set
{
    public static class PowerSet
    {
        public static List<List<T>> GetPowerSet<T>(this IReadOnlyCollection<T> set)
        {
            List<List<T>> output = new List<List<T>>();

            if (set.Count == 0)
            {
                output.Add(new List<T>());
                return output;
            }

            T[] setCopy = set.ToArray();
            T setHead = setCopy[0];
            T[] setRest = setCopy.Skip(1).ToArray();

            foreach (List<T> powerSet in setRest.GetPowerSet())
            {
                List<T> buffer = new List<T>();
                buffer.Add(setHead);
                buffer.AddRange(powerSet);

                output.Add(buffer);
                output.Add(powerSet);
            }

            return output;
        }
    }
}
