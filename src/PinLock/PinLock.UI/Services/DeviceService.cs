using Microsoft.EntityFrameworkCore;
using PinLock.UI.Data;
using PinLock.UI.Helpers;
using PinLock.UI.Models;

namespace PinLock.UI.Services;

public class DeviceService : IDeviceService
{
    private readonly AppDbContext _db;

    public DeviceService(AppDbContext db)
    {
        _db = db;
    }
    public List<Device> GetDevices()
    {
        var devices = _db.Devices.ToList();
        return devices;
    }

    public Device GetDeviceById(int id)
    {
        var device = _db.Devices.FirstOrDefault(d => d.Id == id);

        if (device != null) return device;
        return null;
    }

    public async Task<bool> ChangePin(int id, string pin)
    {
        if (pin.Length != 4)
        {
            return false;
        }
        if (!Int32.TryParse(pin, out int i))
        {
            return false;
        }
        
        var device = _db.Devices.FirstOrDefault(d => d.Id == id);
        if (device != null)
        {
            device.NextPin = pin;
            device.Expire = DateTime.UtcNow;
        }

        await _db.SaveChangesAsync();
        return true;
    }

    public async Task<Device> CreateDevice(string des, DateTime defaultExpire)
    {
        var device = Generators.GenerateDevice(des, defaultExpire);
        
        await _db.Devices.AddAsync(device);
        await _db.SaveChangesAsync();
        return device;
    }
    public async Task<bool> UpdateDevice(int id, string des)
    {
        if (des == "")
        {
            return false;
        }
        var device = _db.Devices.FirstOrDefault(d => d.Id == id);
        if (device != null)
        {
            device.Description = des;
        }
        await _db.SaveChangesAsync();
        return true;
    }

    public async Task<bool> RemoveDevice(int id)
    {
        var device = _db.Devices.FirstOrDefault(d => d.Id == id);
        if (device != null)
        {
            var result = _db.Devices.Remove(device);
            await _db.SaveChangesAsync();
            return true;
        }

        return false;
    }

    public async Task<string> SetNext(int id)
    {
        var newPin = Generators.GeneratePin();
        var newCurrent = "";
        var device = _db.Devices.FirstOrDefault(d => d.Id == id);
        if (device != null)
        {
            device.CurrentPin = device.NextPin;
            device.NextPin = newPin;
            device.Expire = DateTime.UtcNow.AddTicks(device.DefaultExpire.Ticks);
            newCurrent = device.CurrentPin;
        }
        await _db.SaveChangesAsync();
        return newCurrent;
    }

    public async Task<DateTime> GetExpiry(int id)
    {
        var device = _db.Devices.FirstOrDefault(d => d.Id == id);
        if (device != null)
        {
            return device.Expire;
        }

        return DateTime.MinValue;
    }

 

    public async Task<PinResponse> CheckPin(string apiKey, string pin)
    {
        var device = _db.Devices.FirstOrDefault(d => d.ApiKey == apiKey);
        if (device == null)
        {
            // NOT AUTH
            return null;
        }

        var authorized = pin == device.CurrentPin ? true : false;
        var exp = DateTime.UtcNow.CompareTo(device.Expire);
        
        if (exp >= 0) // If expired
        {
            await SetNext(device.Id);
            device = _db.Devices.FirstOrDefault(d => d.ApiKey == apiKey);
        }
        var response = new PinResponse
        {
            Authorized = authorized,
            CurrentPin = device.CurrentPin,
            Expire = device.Expire
        };
        return response;
        
    }

    public async Task Beat(string apiKey)
    {
        var device = _db.Devices.FirstOrDefault(d => d.ApiKey == apiKey);
        if (device == null || device.ApiKey != apiKey)
        {
            return;
        }
        device.Heartbeat = DateTime.UtcNow;
        await _db.SaveChangesAsync();

    }
}