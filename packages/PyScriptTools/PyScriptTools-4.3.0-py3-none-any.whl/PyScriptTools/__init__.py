# █▀█ █▄█ █▀▀ █▀▀ █▀█ █ █▀█ ▀█▀ ▀█▀ █▀█ █▀█ █   █▀▀
# █▀▀  █  ▄▄█ █▄▄ █▀▄ █ █▀▀  █   █  █▄█ █▄█ █▄▄ ▄▄█

"""

    PyScriptTools Library
    =====================
    version : 4.3.0\n
    author : Shervin Badanara\n
    author github : https://www.github.com/shervinbdndev/\n
    source github : https://www.github.com/shervinbdndev/PyScriptTools.py/\n
    
    PyScriptTools is a Python Based Library That You Can Use it To Gather your System Information.\n
    for e.x You Can Print Your Public IP Address:\n\t
        >>> from PyScriptTools import NetworkTools

        >>> network_obj = NetworkTools()
        >>> public_ip = network_obj.ShowPublicIP(show=True)
        >>> print(public_ip)

"""

try:
    """
    from __future__ import absolute_import
    from __future__ import print_function
    from __future__ import all_feature_names
    """
    """import io"""
    import os
    import sys
    import ctypes
    import getpass
    import platform
    import requests
    import json
    import socket
    import GPUtil
    import psutil
    import datetime
    import getmac
    import string
    import colorama
    import cfonts
    import random
    from pathlib import Path
    from typing import (Tuple , Any)
    from .exceptions import (
        AdminPermissionRequestDenied ,
        InvalidVariableType ,
        NoneLinuxMethod ,
        NoneTypeArgumentBool ,
        NoneTypeArgumentInt ,
        NoneTypeArgumentString ,
        UndefinedOperatingSystem ,
        UnrecognizeableTypeArgument
    )
    from .validators import (
        BooleanValidator ,
        IntegerValidator ,
        StringValidator ,
        LengthValidator ,
        LinuxOperatingSystemIdentifierValidator ,
        WindowsOperatingSystemIdentifierValidator
    )
    
    if (__name__ == '__main__' and __package__ is None):
        sys.path.append(os.path.dirname(p=os.path.dirname(p=os.path.abspath(path=__file__))))
        file = Path(__file__).resolve()
        parent , top = file.parent , file.parents[3]
        sys.path.append(str(top))
        try:
            sys.path.remove(str(parent))
        except ValueError:
            pass

except:
    raise ModuleNotFoundError






class MetaData:
    def __init__(self) -> None:
        super(MetaData , self).__init__()
        
        self.version = r"4.3.0"
        """with io.open(file=os.path.join(os.path.abspath('.') , 'version.txt') , mode='r+' , encoding='utf-8' , errors=None) as temp:
            self.version = temp.readline()"""
                
    def __str__(self) -> str:
        return self.version






