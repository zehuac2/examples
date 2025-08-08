using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Forms.Pages
{
	public class AddAndDelete : PageModel
    {
        public class Person : ICloneable
        {
            private readonly static SemaphoreSlim _nextIdSemaphore = new(1);
            private static int _nextId = 0;

            public static async ValueTask<int> GetNewID()
            {
                await _nextIdSemaphore.WaitAsync();

                int nextId = _nextId++;

                _nextIdSemaphore.Release();

                return nextId;
            }

            public int ID { get; set; } = 0;
            
            [Required]
            public string Name { get; set; } = "test";

            [Required]
            [Range(1, 150)]
            public int Age { get; set; } = 1;

            // Initialize to false to demonstrate hidden input
            [Required]
            public bool IsAlive { get; set; } = false;

            public object Clone()
            {
                return new Person()
                {
                    ID = ID,
                    Name = Name,
                    Age = Age,
                    IsAlive = IsAlive,
                };
            }

            public override string ToString()
            {
                return $"Person(Name={Name}, Age={Age}, IsAlive={IsAlive})";
            }
        }

        public sealed class Database: IDisposable
        {
            public IReadOnlyList<Person> People
            {
                get
                {
                    return _people;
                }
            }

            private readonly SemaphoreSlim _semaphore = new(1);
            private readonly List<Person> _people = new();

            public async ValueTask AddPerson(Person person)
            {
                await _semaphore.WaitAsync();

                _people.Add(person);

                _semaphore.Release();
            }

            public async ValueTask DeletePerson(int id)
            {
                await _semaphore.WaitAsync();

                _people.RemoveAll(person => person.ID == id);

                _semaphore.Release();
            }

            public void Dispose()
            {
                _semaphore.Dispose();
            }
        }

        public bool IsAdditionSuccessful { get; set; } = false;

        [BindProperty]
        public Person NewPerson { get; set; } = new();

        public IReadOnlyList<Person> People
        {
            get
            {
                return _database.People;
            }
        }

        [BindProperty]
        [Required]
        public string PersonIdToDelete { get; set; } = "";

        private readonly Database _database;

        public AddAndDelete(Database database)
        {
            _database = database;
        }

        public void OnGet()
        {
        }

        public async Task<IActionResult> OnPostCreatePerson()
        {
            Reset();

            if (!TryValidateModel(NewPerson, nameof(NewPerson)))
            {
                return Page();
            }

            NewPerson.ID = await Person.GetNewID();

            await _database.AddPerson((Person) NewPerson.Clone());
            IsAdditionSuccessful = true;

            return Page();
        }

        public async Task<IActionResult> OnPostDeletePerson(int id)
        {
            await _database.DeletePerson(id);
            return Page();
        }

        private void Reset()
        {
            ModelState.Clear();

            IsAdditionSuccessful = false;
        }
    }
}
