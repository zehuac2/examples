using System;
using System.Collections.Generic;

namespace NLP
{
    using FETable = Dictionary<string, Dictionary<string, float>>;

    internal static class FETableExtension
    {
        public static void InitializeDefautValue(
            this FETable matrix,
            string f,
            string e,
            float defaultValue = 0.0f)
        {
            Dictionary<string, float> row;

            if (!matrix.TryGetValue(f, out row))
            {
                row = new Dictionary<string, float>();
                matrix[f] = row;
            }

            float value;

            if (!row.TryGetValue(e, out value))
            {
                value = defaultValue;
                row[e] = value;
            }
        }
    }

    /// <summary>
    /// Word based dictionaries between two languages
    ///
    /// <example>
    /// Access the t(e|f) using "f, e", as in "given f, get probability of e"
    /// <code>
    /// dictionary[f, e]
    /// </code>
    /// </example>
    /// </summary>
    public class IBMModel1Dictionary
    {
        public FETable Table { get; private set; } = new FETable();

        public float this[string f, string e]
        {
            get
            {
                return this.Table[f][e];
            }
            set
            {
                this.Table[f][e] = value;
            }
        }

        public static IBMModel1Dictionary Train(
            TranslationTrainingData trainingData,
            int iterations = 10,
            float defaultTableValue = 1.0f)
        {
            IBMModel1Dictionary dictionary = new IBMModel1Dictionary();

            // Initialize dictionary
            foreach (string f in trainingData.FWords)
            {
                foreach (string e in trainingData.EWords)
                {
                    dictionary.Table.InitializeDefautValue(f, e, defaultTableValue);
                }
            }

            for (int iteration = 0; iteration < iterations; iteration++)
            {
                // count(e|f)
                FETable count = new FETable();
                // total(f)
                Dictionary<string, float> total = new Dictionary<string, float>();
                // s-total(e)
                Dictionary<string, float> sTotal = new Dictionary<string, float>();

                // Initialize default values
                // - count
                // - total
                foreach (string f in trainingData.FWords)
                {
                    total[f] = 0.0f;

                    foreach (string e in trainingData.EWords)
                    {
                        count.InitializeDefautValue(f, e, 0.0f);
                    }
                }

                foreach (SentencePair sentencePair in trainingData)
                {
                    // Compute normalizations
                    foreach (string e in sentencePair.EWords)
                    {
                        sTotal[e] = 0.0f;

                        foreach (string f in sentencePair.FWords)
                        {
                            sTotal[e] += dictionary[f, e];
                        }
                    }

                    // Collect counts
                    foreach (string e in sentencePair.EWords)
                    {
                        foreach (string f in sentencePair.FWords)
                        {
                            count[f][e] += dictionary[f, e] / sTotal[e];
                            total[f] += dictionary[f, e] / sTotal[e];
                        }
                    }
                }

                // Esitmate probabilities
                foreach (string f in trainingData.FWords)
                {
                    foreach (string e in trainingData.EWords)
                    {
                        dictionary[f, e] = count[f][e] / total[f];
                    }
                }
            }

            return dictionary;
        }
    }
}
