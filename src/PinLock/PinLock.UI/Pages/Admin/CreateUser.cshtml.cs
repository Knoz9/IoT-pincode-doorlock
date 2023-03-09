using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace PinLock.UI.Pages.Admin;
[Authorize(Roles = "Admin")]
public class CreateUser : PageModel
{
    private readonly ILogger<IndexModel> _logger;
    private readonly UserManager<IdentityUser> _userManager;
    public IQueryable<IdentityUser> users;

    public CreateUser(
        ILogger<IndexModel> logger,
        UserManager<IdentityUser> userManager)
    {
        _logger = logger;
        _userManager = userManager;
    }
    public void OnGet()
    {
        users = _userManager.Users;
    }

    public async Task<IActionResult> OnPostDelete(string id)
    {
        var user = _userManager.Users.FirstOrDefault(user => user.Id == id);
        if (user != null)
        {
            if (user.NormalizedUserName == "ADMIN")
            {
                return Redirect("/Admin/CreateUser");
            }

            await _userManager.DeleteAsync(user);
        }
        return Redirect("/Admin/CreateUser");
    }
    public async Task<IActionResult> OnPostAsync(string username, string password)
    {
        // Register functionality

        if (username == null || username == "")
        {
            return Redirect("/Admin/CreateUser");
        }
        if (password == null || password == "")
        {
            
            return Redirect("/Admin/CreateUser");
        }
        

        var user = new IdentityUser
        {
            UserName = username
        };
        
        var result = await _userManager.CreateAsync(user, password);
        
        if (result.Succeeded)
        {
            _logger.LogWarning("Registered!");
        }

        return Redirect("/Admin/CreateUser");
    }
}