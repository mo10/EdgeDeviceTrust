using System;

namespace edge
{
    class DeviceTrust
    {
        public Device di { get; set; }
        public Device dj { get; set; }
        public int t { get; set; }
        private double rank;
        
        public DeviceTrust(Device di,Device dj,int time)
        {
            this.di = di;
            this.dj = dj;
            this.t = time;
            GenerateRank();
        }
        public void GenerateRank()
        {
            Random rd = new Random();
            int r = rd.Next(10000);
            rank = r * 0.0001;
        }
        public double GetRank()
        {
            return rank;
        }
    }
}
