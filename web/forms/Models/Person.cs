using System;
using System.ComponentModel.DataAnnotations;

namespace Forms.Models;

public class Person : ICloneable
{
    [Required]
    public string Name { get; set; } = "";

    [Required]
    [Range(1, 150)]
    public int Age { get; set; } = 0;

    [Required]
    public bool IsAlive { get; set; } = false;

    public object Clone()
    {
        return new Person()
        {
            Name = Name,
            Age = Age,
        };
    }

    public override string ToString()
    {
        return $"Person(Name={Name}, Age={Age}, IsAlive={IsAlive})";
    }
}