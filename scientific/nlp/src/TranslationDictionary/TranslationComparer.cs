using System;
using System.Collections.Generic;

namespace NLP
{
    class TranslationComparer : IComparer<KeyValuePair<string, float>>
    {
        public int Compare(KeyValuePair<string, float> a, KeyValuePair<string, float> b)
        {
            if (a.Value > b.Value)
            {
                return 1;
            }

            if (a.Value == b.Value)
            {
                return 0;
            }

            return -1;
        }
    }
}
