using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace edge
{
    public static class Util
    {
        
        /// <summary>
        /// 从集合里随机抽取一个对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="ts">对象集合</param>
        /// <returns>随机抽取的对象</returns>
        public static T RandomGet<T>(List<T> ts)
        {
            if (ts.Count > 1)
            {
                Random rd = new Random();
                var r = rd.Next(0, ts.Count);
                return ts[r];
            }
            return ts[0];
        }
        /// <summary>
        /// 从集合里随机抽取一个对象，不含tn
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="ts">对象集合</param>
        /// <param name="tn">需要忽略的对象</param>
        /// <returns>随机抽取的对象</returns>
        public static T RandomGet<T>(List<T> ts, T tn)
        {
            if (ts.Count > 1)
            {
                Random rd = new Random();
                while (true)
                {
                    var r = rd.Next(0, ts.Count);
                    if (ts[r].Equals(tn))
                        continue;
                    else
                        return ts[r];
                }
            }
            return ts[0];
        }
    }
}
