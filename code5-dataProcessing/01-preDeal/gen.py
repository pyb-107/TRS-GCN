import os
import pandas as pd
# 对初始航班计划数据进行预处理，包括以下内容
# 1.仅考虑每天执飞的航班
# 2.仅考虑国内航班
# 3.将日期转化成可以识别的模式
# 4.保留航班号、机型、出发地，目的地、出发时间、到达时间
# 5.仅保留抵达时间大于出发时间的（不允许跨天）
# 6.删除掉全为空的列


# 定义输入输出文件夹路径
input_folder = 'inputData'
output_folder = 'outputData'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的所有CSV文件
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        input_path = os.path.join(input_folder, filename)
        filename = "preDeal_"+filename
        output_path = os.path.join(output_folder, filename)

        # 读取GBK编码的CSV文件
        df = pd.read_csv(input_path)

        # 删除Date不为1234567的行
        df = df[df['Date'] == '1234567']

        # 仅保留IsDome为国内的行
        df = df[df['IsDome'] == '国内']

        # 定义一个函数，将时间格式从 `1140`, `1430-` 转换为 `HH:MM:SS`
        def convert_time(time_str):
            if pd.isna(time_str):
                return time_str  # 如果时间为空，直接返回
            # 将时间转换为字符串并去除可能的 `-` 和小数点
            time_str = str(time_str).rstrip('-').replace('.0', '')
            if time_str.isdigit() and len(time_str) == 4:
                return f"{time_str[:2]}:{time_str[2:]}:00"
            elif time_str.isdigit() and len(time_str) == 3:
                return f"0{time_str[0]}:{time_str[1:]}:00"
            else:
                return None  # 如果时间格式不匹配，返回None

        # 应用时间格式转换到Departure Time和Arrival Time列
        df['Departure Time'] = df['Departure Time'].apply(convert_time)
        df['Arrival Time'] = df['Arrival Time'].apply(convert_time)

        # 删除无法转换为正确时间格式的行
        df = df.dropna(subset=['Departure Time', 'Arrival Time'])

        # 转换时间列为datetime对象以进行比较
        df['Departure Time'] = pd.to_datetime(df['Departure Time'], format='%H:%M:%S', errors='coerce')
        df['Arrival Time'] = pd.to_datetime(df['Arrival Time'], format='%H:%M:%S', errors='coerce')

        # 筛选抵达时间大于出发时间的行
        df = df[df['Arrival Time'] > df['Departure Time']]

        # 删除全为空的列
        df = df.dropna(axis=1, how='all')

        # 将时间列转换回字符串格式
        df['Departure Time'] = df['Departure Time'].dt.strftime('%H:%M:%S')
        df['Arrival Time'] = df['Arrival Time'].dt.strftime('%H:%M:%S')

        # 将处理后的数据保存为GBK编码的CSV文件
        df.to_csv(output_path, index=False)

print("CSV文件处理完成，并保存到outputData文件夹中。")
