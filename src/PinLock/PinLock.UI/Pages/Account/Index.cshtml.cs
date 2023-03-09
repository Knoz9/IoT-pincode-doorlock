using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PinLock.UI.Models;
using PinLock.UI.Services;

namespace PinLock.UI.Pages.Account;
[Authorize]
public class Index : PageModel
{
    private readonly ILogger<IndexModel> _logger;
    private readonly UserManager<IdentityUser> _userManager;
    private readonly IDeviceService _deviceService;
    public List<Device> devices { get; set; }


    public Index(ILogger<IndexModel> logger,
        UserManager<IdentityUser> userManager,
        IDeviceService deviceService)
    {
        _logger = logger;
        _userManager = userManager;
        _deviceService = deviceService;
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

        devices = _deviceService.GetDevices();
        return null;
    }
}