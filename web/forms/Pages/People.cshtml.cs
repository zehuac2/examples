using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Forms.Models;

namespace Forms.Pages
{
	public class PeopleModel : PageModel
    {
        private ILogger<PeopleModel> _logger;

        public bool IsAdditionSuccessful { get; set; } = false;
        public bool IsDeletionSuccessful { get; set; } = false;

        [BindProperty]
        public Person NewPerson { get; set; } = new();

        [BindProperty]
        [Required]
        public string PersonIdToDelete { get; set; } = "";

        public PeopleModel(ILogger<PeopleModel> logger)
        {
            _logger = logger;
        }

        public void OnGet()
        {
        }

        public ActionResult OnPostPerson()
        {
            Reset();

            if (!TryValidateModel(NewPerson, nameof(NewPerson)))
            {
                return Page();
            }

            _logger.LogInformation(NewPerson.ToString());
            IsAdditionSuccessful = true;

            return Page();
        }

        public ActionResult OnPostDeletePerson()
        {
            Reset();

            if (PersonIdToDelete == null)
            {
                ModelState.TryAddModelError(nameof(PersonIdToDelete), "Person Id cannot be empty");
                return Page();
            }

            if (!TryValidateModel(PersonIdToDelete, nameof(PersonIdToDelete)))
            {
                return Page();
            }

            _logger.LogInformation($"Person with id {PersonIdToDelete} deleted");
            IsDeletionSuccessful = true;

            return Page();
        }

        private void Reset()
        {
            ModelState.Clear();

            IsDeletionSuccessful = false;
            IsAdditionSuccessful = false;
        }
    }
}
