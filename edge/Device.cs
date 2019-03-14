using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace edge
{
    internal class Device
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public Device(int id,string name)
        {
            Id = id;
            Name = name;
        }
        public override bool Equals(object obj)
        {
            Device device = obj as Device;
            if (Id == device.Id)
                return true;
            else
                return false;
        }
        
    }
}
