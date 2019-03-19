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
        public DeviceType Type { get; set; }
        /// <summary>
        /// the probability of rating honestly
        /// </summary>
        public double RHonest { get; set; }
        /// <summary>
        /// the probability of honestly providing good file
        /// </summary>
        public double PHonest { get; set; }
        public Device(int id,string name)
        {
            Id = id;
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
