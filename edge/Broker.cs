using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace edge
{
    internal class Broker
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public List<Device> Devices;

        public Broker(int id, string name)
        {
            Id = id;
            Name = name;

            Devices = new List<Device>();
        }
        public void requestTrust(Device di,Device dj)
        {
            //如何反馈信任 dj(t)？？
        }
        public override bool Equals(object obj)
        {
            Broker device = obj as Broker;
            if (Id == device.Id)
                return true;
            else
                return false;
        }
    }
}
