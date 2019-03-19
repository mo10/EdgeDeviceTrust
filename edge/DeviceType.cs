using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace edge
{
    /// <summary>
    /// 设备信任类型
    /// </summary>
    public enum DeviceType
    {
        /// <summary>
        /// good
        /// </summary>
        GOOD = 0,
        /// <summary>
        /// independent malicious
        /// </summary>
        MALICIOUS_INDEPENDENT,
        /// <summary>
        /// collective malicious
        /// </summary>
        MALICIOUS_COLLECTIVE,
        /// <summary>
        /// camouflage malicious
        /// </summary>
        MALICIOUS_CAMOUFLAGE,
        /// <summary>
        /// spies malicious
        /// </summary>
        MALICIOUS_SPIES,
    }
}
