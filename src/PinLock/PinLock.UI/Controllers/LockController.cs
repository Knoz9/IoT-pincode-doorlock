using Microsoft.AspNetCore.Mvc;
using PinLock.UI.Models;
using PinLock.UI.Services;

namespace PinLock.UI.Controllers;
[ApiController]
public class LockController : Controller
{
    private readonly IDeviceService _deviceService;

    public LockController(IDeviceService deviceService)
    {
        _deviceService = deviceService;
    }
    [HttpGet]
    [Route("/api/lock/")]
    public async Task<PinResponse> CheckPin(string apiKey, string pin)
    {
        var err = new List<string>();
        if (apiKey == "" || pin == "")
        {
            err.Add("BadRequest");
            return new PinResponse{Errors = err};
        }
        var checkResult = await _deviceService.CheckPin(apiKey, pin);
        if (checkResult == null)
        {
            err.Add("NotAuthorized");
            return new PinResponse{Errors = err};
        }
        return checkResult;
    }

    [HttpGet]
    [Route("/api/lock/beat/")]

    public async Task<IActionResult> Beat(string apiKey)
    {
        _deviceService.Beat(apiKey);
        return BadRequest();
    }
}