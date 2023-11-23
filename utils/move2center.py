import os
import random
from tqdm import tqdm


INPUT_PATH = "point_cloud/4.ply"
OUTPUT_PATH = "point_cloud/4_out.ply"
DOWNSAMPLE_PATH = "point_cloud/4_ds.ply"


def downsampling(path, output, point_pro):
    # point_pro is downsampling pro

    point_cnt = 0
    point_sum = 0
    with open(path, "r") as file:
        for line in file:
            s = line.strip()
            if s.split('')[1] == 'vertex':
                point_sum = int(s.split('')[-1])
                break
    
    with open(path, "r") as file:
        flag = 0
        for line in file:
            s = line.strip()
            if s == "end_header":
                flag = 1
                continue
            if flag == 1:
                pro = random.random()
                if pro < point_pro:
                    point_cnt += 1
                    with open("temp.txt", "a") as file:
                        file.write(s + "\n")
    print(point_cnt)
                        
    with open(path, "r") as file:
        flag = 0
        for line in file:
            s = line.strip()
            if s.split('')[1] == 'vertex':
                ans = ""
                ans = s.split('')[0]
                ans = ans + ' ' + s.split('')[1]
                ans = ans + ' ' + str(point_cnt)
                with open(output, "a") as f:
                    f.write(ans + "\n")
                continue
            else:
                with open(output, "a") as f:
                    f.write(s + "\n")
                if s == "end_header":
                    break
                    
    with open("temp.txt", "r") as file:
        for line in file:
            s = line.strip()
            with open(output, "a") as f:
                f.write(s + "\n")
                
    if os.path.exists("temp.txt"):
        os.remove("temp.txt")
                
           
def get_center(path):
    center, cnt = [0, 0, 0], 0
    with open(path, "r") as file:
        flag = 0
        for line in file:
            s = line.strip()
            if s == "end_header":
                flag = 1
                continue
            if flag == 1:
                numbers = [float(num) for num in s.split()]
                numbers[0] = round(numbers[0], 6)
                numbers[1] = round(numbers[1], 6)
                numbers[2] = round(numbers[2], 6)
                center[0] = round((center[0] * cnt + numbers[0]) / (cnt + 1), 6)
                center[1] = round((center[1] * cnt + numbers[1]) / (cnt + 1), 6)
                center[2] = round((center[2] * cnt + numbers[2]) / (cnt + 1), 6)
                cnt += 1
    return center

def output_res(path, output, center):
    with open(path, "r") as file:
        flag = 0
        for line in file:
            s = line.strip()
            if s == "end_header":
                flag = 1
                with open(output, "a") as f:
                    f.write(s + "\n")
                continue
            if flag == 0:
                if(s.split(' ')[-1][0] == 's'):
                    continue
                with open(output, "a") as f:
                    f.write(s + "\n")
                continue
            if flag == 1:
                numbers = [float(num) for num in s.split()]
                # print(numbers)
                numbers[0] = round(numbers[0] - center[0], 6)
                numbers[1] = round(numbers[1] - center[1], 6)
                numbers[2] = round(numbers[2] - center[2], 6)
                # print(numbers)
                ans = str(round(numbers[0], 6)) + " " + str(round(numbers[1], 6)) + " " + str(numbers[2]) + " " + str(int(numbers[3])) + " " + str(int(numbers[4])) + " " + str(int(numbers[5])) + "\n"
                with open(output, 'a') as f:
                    f.write(ans)


if __name__ == "__main__":
    center = get_center(INPUT_PATH)
    output_res(INPUT_PATH, OUTPUT_PATH, center)
    # downsampling(OUTPUT_PATH, DOWNSAMPLE_PATH, 0.2)