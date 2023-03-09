using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace PinLock.UI.Pages.Account;

public class Login : PageModel
{
    private readonly ILogger<IndexModel> _logger;
    private readonly UserManager<IdentityUser> _userManager;
    private readonly SignInManager<IdentityUser> _signInManager;

    public Login(
        ILogger<IndexModel> logger,
        UserManager<IdentityUser> userManager,
        SignInManager<IdentityUser> signInManager)
    {
        _logger = logger;
        _userManager = userManager;
        _signInManager = signInManager;
    }
    public void OnGet()
    {
        
    }

    public async Task<IActionResult> OnPostAsync(string username, string password)
    {
        if (username == null || password == null)
        {
            return Redirect("/Account/Login");
        }
        // Login functionality
        var user = await _userManager.FindByNameAsync(username);
        
        if (user != null)
        {
            // Signin
            var result = await _signInManager.PasswordSignInAsync(user, password, false, false);
            if (result.Succeeded)
            {
                var isAdmin = await _userManager.IsInRoleAsync(user, "Admin");
                if (isAdmin)
                {
                    return Redirect("/Admin/Index");

                }
                return Redirect("/Account");
            }
        }
        return Redirect("/Index");
    }
}