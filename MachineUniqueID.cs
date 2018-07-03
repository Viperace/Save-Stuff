using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Management;
using System.Net.NetworkInformation;

namespace Shadowsocks.UserLogin
{

    public class MachineUniqueID
    {
        /// <summary>
        /// Return unique key.
        ///  If there is error in finding the key, will return 0
        ///  
        /// For more info on extracting entire system. Refer to project in
        /// https://www.codeproject.com/Articles/17973/How-To-Get-Hardware-Information-CPU-ID-MainBoard-I
        /// </summary>
        /// <returns></returns>
        public static string GetUniqueID()
        {
            ManagementObjectSearcher searcher = new ManagementObjectSearcher("root\\CIMV2", "SELECT * FROM Win32_Processor");

            // Chain different architecture into one
            string machineUniqueId = "";

            try {
                // CPU-related serial number
                foreach (ManagementObject queryObj in searcher.Get())
                {
                    machineUniqueId +=
                        queryObj["Architecture"].ToString() + "_" +
                        queryObj["Caption"].ToString() + "_" +
                        queryObj["Family"].ToString() + "_" +
                        queryObj["ProcessorId"].ToString() + "_" +  // CPU
                        queryObj["SystemName"].ToString() ;    // Motherboard
                }

                // Attach Hardisk serial number
                string hardiskSerial = "";
                try
                {
                    string winPath = System.IO.Path.GetPathRoot(Environment.SystemDirectory);
                    ManagementObject dsk = new ManagementObject(@"win32_logicaldisk.deviceid=""" + winPath.Substring(0, 1) + @":""");
                    dsk.Get();
                    hardiskSerial = dsk["VolumeSerialNumber"].ToString();
                }
                catch
                {
                    hardiskSerial = "";
                }
                machineUniqueId += "_" + hardiskSerial;


                // IGNORE THIS PART. MAC can be spoofed
                /*
                // Attach MAC address
                String firstMacAddress = NetworkInterface
                    .GetAllNetworkInterfaces()
                    .Where(nic => nic.OperationalStatus == OperationalStatus.Up && nic.NetworkInterfaceType != NetworkInterfaceType.Loopback)
                    .Select(nic => nic.GetPhysicalAddress().ToString())
                    .FirstOrDefault();

                machineUniqueId += "_" + firstMacAddress;
                */

                // Remove empty space with "_"
                //machineUniqueId = StringEx.Replace(machineUniqueId, " ", "_", StringComparison.CurrentCulture);

                return machineUniqueId;
            }
            catch
            {
                return "0";
            }
        }

    }
}
