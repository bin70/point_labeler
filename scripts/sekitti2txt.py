import os
import struct
import numpy as np
import argparse

'''
说明: 
这是将手工标注的SemanticKITTI格式的数据，转化成普通的txt文件的脚本

每行的格式为:
(x, y, z, label)

其中label的值为:
{0: unused, 
 1: floor, 
 2: ceiling, 
 3: wall, 
 4以上: others}
'''

def read_labels(filename):
  """ read labels from given file. """
  contents = bytes()
  with open(filename, "rb") as f:  # rb = read binary
    f.seek(0, 2)  # move the cursor to the end of the file
    num_points = int(f.tell() / 4)
    f.seek(0, 0)
    contents = f.read()

  arr = [struct.unpack('<I', contents[4 * i:4 * i + 4])[0] for i in range(num_points)]
  
  return arr

def read_points(filename):
  """ read pointcloud from given file in KITTI format."""
  contents = bytes()
  with open(filename, "rb") as f:  # rb = read binary
    f.seek(0, 2)  # move the cursor to the end of the file
    num_points = int(f.tell() / 4)
    f.seek(0, 0)
    contents = f.read()

  arr = [struct.unpack('<f', contents[4 * i:4 * i + 4])[0] for i in range(num_points)]
  points_arr = np.asarray(arr)  # convert list to array
  
  points = [np.array([x, y, z, 1]) for (x, y, z) in zip(points_arr[0::4], points_arr[1::4], points_arr[2::4])]
  return points

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--input", required=True)
  parser.add_argument("--output")
  
  args = parser.parse_args()

  if not os.path.exists(args.input):
    print("-- Input directory is not exist!")
    exit()
  
  out_dir = args.output
  if out_dir is None:
    out_dir = os.path.join("labeled_pcds", args.input.split('/')[-1])
  if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)
  print("-- Writing pcds to directory {}".format(args.output))

  scan_dir = os.path.join(args.input, "velodyne")
  label_dir = os.path.join(args.input, "labels")

  scan_list = os.listdir(scan_dir)
  label_list = os.listdir(label_dir)

  if(len(scan_list) != len(label_list)):
    print("the scans number is not equal to the labels number")
    exit()

  scan_list.sort()
  label_list.sort()

  for i, scan_name in enumerate(scan_list):
      scan_path = os.path.join(scan_dir, scan_name)
      label_path = os.path.join(label_dir, label_list[i])

      scan = read_points(scan_path)
      label = read_labels(label_path)

      for j in range(len(scan)):
          scan[j][3] = label[j]

      out_name = scan_name.split('.')[0]+'.txt'
      out_path = os.path.join(out_dir, out_name)

      print("saving {}".format(out_path))
      np.savetxt(out_path, scan)
    

