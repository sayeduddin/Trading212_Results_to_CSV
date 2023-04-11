from bs4 import BeautifulSoup
import pandas as pd
from datetime import date as d

with open("results.txt") as file:
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

def color_cell(val):
    if val < 0:
        return 'background-color: #ff9999'
    elif val > 0:
        return 'background-color: #b3ffb3'
    else:
        return ''

# Apply the formatting to the "Result" column
styled_df = df.style.applymap(color_cell, subset=pd.IndexSlice[:, 'Result'])

styled_df.to_excel("Results.xlsx", index=False)



def show_wr(df):
    wr=df.loc[df["Result"]>0]["Result"].count()/len(df)
    print(f"Winrate: {round(wr*100, 2)}%")

def show_avg_wl(df):
    w=round(df.loc[df["Result"]>0]["Result"].mean(), 2)
    l=round(df.loc[df["Result"]<0]["Result"].mean(), 2)
    print(f"Avg W/L: {w}/{l}")

def show_today_res(daily_res):
    """
    today = "/".join(str(d.today()).split("-")[::-1])
    df=df.loc[df["Date"]==today]
    total=round(df["Result"].sum(), 2)
    print(f"Daily Result: £{total}")
    """
    """
    today = "/".join(str(d.today()).split("-")[::-1])
    if today in daily_res:
        print(f"Daily Result: {daily_res[today]}")
    else:
        print(f"Daily Result: None")
    """
    res=daily_res[list(daily_res.keys())[0]]
    print(f"Today's Result: {res}")

def get_daily_res(df):
    curr_date=df.iloc[0]["Date"]
    dates=[]
    sums=[]
    total=0
    for i, row in df.iterrows():
        if row["Date"]==curr_date:
            total+=row["Result"]
        else:
            sums.append(round(total, 2))
            dates.append(curr_date)
            curr_date=row["Date"]
            total=row["Result"]

    sums.append(round(total, 2))
    dates.append(curr_date)
    res_dic=dict(zip(dates, sums))
    return res_dic

def show_prev_res(daily_res):
    res=daily_res[list(daily_res.keys())[1]]
    print(f"Previous Result: {res}")

show_wr(df)
show_avg_wl(df)

daily_res=get_daily_res(df)
show_today_res(daily_res)
show_prev_res(daily_res)


input()
