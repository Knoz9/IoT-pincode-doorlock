namespace PinLock.UI.Models;

public class PinResponse
{
    public bool Authorized { get; set; }
    public string CurrentPin { get; set; }
    public DateTime Expire { get; set; }
    public List<string>? Errors { get; set; }
}