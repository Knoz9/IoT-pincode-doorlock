using PinLock.UI.Models;

namespace PinLock.UI.Helpers;

public static class Generators
{
    public static Device GenerateDevice(string desc,DateTime defaultExpire)
    {
        
        var device = new Device
        {
            Description = desc,
            ApiKey = Guid.NewGuid().ToString(),
            CurrentPin = GeneratePin(),
            NextPin = GeneratePin(),
            Expire = DateTime.UtcNow.AddTicks(defaultExpire.Ticks),
            DefaultExpire = defaultExpire

        };
        return device;
    }

    public static string GeneratePin()
    {
        Random rnd = new Random();
        var value = "";
        for (int i = 0; i < 4; i++)
        {
            value += rnd.Next(9).ToString();
        }

        return value;
    }
}