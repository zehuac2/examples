using System;
using System.Collections.Generic;
using System.Linq;

namespace NLP
{
    class Program
    {
        static void Main(string[] args)
        {
            TranslationTrainingData trainingData = TranslationTrainingData.AlienLanguage;
            IBMModel1Dictionary dictionary = IBMModel1Dictionary.Train(trainingData, 20);

            foreach (string f in trainingData.FWords)
            {
                KeyValuePair<string, float>[] translations = dictionary.Table[f]
                    .Select((pair, index) => { return pair; })
                    .ToArray();

                TranslationComparer comparer = new TranslationComparer();

                Array.Sort(translations, comparer);
                Array.Reverse(translations);

                IEnumerable<string> bestTranslations = translations
                    .Take(3)
                    .Select((pair, index) => $"{pair.Key}({pair.Value:0.00})");

                Console.WriteLine("(f = {0}): {1}",
                    f,
                    string.Join(", ", bestTranslations));
            }
        }
    }
}
