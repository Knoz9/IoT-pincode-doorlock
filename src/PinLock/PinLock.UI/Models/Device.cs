using System.ComponentModel;

namespace PinLock.UI.Models;

public class Device
{
    
    public int Id { get; set; }
    public string Description { get; set; }
    public string ApiKey { get; set; }
    public DateTime Heartbeat { get; set; }
    
    public string CurrentPin { get; set; }
    public DateTime Expire { get; set; }
    public DateTime DefaultExpire { get; set; }
    public string NextPin { get; set; }
}