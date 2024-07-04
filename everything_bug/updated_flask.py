
# from fastapi import FastAPI, Request
# from fastapi.responses import FileResponse
# import uvicorn
# from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import cv2
import numpy as np
import json
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

## Global variable of circle rows
test_x_row = [733, 838, 927, 1016, 1105, 1195, 1284, 1397, 1510, 1599, 1688, 1778, 1867, 1956, 2046, 2173, 2300, 2389, 2478, 2568, 2681, 2793, 2882, 2972, 3061, 3150, 3240, 3329, 3456, 3583, 3672, 3761, 3865, 3894]
test_y_row = [1168, 1482, 1757, 2043, 2328]

x1, y1, x2, y2 = 750, 1168, 4045, 2418 # boundaries to be cropped on pdf

## Load locations json file
f = open('locations.json')
data = json.load(f)
f.close()

warning_msg = "<table> <tr>   <td>Connection problem. Please try again.</td> </tr></table>"

class Route_func:
    ## The following procedure reduces the node dict to at most 6 nodes for path calculation
    def concerned_coords(test_x_row, test_y_row, start, end):

        # concerned nodes along x- / y-axis
        x_can = set()
        y_can = set()

        # Assume that start/end must lie at walking route but not at any nodes themselves!
        # If start/end lie along x-axis of any nodes, store x-coords of adjacent nodes, store its y coords
        # and vice versa 
        if start[0] not in test_x_row:
            bin_id = np.digitize(start[0], test_x_row)
            x_can.add(test_x_row[bin_id-1])
            x_can.add(test_x_row[bin_id])

            y_can.add(start[1])

        if end[0] not in test_x_row:

            bin_id = np.digitize(end[0], test_x_row)
            # print(bin_id, len(test_x_row))
            x_can.add(test_x_row[bin_id-1])
            x_can.add(test_x_row[bin_id])

            y_can.add(end[1])

        if start[1] not in test_y_row:
            bin_id = np.digitize(start[1], test_y_row)
            y_can.add(test_y_row[bin_id-1])

            if bin_id != len(test_y_row):
                y_can.add(test_y_row[bin_id])

            x_can.add(start[0])

        if end[1] not in test_y_row:
            bin_id = np.digitize(end[1], test_y_row)
            y_can.add(test_y_row[bin_id-1])
            if bin_id != len(test_y_row):
                y_can.add(test_y_row[bin_id])

            x_can.add(end[0])


        test_x_row = sorted(list(x_can))
        test_y_row = sorted(list(y_can))

        return test_x_row, test_y_row
    
    def extract_first_number(string):
        match = re.search(r'^[^\d]*(\d+)', string)
        if match:
            return match.group(1).zfill(2)  # Convert matched string to integer
        else:
            return None  # Return None if no number is found

    
    # Convert circle locations to nearest location on walking route
    def circle_pts_conversion(points):

        converted_list = []

        for point in points:

            # If the circle locates at the bottom of the venue, where visitors can't walk behind the circle as a wall is there, not walking path
            # i.e. circle y-coords is lower than y-max of walking paths
            # Set the converted point to the closest point where visitor can face directly to the circle, not nearest point
            if np.digitize(point[1], test_y_row) == len(test_y_row):
                converted_list.append((point[0], test_y_row[-1]))

            else:
                min_x_dist = max(test_x_row)
                min_x_bin = 0
                min_y_dist = max(test_y_row)
                min_y_bin = 0

                for i in range(len(test_x_row)):
                    if abs(test_x_row[i] - point[0]) < min_x_dist:
                        min_x_dist = abs(test_x_row[i] - point[0])
                        min_x_bin = i

                for j in range(len(test_y_row)):
                    if abs(test_y_row[j] - point[1]) < min_y_dist:
                        min_y_dist = abs(test_y_row[j] - point[1])
                        min_y_bin = j

                print(test_x_row[min_x_bin], min_x_dist, test_y_row[min_y_bin], min_y_dist)

                # if min_x_dist is closer to bin line
                if min_x_dist < min_y_dist:
                    converted_list.append((test_x_row[min_x_bin], point[1]))
                
                else:
                    converted_list.append((point[0], test_y_row[min_y_bin]))

        return converted_list

    def enter(self, route_dict, current, end, route, dist, layer):

        print("entered:", current)

        #update route
        route.append(current)
        layer += 1

        # Limit recursion depth: it can't exceed 4 using the simplified map:
        if layer == 5:
            return [], 100000000

        min_dist = -1
        min_route = []

        for new_coords in route_dict[current]:

            if new_coords in route:
                continue

            # If new position is the destination, avoid recursion

            if end == new_coords:
                
                temp_dist = dist + abs(sum(np.subtract(current, new_coords)))
                temp_route = route[:]
                temp_route.append(new_coords)
                if min_dist < 0 or temp_dist < min_dist:
                    min_dist = temp_dist
                    min_route = temp_route

                print("reach end", min_dist, min_route, dist)
                return min_route, min_dist

            # If new position is not the destination, do recursion

            else:
                temp_route, temp_dist = self.enter(route_dict, new_coords, end, route[:], dist + abs(sum(np.subtract(current, new_coords))), layer)

                # if min_dist == 100000000 and temp_dist < min_dist:
                #     print("found!!", min_dist, temp_dist, min_route, layer)

                if (min_dist < 0 or temp_dist < min_dist) and temp_dist >= 0:

                    if min_dist == 100000000:
                        print(temp_dist, min_dist)

                    # print(min_dist)
                    min_dist = temp_dist
                    min_route = temp_route

                
        
        print(route_dict[current], min_route, min_dist, layer)

        return min_route, min_dist


    def gen_route_dict(test_x_row, test_y_row):

        route_dict = {}
        id_list = []

        # Generate route dict
        for i in range(len(test_x_row)):
            for j in range(len(test_y_row)):
                id_list.append((i, j))

        for id_pair in id_list:

            i, j = id_pair[0], id_pair[1]
            current_coord = (test_x_row[i], test_y_row[j])
            
            if current_coord not in route_dict:
                route_dict[current_coord] = []

            if i-1 >= 0:
                route_dict[current_coord].append((test_x_row[i-1], test_y_row[j]))
            if i+1 < len(test_x_row):
                route_dict[current_coord].append((test_x_row[i+1], test_y_row[j]))
            if j-1 >= 0:
                route_dict[current_coord].append((test_x_row[i], test_y_row[j-1]))
            if j+1 < len(test_y_row):
                route_dict[current_coord].append((test_x_row[i], test_y_row[j+1]))

        return route_dict


    # modify route_dict after adding start/end points to map
    def modify_route_dict(route_dict, add_pt, test_x_row, test_y_row):
        # test_x_row = [0] + test_x_row

        x, y = add_pt

        if x not in test_x_row:
            bin_id = np.digitize(x, test_x_row)

            # print(x, y,  test_x_row[bin_id-1],  test_x_row[bin_id])
            # print(test_x_row)
            # print(route_dict)

            if bin_id == 0:
                return route_dict, test_x_row[bin_id] - x
            
            # if bin_id == len(test_x_row):
            #     return route_dict, x - test_x_row[bin_id]

            print("now", x, y, bin_id)
            print("nec", route_dict[(test_x_row[bin_id-1], y)], (test_x_row[bin_id], y))

            # remove route intercepted by start point
            # add route due to start point
            route_dict[(test_x_row[bin_id-1], y)].remove((test_x_row[bin_id], y))
            route_dict[(test_x_row[bin_id-1], y)].append(add_pt)

            route_dict[(test_x_row[bin_id], y)].remove((test_x_row[bin_id-1], y))
            route_dict[(test_x_row[bin_id], y)].append(add_pt)

            route_dict[add_pt] = []
            route_dict[add_pt].append((test_x_row[bin_id-1], y))
            route_dict[add_pt].append((test_x_row[bin_id], y))

        if y not in test_y_row:
            bin_id = np.digitize(y, test_y_row)

            if bin_id == 0:
                return route_dict, test_y_row[bin_id] - y
            
            # if bin_id == len(test_x_row):
            #     return route_dict, y - test_y_row[bin_id]

            # remove route intercepted by start point
            # add route due to start point

            print("now", x, y)
            print("nec", route_dict[(x, test_y_row[bin_id-1])], (x, test_y_row[bin_id]))

            route_dict[(x, test_y_row[bin_id-1])].remove((x, test_y_row[bin_id]))
            route_dict[(x, test_y_row[bin_id-1])].append(add_pt)

            route_dict[(x, test_y_row[bin_id])].remove((x, test_y_row[bin_id-1]))
            route_dict[(x, test_y_row[bin_id])].append(add_pt)

            route_dict[add_pt] = []
            route_dict[add_pt].append((x, test_y_row[bin_id-1]))
            route_dict[add_pt].append((x, test_y_row[bin_id]))

        return route_dict, 0
    
    def optimal_route_multipt(points, all_dict):

        print("calculating...")

        hist = {(0, ): 0} # record all routes explored, {(route): dist}
        queue = [(0, x) for x in range(len(points))]

        count = 0

        while True:

            # Find route with shortest distance, accessing last point
            # Handle multiple route with same minimum distance
            current_dist = min(hist.values())
            min_keys = [k for k in hist if hist[k] == current_dist]

            # print(min_keys, hist[min_keys[0]])

            # print(min_keys)

            for current_route in min_keys:
                # print(current_route)
                current_pt = current_route[-1]

                queue = [(current_pt, x) for x in range(len(points))]

                # Find all distances in queue
                for x in queue:
                    count += 1

                    # Skip route with same start and end
                    if x[0] == x[1] or x[1] in current_route:
                        continue

                    hist[current_route + (x[1], )] = current_dist + all_dict[x][1]
                    # min_dists.append(current_dist + all_dict[x][1])

                # remove this route from hist as it has been expanded.
                # Avoid removing history of full routes
                if len(current_route) != len(points):
                    hist.pop(current_route)

                else:
                    if hist[current_route] == min(hist.values()):
                        return hist, current_route

    def twopt_search(points, all_dict, search_pt = 2):

        hist = {(0, ): 0} # record all routes explored, {(route): dist}
        queue = [(0, x) for x in range(len(points))]

        count = 0

        while True:

            # Find route with shortest distance, accessing last point
            # Handle multiple route with same minimum distance
            current_dist = min(hist.values())
            min_keys = [k for k in hist if hist[k] == current_dist]

            for current_route in min_keys:
                
                current_pt = current_route[-1]  # current point is the rightmost node in key

                # possible routes to be explored
                # If current route is a full route, queue is an empty list
                queue = [(current_pt, dest) for dest in range(len(points))\
                        if (current_pt, dest) in all_dict and dest not in current_route]

                # Find min 2 dists in all possible routes
                min_dists_to_explore = sorted([all_dict[x][1] for x in queue])[:search_pt]

                # Find those routes with any of these min 2 dists
                queue = [x for x in queue
                        if all_dict[x][1] in min_dists_to_explore]

                # Find all distances in queue
                for x in queue:
                    count += 1

                    # Skip route with same start and end
                    if x[0] == x[1] or x[1] in current_route:
                        continue

                    hist[current_route + (x[1], )] = current_dist + all_dict[x][1]
                    # min_dists.append(current_dist + all_dict[x][1])

                # remove this route from hist as it has been expanded.
                # Avoid removing history of full routes
                
                if len(current_route) != len(points):
                    hist.pop(current_route)

                else:
                    print(len(current_route), len(points))
                    if hist[current_route] == min(hist.values()):
                            return hist, current_route, count
                    

    def visualize(circle_points, points, current_route, all_dict):
        print(current_route)

        img = np.zeros((3000,5000,3), dtype=np.uint8)

        for row in data:
            for coords in data[row].values():

                img = cv2.circle(img, tuple([int(x) for x in coords]), 10, (255, 255, 0), -1)

        # # Plot all row labels
        # row_center_list = [int(x)+30 for x in x_bins1]
        # for i in range(len(row_center_list)):

        #     img = cv2.putText(img, CHAR_LIST_ROW1[i], (row_center_list[i], 1100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)

        # plot all nodes passed through
        for i in range(len(current_route)-1):
            print((current_route[i], current_route[i+1]))

            pts = all_dict[(current_route[i], current_route[i+1])][0]

            for pt in pts:
                img = cv2.circle(img, (pt[0], pt[1]), 25, (0, 255, 255), -1)

        # Plot all concerned circles
        for pt in points:
            img = cv2.circle(img, (pt[0], pt[1]), 25, (0, 0, 255), -1)

        # Plot all arrows

        for i in range(len(current_route)-1):

            color = (255/len(current_route)-1) * i

            pts = all_dict[(current_route[i], current_route[i+1])][0]

            for i in range(len(pts) - 1):
                img = cv2.arrowedLine(img, pts[i], pts[i+1], (255, 0, color), 20)

        # Plot all concerned circle points

        for pt in circle_points:

            img = cv2.circle(img, pt, 20, (0, 255, 0), -1)
            # img = cv2.putText(img, 'x', pt, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)

        # Plot start and end circle points

        for pt in [circle_points[0], circle_points[-1]]:

            img = cv2.circle(img, pt, 20, (255, 255, 255), -1)
            # img = cv2.putText(img, 'x', pt, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)

        img = img[1000:2500, 500:4500]
        img = cv2.resize(img, (400, 200), interpolation = cv2.INTER_LINEAR)

        return img


