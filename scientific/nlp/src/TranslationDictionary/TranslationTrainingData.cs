using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Reflection;

namespace NLP
{
    public struct SentencePair
    {
        public string[] EWords;
        public string[] FWords;
    }

    public class TranslationTrainingData : IEnumerable<SentencePair>
    {
        internal struct ModelPair
        {
            public string E { get; set; }
            public string F { get; set; }
        }

        internal struct Model
        {
            /// <summary>
            /// Name of the training data
            /// </summary>
            public string Name { get; set; }

            /// <summary>
            /// Array of sentence pairs
            /// </summary>
            /// <value>Data[sentence][pair]</value>
            public ModelPair[] Data { get; set; }
        }

        public string Name { get; set; }
        public List<SentencePair> Pairs { get; } = new List<SentencePair>();
        public HashSet<string> EWords { get; } = new HashSet<string>();
        public HashSet<string> FWords { get; } = new HashSet<string>();

        /// <summary>
        /// Load training data from stream
        /// </summary>
        /// <param name="stream">some kind of stream</param>
        public TranslationTrainingData(Stream stream)
        {
            using StreamReader reader = new StreamReader(stream);
            JsonSerializerOptions options = new JsonSerializerOptions()
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase
            };

            Model model = JsonSerializer.Deserialize<Model>(reader.ReadToEnd(), options);

            this.Name = model.Name;

            foreach (ModelPair pair in model.Data)
            {
                SentencePair sentencePair = new SentencePair()
                {
                    FWords = this.ToWords(pair.F),
                    EWords = this.ToWords(pair.E)
                };

                this.Add(sentencePair);
            }
        }

        public IEnumerator<SentencePair> GetEnumerator()
        {
            return Pairs.GetEnumerator();
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return Pairs.GetEnumerator();
        }

        public void Add(SentencePair pair)
        {
            foreach (string e in pair.EWords)
            {
                EWords.Add(e);
            }

            foreach (string f in pair.FWords)
            {
                FWords.Add(f);
            }

            Pairs.Add(pair);
        }

        private string[] ToWords(string sentence)
        {
            List<string> words = new List<string>();
            StringBuilder builder = new StringBuilder();

            foreach (char letter in sentence)
            {
                switch (letter)
                {
                    case ' ':
                        if (builder.Length != 0)
                        {
                            words.Add(builder.ToString());
                            builder.Clear();
                        }
                        break;
                    case '.':
                        if (builder.Length != 0)
                        {
                            words.Add(builder.ToString());
                            builder.Clear();
                        }
                        words.Add(".");
                        break;
                    default:
                        builder.Append(letter);
                        break;
                }
            }

            return words.ToArray();
        }

        public static TranslationTrainingData AlienLanguage
        {
            get
            {
                Assembly assembly = Assembly.GetAssembly(typeof(TranslationTrainingData));
                using Stream stream = assembly.GetManifestResourceStream("NLP.Data.AlienLanguage.json");

                return new TranslationTrainingData(stream);
            }
        }
    }
}