class NetworkTools:
    localIP = str(socket.gethostbyname(socket.gethostname()))
    publicIPLoader = requests.get('https://api.myip.com').content
    loadedIP = json.loads(publicIPLoader)
    publicIP = str(loadedIP['ip'])
    ipAddrs =  psutil.net_if_addrs()
    
    @classmethod
    def ShowLocalIP(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _Local IP_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.localIP
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowPublicIP(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _Public IP_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                try:
                    return cls.publicIP
                except ConnectionError:
                    pass
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowMacAddress(cls , show : bool = False , network_request : bool = True) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.
            network_request (bool): _Use Internet To get MacAddress(better to use True)_. Defaults to True.

        Returns:
            str: _MAC Address_
        """
        if (BooleanValidator.is_boolean([show , network_request])):
            if (show is True):
                try:
                    return getmac.get_mac_address(ip = socket.gethostbyname(socket.gethostname()) , network_request = network_request)
                except ConnectionError:
                    pass
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowNetworkInfo(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _Shows Some of Your Network Information_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                for interfaceName , interfaceAddresses in cls.ipAddrs.items():
                    for address in interfaceAddresses:
                        print(f"{colorama.ansi.Fore.GREEN}=== Interface :{colorama.ansi.Fore.MAGENTA} {interfaceName} {colorama.ansi.Fore.GREEN}===")
                        if (str(address.family) == "AddressFamily.AF_INET"):
                            print(f"{colorama.ansi.Fore.WHITE}IP Address : {address.address}")
                            print(f"Netmask : {address.netmask}")
                            print(f"Broadcast IP : {address.broadcast}")
                        elif (str(address.family) == "AddressFamily.AF_PACKET"):
                            print(f"Mac Address : {address.address}")
                            print(f"Netmask : {address.netmask}")
                            print(f"Broadcast MAC : {address.broadcast}")
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowSavedNetworks(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _Shows Saved Networks_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                if (WindowsOperatingSystemIdentifierValidator.current_is_windows):
                    for i in os.popen("netsh wlan show profiles"):
                        if ("All User Profile" in i):
                            i = str(i).split(":")
                            i = f"{colorama.ansi.Fore.GREEN}Network Name : {colorama.ansi.Fore.MAGENTA} {i[1].strip()}"
                            print(i)
                            continue
                else:
                    return f"{colorama.ansi.Fore.YELLOW}This Method Only Works on Windows OS !!!"
            elif (show is False):
                return AdminPermissionRequestDenied
            elif (show is None):
                show = None
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return AdminPermissionRequestDenied

    @classmethod
    def TestConnection(cls , show : bool = False , timeout : int = 5):
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.
            timeout (int): _Sets The Timeout For Each Request_. Defaults to 5.

        Returns:
            _str_: _Tests Internet Connection_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                if (IntegerValidator.is_integer(timeout)):
                    try:
                        req = requests.get("https://www.google.com" , timeout = timeout)
                        return f"{colorama.ansi.Fore.GREEN}You're Connected To Internet"
                    except (requests.ConnectionError , requests.Timeout) as E:
                        return f"{colorama.ansi.Fore.RED}You're not Connected To Internet \n{E}"
                else:
                    return NoneTypeArgumentInt
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def StatusCodeChecker(cls , show : bool = False , link : str = ''):
        """_summary_

        Args:
            _show_ (bool): _Shows The Output_. Defaults to False.
            _link_ (str): Link to The Target Website or IP Address.

        Returns:
            _str_: Status Codes Available in Link or IP Address
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                if (StringValidator.is_string(link)):
                    for code in range(200 , 599 + 1):
                        if (requests.get(link).status_code == code):
                            print(f"{colorama.ansi.Fore.MAGENTA}Status : {colorama.ansi.Fore.BLUE}{code} {colorama.ansi.Fore.GREEN}is Available")
                        else:
                            print(f"{colorama.ansi.Fore.MAGENTA}Status : {colorama.ansi.Fore.BLUE}{code} {colorama.ansi.Fore.RED}is not Available")
                else:
                    return NoneTypeArgumentString
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool






class CPUTools:
    phCores = psutil.cpu_count(logical = False)
    totCores = psutil.cpu_count(logical = True)
    cpuFreq = psutil.cpu_freq()
    cpuType = platform.uname().processor

    @classmethod
    def ShowCPUType(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _CPU Type_
        """
        if (show is True):
            return cls.cpuType
        elif (show is False):
            return AdminPermissionRequestDenied
        else:
            return UnrecognizeableTypeArgument

    @classmethod
    def ShowCPUPhysicalCores(cls , show : bool = False) -> int:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            int: _CPU Physical Cores_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.phCores
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowCPUTotalCores(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _CPU Total Cores_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.totCores
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowCPUMaxFreq(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _CPU Maximum Frequency_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{cls.cpuFreq.max:.2f}Mhz"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool
    
    @classmethod
    def ShowCPUMinFreq(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _CPU Minimum Frequency_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{cls.cpuFreq.min:.2f}Mhz"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowCPUCurrentFreq(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _CPU Current Frequency_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{cls.cpuFreq.current:.2f}Mhz"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowCPUTotalUsage(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _CPU Total Frequency_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{psutil.cpu_percent()}%"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowCPUUsagePerCore(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _CPU Usage Per Cores_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                for core , percentage in enumerate(psutil.cpu_percent(percpu = True , interval = 1)):
                    print(f"Core {core} : {percentage}%")
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool






class GPUTools:
    gpuInfo = GPUtil.getGPUs()

    @classmethod
    def ShowGPU_ID(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _GPU ID_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                for gpu in cls.gpuInfo:
                    gpuID = gpu.id
                return gpuID
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowGPUName(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _GPU Name_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                for gpu in cls.gpuInfo:
                    gpuName = gpu.name
                return gpuName
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowGPULoad(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _GPU Load_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                for gpu in cls.gpuInfo:
                    gpuLoad = gpu.load * 100
                    if (gpuLoad > 50.0):
                        newGpu = f"{colorama.ansi.Fore.RED}{gpu.load * 100}%{colorama.ansi.Fore.WHITE}"
                        return newGpu
                    else:
                        newGpu = f"{colorama.ansi.Fore.GREEN}{gpu.load * 100}%{colorama.ansi.Fore.WHITE}"
                        return newGpu
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowGPUFreeMemory(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _GPU Free Memory_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                for gpu in cls.gpuInfo:
                    gpuFree = gpu.memoryFree
                return gpuFree
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowGPUUsedMemory(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _GPU Used Memory_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                for gpu in cls.gpuInfo:
                    gpuUsed = f"{gpu.memoryUsed}MB"
                return gpuUsed
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowGPUTotalMemory(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _GPU Total Memory_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                for gpu in cls.gpuInfo:
                    gpuTot = f"{gpu.memoryTotal}MB"
                return gpuTot
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowGPUTemperature(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _GPU Temperature_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                for gpu in cls.gpuInfo:
                    gpuTemp = f"{gpu.temperature}℃"
                return gpuTemp
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowGPU_UUID(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _GPU UUID_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                for gpu in cls.gpuInfo:
                    gpuUUID = gpu.uuid
                return gpuUUID
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool





class RAMTools:
    ramVir = psutil.virtual_memory()
    swapMemo = psutil.swap_memory()
    
    @classmethod
    def ShowTotalRAM(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _Total RAM Memory_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{LengthValidator.getSize(cls.ramVir.total)}"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowAvailableRAM(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _Available RAM Memory_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{LengthValidator.getSize(cls.ramVir.available)}"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowUsedRAM(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _Used RAM Memory_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{LengthValidator.getSize(cls.ramVir.used)}"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowRAMPercentage(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _RAM Percentage_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{LengthValidator.getSize(cls.ramVir.percent)}%"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowTotalSwap(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _Total Swap Memory_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{LengthValidator.getSize(cls.swapMemo.total)}"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowFreeSwap(cls , show : bool = False) -> int:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            int: _Free Swap Memory_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{LengthValidator.getSize(cls.swapMemo.free)}"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowUsedSwap(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _Used Swap Memory_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{LengthValidator.getSize(cls.swapMemo.used)}"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowSwapPercentage(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            float: _Swap Percentage_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{LengthValidator.getSize(cls.swapMemo.percent)}%"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool






class DiskTools:
    listDrives = []
    try:
        bitMask = ctypes.windll.kernel32.GetLogicalDrives()
    except:
        bitMask = str(NoneLinuxMethod)
    drivesInfo = psutil.disk_partitions()
    parentDiskInfo = psutil.disk_usage(path='/')

    @classmethod
    def ShowDrives(cls , show : bool = False) -> list:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            list: _List Of All Available Drives_
        """
        if (BooleanValidator.is_boolean(show)):
            if (platform.system()[0].upper() == 'W'):
                if (show is True):
                    for driver in string.ascii_uppercase:
                        if (cls.bitMask & 1) :
                            cls.listDrives.append(driver)
                        cls.bitMask >>= 1
                    return cls.listDrives
                elif (show is False):
                    return AdminPermissionRequestDenied
                else:
                    return UnrecognizeableTypeArgument
            else:
                return NoneLinuxMethod
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowParentDiskTotalMemory(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            list: _Parent Disk Total Memory_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.parentDiskInfo.total / 1024 ** 3
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod    
    def ShowParentDiskUsedMemory(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            list: _Parent Disk Used Memory_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.parentDiskInfo.used / 1024 ** 3
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod    
    def ShowParentDiskFreeMemory(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            list: _Parent Disk Free Memory_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.parentDiskInfo.free / 1024 ** 3
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod    
    def ShowParentDiskPercentage(cls , show : bool = False) -> float:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            list: _Parent Disk Percentage_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return f"{cls.parentDiskInfo.percent:.2f}"
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod    
    def ShowDiskInfo(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            list: _Disk Information_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                for partition in cls.drivesInfo:
                    print(f"{colorama.ansi.Fore.GREEN}=== Device : {partition.device} ===")
                    print(f"{colorama.ansi.Fore.WHITE}Mountpoint : {colorama.ansi.Fore.MAGENTA}{partition.mountpoint}{colorama.ansi.Fore.WHITE}")
                    print(f"File System Type : {partition.fstype}")
                    try:
                        partitionUsage = psutil.disk_usage(partition.mountpoint)
                    except PermissionError:
                        continue
                    print(f"Total Size : {LengthValidator.getSize(partitionUsage.total)}")
                    print(f"Used : {LengthValidator.getSize(partitionUsage.used)}")
                    print(f"Free : {LengthValidator.getSize(partitionUsage.free)}")
                    print(f"Percentage : {LengthValidator.getSize(partitionUsage.percent)}\n")
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool






class SystemTools:
    osName = str(platform.system())
    osType = list(platform.architecture())[0]
    systemName = str(platform.node())
    try:
        getKernel32 = ctypes.windll.kernel32.GetTickCount64()
        getTime = int(str(getKernel32)[:-3])
        mins, sec = divmod(getTime, 60)
        hour, mins = divmod(mins, 60)
        days, hour = divmod(hour, 24)
        uptimeSystem = str("{0}:{1}:{2}:{3}").format(days , hour , mins , sec)
    except:
        getKernel32 = str(NoneLinuxMethod);getTime = str(NoneLinuxMethod);mins=str(NoneLinuxMethod);sec=str(NoneLinuxMethod);hour=str(NoneLinuxMethod);days=str(NoneLinuxMethod);uptimeSystem=str(NoneLinuxMethod)
    userName = getpass.getuser()
    listSysInfo = []
    pythonVer = sys.version[0:6]
    nodeName = platform.uname().node
    sysRelease = platform.uname().release
    sysVersion = platform.uname().version
    bootTime = datetime.datetime.fromtimestamp(psutil.boot_time())

    @classmethod
    def ShowOsName(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _Operating System's Name_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.osName
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowOsType(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _Operating System's Type
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.osType
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowNodeName(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _Node Name or System's Name_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.nodeName
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowOSRelease(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _Operating System's Release_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.sysRelease
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowOSVersion(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _Operating System's Version_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.sysVersion
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowSystemName(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _System's Name_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.systemName
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowSystemUptime(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _System's Uptime_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.uptimeSystem
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowUserName(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _Active Logined Username_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.userName
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowSystemInformation(cls , show : bool = False , os_name : str = "Windows") -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.
            os_name (str): _Choose The Operating System_. Defaults to "Windows".

        Returns:
            str: _Shows System Information Based On Your Operating System_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                if (StringValidator.is_string(os_name)):
                    if (WindowsOperatingSystemIdentifierValidator.is_windows(os_name)):
                        print (
                            f"{colorama.ansi.Fore.GREEN}OS Name : {colorama.ansi.Fore.BLUE}{cls.osName}" ,
                            f"\n{colorama.ansi.Fore.GREEN}OS Type : {colorama.ansi.Fore.WHITE}{cls.osType}" ,
                            f"\n{colorama.ansi.Fore.GREEN}OS Release : {colorama.ansi.Fore.WHITE}{cls.sysRelease}" ,
                            f"\n{colorama.ansi.Fore.GREEN}OS Version : {colorama.ansi.Fore.WHITE}{cls.sysVersion}" ,
                            f"\n{colorama.ansi.Fore.GREEN}System Name : {colorama.ansi.Fore.WHITE}{cls.systemName or cls.nodeName}" ,
                            f"\n{colorama.ansi.Fore.GREEN}System Uptime : {colorama.ansi.Fore.WHITE}{cls.uptimeSystem}" ,
                            f"\n{colorama.ansi.Fore.GREEN}User Logined As : {colorama.ansi.Fore.WHITE}{cls.userName}"
                        )
                    elif (LinuxOperatingSystemIdentifierValidator.is_linux(os_name)):
                        print (
                            f"{colorama.ansi.Fore.GREEN}OS Name : {colorama.ansi.Fore.BLUE}{cls.osName}" ,
                            f"\n{colorama.ansi.Fore.GREEN}OS Type : {colorama.ansi.Fore.WHITE}{cls.osType}" ,
                            f"\n{colorama.ansi.Fore.GREEN}OS Release : {colorama.ansi.Fore.WHITE}{cls.sysRelease}" ,
                            f"\n{colorama.ansi.Fore.GREEN}OS Version : {colorama.ansi.Fore.WHITE}{cls.sysVersion}" ,
                            f"\n{colorama.ansi.Fore.GREEN}System Name : {colorama.ansi.Fore.WHITE}{cls.systemName or cls.nodeName}" ,
                            f"\n{colorama.ansi.Fore.GREEN}User Logined As : {colorama.ansi.Fore.WHITE}{cls.userName}"
                        )
                    else:
                        return UndefinedOperatingSystem
                else:
                    return InvalidVariableType
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowPythonVersion(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _Python Version_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.pythonVer
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def ShowBootTime(cls , show : bool = False) -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.

        Returns:
            str: _Operating System's Boot Time_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                return cls.bootTime
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool






class OtherTools:
    pathValidation = bool()

    @classmethod
    def ConvertToAscii(cls , show : bool = False , text : Any = '' , colors : list = [] , align : Tuple[str] = "" , font : str = "") -> str:
        """_summary_

        Args:
            show (bool, optional): _Show The Output_. Defaults to False.
            text (str, optional): _Your Text Here_. Defaults to ''.
            colors (list, optional): _['color1' , 'color2']_. Defaults to [].
            align (Tuple, optional): _("left" , "center" , "right") Use One_. Defaults to "".
            font (str, optional): _("console" , "block" , "simpleBlock" , "simple" , "3d" , "simple3d" , "chrome" , "huge" , "grid" , "pallet" , "shade" , "slick" , "tiny") Use One_. Defaults to "".

        Returns:
            str: _Customized Ascii Art_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                if (StringValidator.is_string([text , font])):
                    cls.text = str(text)
                    cls.colors = colors
                    cls.align = align
                    cls.font = font
                    cls.configuration = cfonts.render(
                        text = cls.text ,
                        colors = cls.colors ,
                        align = cls.align ,
                        font = cls.font
                    )
                    return cls.configuration
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool

    @classmethod
    def IsPath(cls , show : bool = False , pathaddr : str = '') -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.
            pathaddr (str): _System's Local Address_. Defaults to ''.

        Returns:
            str: _Validates The Path You've Entered_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                if (StringValidator.is_string(pathaddr)):
                    if (os.path.exists(r"{0}".format(pathaddr)) and (platform.system()[0].upper() in ["W" , "L" , "J"])):
                        return f"{colorama.ansi.Fore.GREEN}The Path Exists\nThe Code Output is {colorama.ansi.Fore.BLUE}{True}"
                    else:
                        return f"{colorama.ansi.Fore.RED}The Path Doesn't Exist\nThe Code Output is {colorama.ansi.Fore.BLUE}{False}"
                else:
                    return InvalidVariableType
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool
        
    @classmethod
    def GetAbsOutput(cls , show : bool = False , string : str = '') -> str:
        """_summary_

        Args:
            show (bool): _Shows The Output_. Defaults to False.
            string (str): _Your Python Command or Expression_. Defaults to ''.

        Returns:
            str: _Runs The Text as a Python Command or Expression_
        """
        if (BooleanValidator.is_boolean(show)):
            if (show is True):
                if (StringValidator.is_string(string)):
                    return eval(string)
                else:
                    return InvalidVariableType
            elif (show is False):
                return AdminPermissionRequestDenied
            else:
                return UnrecognizeableTypeArgument
        else:
            return NoneTypeArgumentBool





class PrintHeaderClass:
    def __init__(self , *args , **kwargs) -> str:
        super(PrintHeaderClass , self).__init__(*args , **kwargs)
        self.colorList = [
            "black" , "red" , "green" , "yellow" ,
            "blue" , "magenta" , "cyan" , "white" ,
            "gray"
        ]
        self.headerShow = cfonts.render(
            text = "PyScriptTools" ,
            colors = [
                random.choice(self.colorList) ,
                random.choice(self.colorList)
            ] ,
            align = "center" ,
            font = "slick"
        )

    @property
    async def HeaderPrint(self):
        return self.headerShow