# Function for returning csv of all circles

@app.route("/return_whole_csv")
async def return_whole_csv():

    print("wasdf")

    try:
        ori_df = pd.read_csv("circle_list.csv")
        ori_df = ori_df.astype({"購入済み": 'Int32'})
        df = ori_df.to_html(index = False).replace("\n", "").replace("NaN", "")
        print(jsonify({"status":"OK",'result': df}))
        
        return jsonify({"status":"OK",'result': df})

    except Exception as e:
        print(e)

        return warning_msg




# # Function for returning csv of closest circle
# @app.route("/closest_circle/")
# async def closest_circle(request: Request):
#         input = await request.body()

#     # try:
#         currentRow, currentBooth = input.decode().split('\n')
#         currentBooth = currentBooth.zfill(2)

#         # Read csv, filtered bought circles away
#         ori_df = pd.read_csv("circle_list.csv")
#         ori_df = ori_df.astype({"購入済み": 'Int32'})
#         unbought_df = ori_df.loc[ori_df["購入済み"] == 0].reset_index(drop = True)

#         # Create circle row, booth, and point list
#         circle_row_list, circle_booth_list = [currentRow] + list(unbought_df["行"]),\
#                                 [Route_func.extract_first_number(x) for x in [currentBooth] + list(unbought_df["番"])]
        
