using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PinLock.UI.Data;
using PinLock.UI.Helpers;
using PinLock.UI.Models;
using PinLock.UI.Services;

namespace PinLock.UI.Pages.Admin;
[Authorize(Roles = "Admin")]
public class Devices : PageModel
{
    private readonly IDeviceService _deviceService;

    public List<Device> devices { get; set; }

    public Devices(IDeviceService deviceService)
    {
        _deviceService = deviceService;
    }
    public async Task OnGet()
    {
        devices = _deviceService.GetDevices();
    }

    public async Task<IActionResult> OnPostAsync(string desc, string defaultExpireHours)
    {
        if (desc != "" && desc != null && defaultExpireHours != null)
        {
            if (Int32.TryParse(defaultExpireHours, out int i))
            {
                var defaultExpire = DateTime.MinValue;
                defaultExpire = defaultExpire.AddHours(i);
                var device = await _deviceService.CreateDevice(desc, defaultExpire);
                return RedirectToPage("/Admin/Devices");
            }
            return RedirectToPage("/Admin/Devices");
        }

        return RedirectToPage("/Admin/Devices");
    }

    public async Task<IActionResult> OnPostDelete(int id)
    {
        await _deviceService.RemoveDevice(id);
        return RedirectToPage("/Admin/Devices");

    }
    
    public async Task<IActionResult> OnPostEdit(int id, string desc)
    {
        if (desc == null || desc == "")
        {
            return RedirectToPage("/Admin/Devices");
        }
        await _deviceService.UpdateDevice(id, desc);
        return RedirectToPage("/Admin/Devices");

    }

    public async Task<IActionResult> OnPostNew(int id, string pin, string forcechecked)
    {
        
        if (pin == null)
        {
            return RedirectToPage("/Admin/Devices");
        }
        await _deviceService.ChangePin(id, pin);
        if (forcechecked == null)
        {
            return RedirectToPage("/Admin/Devices");
        }

        await _deviceService.SetNext(id);
        return RedirectToPage("/Admin/Devices");
    }



}