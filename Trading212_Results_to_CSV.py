from bs4 import BeautifulSoup
import pandas as pd

with open("results.html") as file:
    data=file.read()

soup = BeautifulSoup(data, 'html.parser')

# Find all elements with a class attribute
results = soup.find_all(class_="data-item result")
dates = soup.find_all(class_="data-item time")
directions = soup.find_all(class_="data-item item-direction")

result_list=[]
date_list=[]
dir_list=[]

# Loop through the results and print the class names
for result in results:
    result_list.append(float(result.text))

for date in dates:
    date_list.append(date.text.split(",")[0])

for direction in directions:
    dir_list.append(direction.text)

df=pd.DataFrame({"Date":date_list, "Result":result_list, "Direction":dir_list})

df.to_csv("Results.csv", index=False)
