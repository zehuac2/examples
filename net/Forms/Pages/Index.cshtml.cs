using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Forms.Pages;

public class IndexModel : PageModel
{
    public record struct ExamplesModel(string Url, string Name);

    public ExamplesModel[] Examples
    {
        get
        {
            return new ExamplesModel[]
            {
                new ExamplesModel("AddAndDelete", "Add and delete"),
                new ExamplesModel("Checkbox", "Checkbox"),
            };
        }
    }
    
    private readonly ILogger<IndexModel> _logger;

    public IndexModel(ILogger<IndexModel> logger)
    {
        _logger = logger;
    }

    public void OnGet()
    {
    }
}
