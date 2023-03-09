using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using PinLock.UI.Models;

namespace PinLock.UI.Data;

public class AppDbContext : IdentityDbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
        
    }

    public DbSet<Device> Devices { get; set; }
    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);
        var adminUser = new IdentityUser
        {
            Id = "009f5957-5c0a-4416-ba87-46e811092621",
            UserName = "admin",
            NormalizedUserName = "ADMIN",
            Email = null,
            NormalizedEmail = null,
            EmailConfirmed = false,
            PasswordHash = "AQAAAAEAACcQAAAAEA3NQBtfrNyInVYCDsgn+ee8Ba00ZxvaN2RUB3aazpkujfM/gh9iSVp5C3bJN5yXJQ==",
            SecurityStamp = "ZPXXQPJYE2RYIO2V2RZGMIORGWXWW4J4",
            ConcurrencyStamp = "aef8cc20-0d40-4930-af6d-1a49ab89dc23",
            PhoneNumber = null,
            PhoneNumberConfirmed = false,
            TwoFactorEnabled = false,
            LockoutEnd = null,
            LockoutEnabled = false,
            AccessFailedCount = 0


        };
        var adminRole = new IdentityRole
        {
            Id = "fa21e3e0-5ef3-4456-b1ba-a81eac277639",
            Name = "Admin",
            NormalizedName = "ADMIN",
            ConcurrencyStamp = "55a1a8c7-6275-4fa3-accd-e7622c18ae85"
        };
        var adminUserRole = new IdentityUserRole<string>
        {
            UserId = "009f5957-5c0a-4416-ba87-46e811092621",
            RoleId = "fa21e3e0-5ef3-4456-b1ba-a81eac277639"
        };
        builder.Entity<IdentityUser>().HasData(adminUser);
        builder.Entity<IdentityRole>().HasData(adminRole);
        builder.Entity<IdentityUserRole<string>>().HasData(adminUserRole);
    }
}