#         circle_points = []   #initiate circle point list with current location
#         for i in range(len(circle_row_list)):
#             print(circle_booth_list[i], type(circle_booth_list[i]))
#             coords = data[circle_row_list[i]][circle_booth_list[i].zfill(2)]
#             circle_points.append([int(coords[0]), int(coords[1])])

#         points = Route_func.circle_pts_conversion(circle_points)

#         routeDictSelf = Route_func()

#         # For each start-dest combination, simplify the grid network and find the shortest path
#         all_dict = {}

#         for i in range(len(points)):
#             for j in range(len(points)):

#                 # test_x_row = [int(x) for x in x_bins2]
#                 # test_y_row = [0, int(y_max1), int(y_max2)]      

#                 if i == j:
#                     continue

#                 start = points[i]
#                 end = points[j]

#                 # If lie on same line of walking route, route_dict can't be modified using the following algorithm
#                 # When so, need to calculate the distance directly

#                 if start[0] == end[0] and start[0] in test_x_row:
#                     all_dict[(i, j)] = [(start, end), abs(start[1] - end[1])]
                
#                 elif start[1] == end[1] and end[1] in test_y_row:
#                     all_dict[(i, j)] = [(start, end), abs(start[0] - end[0])]

#                 else:
#                     print(start, end)
#                     concerned_xs, concerned_ys = Route_func.concerned_coords(test_x_row, test_y_row, start, end)
#                     route_dict = Route_func.gen_route_dict(concerned_xs, concerned_ys)

