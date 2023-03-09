using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace PinLock.UI.Pages;

public class IndexModel : PageModel
{
    private readonly ILogger<IndexModel> _logger;
    private readonly UserManager<IdentityUser> _userManager;

    public IndexModel(ILogger<IndexModel> logger,
        UserManager<IdentityUser> userManager)
    {
        _logger = logger;
        _userManager = userManager;
    }

    public async Task<RedirectResult> OnGetAsync()
    {
        var currentUser = this.User;
        var id = _userManager.GetUserId(User);
        var user = await _userManager.GetUserAsync(User);
        if (user == null)
        {
            return Redirect("/Account/Login");
        }
        else
        {
            var isAdmin = await _userManager.IsInRoleAsync(user, "Admin");
            if (isAdmin)
            {
                return Redirect("/Admin/Index");
            }
        }
        return Redirect("/Account/Index");
    }
    
}