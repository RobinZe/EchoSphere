import psutil

def monitor_memory():
    # 获取CPU的逻辑核心数
    # cpu_logical_count = psutil.cpu_count()
    # 获取CPU的物理核心数
    # cpu_physical_count = psutil.cpu_count(logical=False)
    # 获取CPU的时间统计
    # cpu_times = psutil.cpu_times()
    # 获取物理内存信息
    # memory_info = psutil.virtual_memory()
    # 获取物理内存信息
    mem = psutil.virtual_memory()

    # 将字节转换为GB
    total_memory_gb = mem.total / (1024 ** 3)
    used_memory_gb = mem.used / (1024 ** 3)
    free_memory_gb = mem.free / (1024 ** 3)

    # 打印内存信息
    print(f"Total memory: {total_memory_gb:.2f} GB")
    print(f"Used memory: {used_memory_gb:.2f} GB")
    print(f"Free memory: {free_memory_gb:.2f} GB")
    # 获取磁盘使用率
    # disk_usage = psutil.disk_usage()
    # print(f"CPU logical count: {cpu_logical_count};\nCPU physical count: {cpu_physical_count};\nCPU times: {cpu_times};\nMemory usage: {memory_info.percent}%\nDisk usage: {disk_usage}\n")
