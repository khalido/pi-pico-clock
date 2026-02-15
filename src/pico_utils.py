import os

def filesystem_info():
    statvfs = os.statvfs('/')

    # Calculate the total space in kilobytes
    total_space_kb = (statvfs[0] * statvfs[2]) / 1024

    # Calculate the free space in kilobytes
    free_space_kb = (statvfs[0] * statvfs[3]) / 1024

    print(f"Total space: {total_space_kb:.2f} KB")
    print(f"Free space: {free_space_kb:.2f} KB")

filesystem_info()