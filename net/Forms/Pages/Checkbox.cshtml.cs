using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Forms.Pages
{
    public class CheckboxModel : PageModel
    {
        public enum Attribute
        {
            Fast,
            Slow,
            Male,
            Female
        }

        public Attribute[] AvailableAttributes
        {
            get
            {
                return Enum.GetValues<Attribute>();
            }
        }

        public string Message
        {
            get
            {
                if (_selectedAttributes.Count == 0)
                {
                    return "Nothing selected";
                }

                return string.Join(",", _selectedAttributes);
            }
        }

        [BindProperty]
        public List<Attribute> SelectedAttributes
        {
            get
            {
                return _selectedAttributes.ToList();
            }
            set
            {
                _selectedAttributes = new HashSet<Attribute>(value);
            }
        }

        private HashSet<Attribute> _selectedAttributes = new HashSet<Attribute>();

        public void OnGet()
        {
            _selectedAttributes = new HashSet<Attribute>()
            {
                Attribute.Fast
            };
        }

        public bool IsAttributeSelected(Attribute attribute)
        {
            return _selectedAttributes.Contains(attribute);
        }

        public IActionResult OnPost()
        {
            return Page();
        }
    }
}
