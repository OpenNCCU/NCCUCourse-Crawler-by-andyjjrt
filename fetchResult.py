import csv, requests, os, json
from tqdm import tqdm
from constant import courseresult_csv, COURSERESULT_YEARSEM
import shutil

def main():
  for sem in COURSERESULT_YEARSEM:
    i = 0
    row_count = sum(1 for line in open("./data/" + courseresult_csv(sem), 'r'))
    with open("./data/" + courseresult_csv(sem), 'r') as f:
      reader = tqdm(csv.reader(f), total=row_count)
      for row in reader:
        courseid = str(row[0])
        try:
          res = requests.get("https://es.nccu.edu.tw/course/zh-TW/:sem=" + sem + "%20" + str(courseid) + "%20/").json()
          result = dict({
            "yearsem": sem,
            "time": res[0]["subTime"],
            "courseId": courseid,
            "studentLimit": str(row[3]),
            "studentCount": str(row[4]),
            "lastEnroll": str(row[5])
          })
          data_path= "./result/" + res[0]["teaNam"] + "/" + res[0]["subNam"]
          if not os.path.exists(data_path):
            os.makedirs(data_path)
          if not os.path.exists(data_path + "/courseResult"):
            os.makedirs(data_path + "/courseResult")
          if not os.path.exists(data_path + "/courseResult/" + sem + ".json"):
            with open(data_path + "/courseResult/" + sem + ".json", "w") as file:
              json.dump(list(), file)
          
          with open(data_path + "/courseResult/" + sem + ".json", 'r') as file:
            original_data = json.loads(file.read())
          original_data.append(result)
          with open(data_path + "/courseResult/" + sem + ".json", "w") as file:
            json.dump(original_data, file)
        except BaseException as err:
          print(courseid + ": ", err)
        i += 1
      
  
if __name__ == "__main__":
  main()