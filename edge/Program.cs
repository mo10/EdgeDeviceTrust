using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace edge
{
    class Program
    {
        /// <summary>
        /// 生成设备信任集合
        /// </summary>
        /// <param name="size">设备数量</param>
        /// <param name="time">时间</param>
        /// <returns>设备信任集合</returns>
        public static List<DeviceTrust> GenDeviceTrustSet(int size,int time)
        {
            List<DeviceTrust> dts = new List<DeviceTrust>();
            List<Device> ds = new List<Device>();

            //生成设备
            for(int i = 0; i < size; i++)
                ds.Add(new Device(i, $"Device {i}"));
            // 生成fbk->dj(t)
            for (int i = 0; i < size; i++)
                for (int j = 0; j < size; j++)
                    dts.Add(new DeviceTrust(ds[i], ds[j], time));
            return dts;
        }
        /// <summary>
        /// 计算Pij
        /// </summary>
        /// <param name="dts">设备信任集合</param>
        /// <returns>Pij集合</returns>
        public static List<double> CalcPSet(List<DeviceTrust> dts)
        {
            List<double> ps = new List<double>();
            double TrustSUM = 0;
            // 计算∑^n i = Ddi,Ddj(t)
            foreach (DeviceTrust dt in dts)
                TrustSUM += dt.GetRank();
            // 计算Pij
            foreach (DeviceTrust dt in dts)
                ps.Add(dt.GetRank() / TrustSUM);

            return ps;
        }
        /// <summary>
        /// 计算Ei
        /// </summary>
        /// <param name="ps">Pij的集合</param>
        /// <param name="i">列</param>
        /// <param name="j">行</param>
        /// <param name="offset">列偏移量</param>
        /// <returns>Ei</returns>
        public static double CalcE(List<double> ps,int i,int j,int offset)
        {
            double PSUM = 0;
            //求和
            for(int ii=0; ii < i; ii++)
            {
                double p = ps[offset+ii*j]; // 获取Pij 4是目前钦定
                Console.Write($"{p:0.00} ");
                if (p == 0)
                    continue;// 如果Pij=0则跳过本次计算
                else
                    PSUM += p * Math.Log(p, Math.E);
            }
            Console.Write($"SUM={PSUM:00.00}\t");
            //计算Ei
            //double e = PSUM / (0.00 - Math.Pow(Math.Log(n, Math.E), -1));

            double e = 0.00 - PSUM / Math.Log(4, Math.E);
            return e;
        }

        static void Main(string[] args)
        {
            int deviceCount = 1000;
            //生成一个大小为 deviceCount * deviceCount 个的设备信任集合;
            List<DeviceTrust> DeviceTrustSet = GenDeviceTrustSet(deviceCount, 20);
            //通过 DeviceTrustSet 计算 Pij 集合
            List<double> PijSet = CalcPSet(DeviceTrustSet);

            double[] t =
            {
                1.00, 0.00, 1.00, 0.00,0.50,1.00,1.00,1.00,1.00,
                1.00, 1.00, 0.00, 1.00,0.50,1.00,1.00,1.00,1.00,
                0.00, 1.00, 0.33, 1.00,0.50,1.00,1.00,1.00,1.00,
                1.00, 1.00, 0.00, 1.00,0.50,1.00,0.87,1.00,1.00,
                1.00, 0.00, 1.00, 1.00,1.00,0.00,1.00,1.00,0.00,
                1.00, 1.00, 1.00, 1.00,0.50,1.00,1.00,0.00,1.00,
                1.00, 1.00, 0.00, 1.00,0.50,1.00,0.00,1.00,1.00,
                0.50, 1.00, 0.33, 1.00,1.00,1.00,1.00,1.00,1.00,
                1.00, 1.00, 0.67, 1.00,0.00,1.00,1.00,1.00,1.00,
                1.00, 0.00, 1.00, 1.00,1.00,1.00,1.00,1.00,1.00,
                1.00, 1.00, 0.67, 1.00,0.50,1.00,1.00,1.00,1.00,
            };
            List<double> ts = new List<double>(t);
            for(int i = 0; i < 9; i++)
            {
                var a = CalcE(ts, 11,9,i);
                Console.WriteLine($"E{i}={a:00.00} ");
            }
            
            Console.ReadKey();
        }
    }
}
