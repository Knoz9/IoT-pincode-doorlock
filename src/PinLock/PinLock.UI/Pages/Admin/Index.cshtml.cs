using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace PinLock.UI.Pages.Admin;
[Authorize(Roles = "Admin")]
public class Index : PageModel
{
    public void OnGet()
    {
        
    }
}