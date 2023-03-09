using PinLock.UI.Models;

namespace PinLock.UI.Services;

public interface IDeviceService
{
    List<Device> GetDevices();
    Device GetDeviceById(int id);
    Task<bool> ChangePin(int id, string pin);

    Task<Device> CreateDevice(string des,DateTime defaultExpire);
    Task<bool> UpdateDevice(int id,string des);
    Task<bool> RemoveDevice(int id);
    Task<string> SetNext(int id);
    Task<DateTime> GetExpiry(int id);

    Task<PinResponse> CheckPin(string apiKey, string pin);

    Task Beat(string apiKey);
}