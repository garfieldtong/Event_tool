
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

## Global variable of circle rows

# String of possible row name
uppercase_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercase_list = "abcdefghijklmnopqrstuvwxyz"
katakana_list = "アイウエオカキクケコサシスセソタチツテトナニヌネノハパヒピフプヘペホポマミムメモヤユヨラリルレロワヲン"
hiragana_list = "あいうえおかきくけこさしすせそたちつてとなにぬねのはぱひぴふぷへぺほぽまみむめもやゆよらりるれろわをん" 

# Specify the upper limit of the row name for each string list
uppercase_stop = "Z"
lowercase_stop = "w"
katakana_stop = "ヲ"
hiragana_stop = "む"

# Concatenate all the existing row name
all_rows = uppercase_list.split(uppercase_stop)[0] + uppercase_list \
        + katakana_list.split(katakana_stop)[0] +  katakana_stop\
        + lowercase_list.split(lowercase_stop)[0] + lowercase_stop\
        + hiragana_list.split(hiragana_stop)[0] + hiragana_stop

# Specify the upper limit of row name in each hall
hall_1_stop = "シ"
hall_2_stop = "ヲ"
hall_3_stop = "m"
hall_4_stop = "w"

# Find out the exising row name in each hall
hall_1_row = all_rows.split(hall_1_stop)[0] + hall_1_stop
hall_2_row = all_rows.split(hall_1_row)[-1].split(hall_2_stop)[0] + hall_2_stop
hall_3_row = all_rows.split(hall_2_row)[-1].split(hall_3_stop)[0] + hall_3_stop
hall_4_row = all_rows.split(hall_3_row)[-1].split(hall_4_stop)[0] + hall_4_stop
hall_5_row = all_rows.split(hall_4_row)[-1]

kabe_circle_list = ['A', 'a', 'あ', 'ス']

app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


warning_msg = "<table> <tr>   <td>Connection problem. Please try again.</td> </tr></table>"


# def checkbox_convert(df1):

#     df1["購入済み"].replace({1: 'O', 0: 'X'}, inplace=True)


# Function for returning csv of all circles
@app.get("/bug")
async def return_whole_csv():

    dd="abc"+1344
    return 0
@app.get("/return_whole_csv")
async def return_whole_csv():



    try:
        ori_df = pd.read_csv("circle_list.csv")
        ori_df = ori_df.astype({"購入済み": 'Int32'})
        df = ori_df.to_html(index = False).replace("\n", "").replace("NaN", "")
        
        return df

    except:
        return warning_msg

# Function for returning csv of all circles on FIRST DAY
@app.get("/first_day_csv")
async def first_day_csv():

    try:
        ori_df = pd.read_csv("circle_list.csv")
        ori_df = ori_df.astype({"購入済み": 'Int32'})
        df = ori_df.loc[ori_df["何日目"] == 1]
        df = df.to_html(index = False).replace("\n", "").replace("NaN", "")

        return df
    
    except:
        return warning_msg
    
# Function for returning csv of all circles on SECOND DAY
@app.get("/second_day_csv")
async def second_day_csv():

    try:
        ori_df = pd.read_csv("circle_list.csv")
        ori_df = ori_df.astype({"購入済み": 'Int32'})
        df = ori_df.loc[ori_df["何日目"] == 2]
        df = df.to_html(index = False).replace("\n", "").replace("NaN", "")

        return df

    except:
        return warning_msg


# Function for returning csv of closest circle
@app.post("/closest_circle/")
async def closest_circle(request: Request):
    input = await request.body()

    try:

        day, currentPos = input.decode().split('\n')

        # Filter df according to which day
        ori_df = pd.read_csv("circle_list.csv")
        ori_df = ori_df.astype({"購入済み": 'Int32'})
        temp_df = ori_df.loc[ori_df["何日目"] == int(day)].reset_index(drop = True)

        # Find row names in current row
        for row in [hall_1_row, hall_2_row, hall_3_row, hall_4_row, hall_5_row]:
            if currentPos in row:
                current_hall_row = row
                break

        # Find index of current position in row name string
        current_index = current_hall_row.find(currentPos)

        # Calculate distance to each circle
        dist_list = []
        other_hall_id_list = []

        # Loop through all rows in temp_df

        for csv_row_id, row_name in enumerate(temp_df["行"]):
            print(csv_row_id, row_name)
            index = current_hall_row.find(row_name)
            if index >= 0:   # If circle in same hall (row of all circles index can be found in row list)
                print(row_name, current_index - index)

                dist_list.append((csv_row_id, abs(current_index - index)))
            else:
                other_hall_id_list.append(csv_row_id)

        # Sort according to distance for circles in same hall, create df for circles in other halls as well
        dist_list = sorted(dist_list, key=lambda x:x[1])
        df = temp_df.reindex([x[0] for x in dist_list])
        other_hall_df = temp_df.reindex([x for x in other_hall_id_list])

        # Generate table
        df = df.to_html(index = False).replace("\n", "").replace("NaN", "")
        other_hall_df = other_hall_df.to_html(index = False).replace("\n", "").replace("NaN", "")


        df += "<table>\
                <tr><th colspan='6'>別のホール</th></tr>\
                </table>" 
        
        df += other_hall_df

        return df

    except:
        return warning_msg


# Function for adding circle to csv
@app.post("/add_circle/")
async def closest_circle(request: Request):
    input = await request.body()

    try:

        newCircle, newHall, newRow,newNumber, newDay  = input.decode().split('\n')

        # add the info to csv
        ori_df = pd.read_csv("circle_list.csv")
        ori_df = ori_df.astype({"購入済み": 'Int32'})
        appendRow = pd.DataFrame({
        'サークル名': [newCircle],
        'ホール': [newHall],
        '行': [newRow],
        '番': [newNumber],
        '何日目': [newDay],
        '購入済み': ['0']
        })

        pd.concat([ori_df, appendRow], ignore_index=True).to_csv("circle_list.csv", index = False)

    except:
        return warning_msg

# Function for adding circle to csv
@app.post("/filter_table/")
async def filter_table(request: Request):
    form = await request.form()

    try:
        dayList = form.get("checkedDayList").split(",")
        dayList = [int(x) for x in dayList]
        hallList = form.get("checkedHallList").split(",")
        boughtList = form.get("checkedBoughtList").split(",")
        boughtList = [int(x) for x in boughtList]

        print(dayList, hallList, boughtList)


        # filter csv
        ori_df = pd.read_csv("circle_list.csv")
        ori_df = ori_df.astype({"購入済み": 'Int32'})

        df = ori_df[(ori_df['何日目'].isin(dayList)) & (ori_df['ホール'].isin(hallList)) & (ori_df['購入済み'].isin(boughtList))]

        df = df.to_html(index = False).replace("\n", "").replace("NaN", "")

        return df
    
    except:
        return warning_msg



# Function for adding circle to csv
@app.post("/change_bought_status/")
async def change_bought_status(request: Request):
    input = await request.body()

    try:

        circleName = input.decode()
        ori_df = pd.read_csv("circle_list.csv")
        ori_df = ori_df.astype({"購入済み": 'Int32'})
        circledfIndex = ori_df.index[ori_df['サークル名'] == circleName].tolist()[0]

        currentStatus = ori_df.loc[circledfIndex, '購入済み']
        if currentStatus == 1:
            currentStatus = 0
        else:
            currentStatus = 1

        
        ori_df.loc[circledfIndex, '購入済み'] = currentStatus
        ori_df.to_csv("circle_list.csv", index = False)

    except:
        return warning_msg


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