#                     for pt in [start, end]:
#                         route_dict, dist = Route_func.modify_route_dict(route_dict, pt, concerned_xs, concerned_ys)

#                     all_dict[(i, j)] = routeDictSelf.enter(route_dict, start, end, [], 0, -1)

#         hist, current_route = Route_func.optimal_route_multipt(points, all_dict)

#         print(current_route)
#         for x in current_route:
#             print(circle_row_list[x], circle_booth_list[x])


#         nodes_passed = []
#         # Find all nodes passed through
#         for i in range(len(current_route)-1):
#             nodes_passed.append(all_dict[(current_route[i], current_route[i+1])][0])

#         # if input to visualize
#         # if mapBool:
        
#             # img = Route_func.visualize(circle_points, points, current_route, all_dict)
#             # _, img_encoded = cv2.imencode('.png', img)
#             # b64 = base64.b64encode(img_encoded.tobytes()).decode('utf-8')

#         new_index_list = [x-1 for x in current_route if x != 0]

#         return_df = unbought_df.reindex(new_index_list).to_html(index = False).replace("\n", "").replace("NaN", "")


#         # else:
#         return {"df": return_df, "node_list": nodes_passed, "circle_points": circle_points[1:]}

#     # except:
#     #     return warning_msg





# # # Function for returning csv of closest circle
# # @app.post("/closest_circle/")
# # async def closest_circle(request: Request):
# #     input = await request.body()

