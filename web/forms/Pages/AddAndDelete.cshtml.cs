using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Forms.Pages
{
	public class AddAndDelete : PageModel
    {
        public class Person : ICloneable
        {
            private readonly static object _nextIdLock = new object();
            private static int _nextId = 0;

            public static int GetNewID()
            {
                lock(_nextIdLock)
                {
                    return _nextId++;
                }
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

        public sealed class Database
        {
            public IReadOnlyList<Person> People
            {
                get
                {
                    return _people;
                }
            }

            private readonly List<Person> _people = new();

            public void AddPerson(Person person)
            {
                lock(this)
                {
                    _people.Add(person);
                }
            }
        }

        public bool IsAdditionSuccessful { get; set; } = false;
        public bool IsDeletionSuccessful { get; set; } = false;

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

        public ActionResult OnPostCreatePerson()
        {
            Reset();

            if (!TryValidateModel(NewPerson, nameof(NewPerson)))
            {
                return Page();
            }

            NewPerson.ID = Person.GetNewID();

            _database.AddPerson((Person) NewPerson.Clone());
            IsAdditionSuccessful = true;

            return Page();
        }

        public ActionResult OnPostDeletePerson(int id)
        {
            return Redirect("./Index");
        }

        private void Reset()
        {
            ModelState.Clear();

            IsDeletionSuccessful = false;
            IsAdditionSuccessful = false;
        }
    }
}
