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
        /// 求熵
        /// </summary>
        /// <param name="vs">数据集合</param>
        /// <param name="cols">列数</param>
        /// <param name="rows">行数</param>
        /// <returns>Ei</returns>
        public static double[] CalcShang(double[,] vs,int cols,int rows)
        {
            double[] H = new double[cols];
            double K = 1 / Math.Log(rows);

            for(int i = 0; i < cols; i++)
            {
                double temp = 0.00;
                for(int j = 0; j < rows; j++)
                {
                    double f = vs[j, i] / Sum(Transpose(vs, i, rows));
                    if (f > 0)
                        temp += f * Math.Log(f);
                }
                H[i] = (-K) * temp;
            }
            return H;
        }
        /// <summary>
        /// 集合转置
        /// </summary>
        /// <param name="matrix">集合</param>
        /// <param name="col">列定位</param>
        /// <param name="rows">总行数</param>
        /// <returns>返回指定列转置数组</returns>
        public static double[] Transpose(double[,] matrix,int col,int rows)
        {
            List<double> arr = new List<double>();
            for (int i = 0; i < rows; i++)
            {
                arr.Add(matrix[i, col]);
            }
            
            return arr.ToArray();
        }
        /// <summary>
        /// 集合求和
        /// </summary>
        /// <param name="set">集合</param>
        /// <returns>和</returns>
        public static double Sum(double[] set)
        {
            double sum = 0.00;
            foreach(double num in set)
            {
                sum += num;
            }
            return sum;
        }
        public static void DumpArray<T>(T[,] set,int cols, int rows)
        {
            Console.WriteLine("当前数据集");
            for (int i = 0; i < rows; i++)
            {
                for(int j = 0; j < cols; j++)
                {
                    Console.Write($"{set[i,j]:0.0000} ");
                }
                Console.WriteLine();
            }
            Console.WriteLine("-----------------------------------------------------------------");
        }

        static void Main(string[] args)
        {
            int deviceCount = 1000;
            //生成一个大小为 deviceCount * deviceCount 个的设备信任集合;
            List<DeviceTrust> DeviceTrustSet = GenDeviceTrustSet(deviceCount, 20);
            //通过 DeviceTrustSet 计算 Pij 集合
            List<double> PijSet = CalcPSet(DeviceTrustSet);

            double[,] t =
            {
                {1.00, 0.00, 1.00, 0.00,0.50,1.00,1.00,1.00,1.00},
                {1.00, 1.00, 0.00, 1.00,0.50,1.00,1.00,1.00,1.00},
                {0.00, 1.00, 0.33, 1.00,0.50,1.00,1.00,1.00,1.00},
                {1.00, 1.00, 0.00, 1.00,0.50,1.00,0.87,1.00,1.00},
                {1.00, 0.00, 1.00, 1.00,1.00,0.00,1.00,1.00,0.00},
                {1.00, 1.00, 1.00, 1.00,0.50,1.00,1.00,0.00,1.00},
                {1.00, 1.00, 0.00, 1.00,0.50,1.00,0.00,1.00,1.00},
                {0.50, 1.00, 0.33, 1.00,1.00,1.00,1.00,1.00,1.00},
                {1.00, 1.00, 0.67, 1.00,0.00,1.00,1.00,1.00,1.00},
                {1.00, 0.00, 1.00, 1.00,1.00,1.00,1.00,1.00,1.00},
                {1.00, 1.00, 0.67, 1.00,0.50,1.00,1.00,1.00,1.00},
            };
            double[,] t2 =
            {
                {0.4922, 0.4516, 0.5159, 0.1294, 0.6565, 0.3395, 0.1083, 0.6306, 0.2860},
                {0.4442, 0.3552, 0.6315, 0.1410, 0.5303, 0.6156, 0.2567, 0.5291, 0.6142},
                {0.5078, 0.0088, 0.1901, 0.5485, 0.2547, 0.1209, 0.3843, 0.1162, 0.0270},
                {0.1814, 0.2505, 0.2671, 0.2392, 0.3224, 0.1732, 0.1350, 0.3689, 0.1894},
                {0.3020, 0.5002, 0.3686, 0.4515, 0.3435, 0.2784, 0.0015, 0.3694, 0.3858},
                {0.2170, 0.5484, 0.3217, 0.4128, 0.2662, 0.3844, 0.6157, 0.3063, 0.3520},

            };
            //List<double> ts = new List<double>(t);
            //for(int i = 0; i < 9; i++)
            //{
            //    var a = CalcE(ts, 11,9,i);
            //    Console.WriteLine($"E{i}={a:00.00} ");
            //}
            DumpArray(t2, 9, 6);
            double[] ts = CalcShang(t2, 9, 6);
            foreach (double d in ts)
                Console.Write($"{d:0.0000} ");
            Console.ReadKey();
        }
    }
}