# #     try:

# #         day, currentPos = input.decode().split('\n')

# #         # Filter df according to which day
# #         ori_df = pd.read_csv("circle_list.csv")
# #         ori_df = ori_df.astype({"購入済み": 'Int32'})
# #         temp_df = ori_df.loc[ori_df["何日目"] == int(day)].reset_index(drop = True)

# #         # Find row names in current row
# #         for row in [hall_1_row, hall_2_row, hall_3_row, hall_4_row, hall_5_row]:
# #             if currentPos in row:
# #                 current_hall_row = row
# #                 break

# #         # Find index of current position in row name string
# #         current_index = current_hall_row.find(currentPos)

# #         # Calculate distance to each circle
# #         dist_list = []
# #         other_hall_id_list = []

# #         # Loop through all rows in temp_df

# #         for csv_row_id, row_name in enumerate(temp_df["行"]):
# #             print(csv_row_id, row_name)
# #             index = current_hall_row.find(row_name)
# #             if index >= 0:   # If circle in same hall (row of all circles index can be found in row list)
# #                 print(row_name, current_index - index)

# #                 dist_list.append((csv_row_id, abs(current_index - index)))
# #             else:
# #                 other_hall_id_list.append(csv_row_id)

# #         # Sort according to distance for circles in same hall, create df for circles in other halls as well
# #         dist_list = sorted(dist_list, key=lambda x:x[1])
# #         df = temp_df.reindex([x[0] for x in dist_list])
# #         other_hall_df = temp_df.reindex([x for x in other_hall_id_list])

# #         # Generate table
# #         df = df.to_html(index = False).replace("\n", "").replace("NaN", "")
# #         other_hall_df = other_hall_df.to_html(index = False).replace("\n", "").replace("NaN", "")


# #         df += "<table>\
# #                 <tr><th colspan='6'>別のホール</th></tr>\
# #                 </table>" 
        
# #         df += other_hall_df

# #         return df

# #     except:
# #         return warning_msg


# Function for adding circle to csv
@app.post("/add_circle/")
async def add_circle():
    input = request.get_data()
    print(input)
    try:

        newCircle, newRow,newNumber  = input.decode().split('\n')
        print(input.decode().split('\n'))

        # add the info to csv
        ori_df = pd.read_csv("circle_list.csv")
        ori_df = ori_df.astype({"購入済み": 'Int32'})
        appendRow = pd.DataFrame({
        'サークル名': [newCircle],
        '行': [newRow],
        '番': [newNumber],
        '購入済み': ['0']
        })

        pd.concat([ori_df, appendRow], ignore_index=True).to_csv("circle_list.csv", index = False)

        return jsonify()

    except:
        return warning_msg

# # Function for adding circle to csv
# @app.post("/filter_table/")
# async def filter_table(request: Request):
#     form = await request.form()

#     try:
#         boughtList = form.get("checkedBoughtList").split(",")
#         boughtList = [int(x) for x in boughtList]
#         # filter csv
#         ori_df = pd.read_csv("circle_list.csv")
#         ori_df = ori_df.astype({"購入済み": 'Int32'})

#         df = ori_df[ori_df['購入済み'].isin(boughtList)]

#         df = df.to_html(index = False).replace("\n", "").replace("NaN", "")
#         print("WA")

#         return {"df": df}
    
#     except Exception as e:
#         print(e)
        
#         return warning_msg



# # Function for adding circle to csv
# @app.post("/change_bought_status/")
# async def change_bought_status(request: Request):
#     input = await request.body()

#     try:

#         circleName = input.decode()
#         ori_df = pd.read_csv("circle_list.csv")
#         ori_df = ori_df.astype({"購入済み": 'Int32'})
#         circledfIndex = ori_df.index[ori_df['サークル名'] == circleName].tolist()[0]

#         currentStatus = ori_df.loc[circledfIndex, '購入済み']
#         if currentStatus == 1:
#             currentStatus = 0
#         else:
#             currentStatus = 1

        
#         ori_df.loc[circledfIndex, '購入済み'] = currentStatus
#         ori_df.to_csv("circle_list.csv", index = False)

#     except:
#         return warning_msg

if __name__ == '__main__':
   app.run(debug=True, port=8000)
