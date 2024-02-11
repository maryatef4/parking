import cv2
import numpy as np
import cvzone
import pickle

cap = cv2.VideoCapture("easy.mp4")
drawing = False
area_names = []
try:
    with open ("saved","rb") as f:
        data = pickle.load(f)
        shapes,area_names = data["shapes"],data["area_names"]
except:
   shapes = []
 
points = []
current_name =" "

# def draw(event,x,y,flags,param):
#     global  points,drawing,polylines
#     drawing = True
#     if event == cv2.EVENT_LBUTTONDOWN:
#         # current_name = input("areaname: ")
#         # if current_name:
#         #     #  points.append((x,y))
#             points = [(x,y)]
#             # area_names.append(current_name)
#     elif event == cv2.EVENT_MOUSEMOVE:
#         if drawing:
#             points.append((x,y))
#     elif event == cv2.EVENT_LBUTTONUP:
#         drawing = False
#             # drawing = False
#         current_name = input('area_name: ')
#         if current_name:
#             area_names.append(current_name)
#             polylines.append(np.array(points,np.int32))
            
#             # for i,point in enumerate(points):
#             #     x1,y1 = point
#             #     if x1<x<x1+width and y1<y<y1+height:
#             #         points.pop(i)
#     elif event == cv2.EVENT_RBUTTONDOWN:
#     # Create a new list to store the polylines you want to keep
#         updated_polylines = []
#         for i, polyline in enumerate(polylines):
#             # Extract the contour from the polyline
#             contour = polyline
#             # Ensure the contour is a 2D numpy array
#             contour = contour.reshape((-1, 2))
#             # Check if the right-click is inside the contour
#             if contour.size > 0 and cv2.pointPolygonTest(contour, (x, y), False) >= 0:
#                 continue
#             # If not inside, add the polyline to the updated list
#             updated_polylines.append(polyline)
#         # Update the original list with the new list
#         polylines = updated_polylines

current_shape = []

def draw_line(event, x, y, flags, param):
    global shapes, current_shape

    if event == cv2.EVENT_LBUTTONDOWN:
        current_shape.append((x, y))
        if len(current_shape) == 4:
            shapes.append(np.array(current_shape))
            current_shape = []
            current_name = input('area_name: ')
            if current_name:
                area_names.append(current_name)
    

    elif event == cv2.EVENT_RBUTTONDOWN:
        updated_shapes= []
        for i, shape in enumerate(shapes):
            contour = shape.reshape((-1, 2))
            if contour.size > 0 and cv2.pointPolygonTest(contour, (x, y), False) >= 0:
                continue
            updated_shapes.append(shape)
        shapes = updated_shapes




cv2.namedWindow("FRAME")
cv2.setMouseCallback("FRAME", draw_line)


while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    frame=cv2.resize(frame,(1020,500))
    for i,shape in enumerate(shapes):
        cvzone.putTextRect(frame,f"{area_names[i]}",tuple(shape[0]),1,1)
   
     # Draw existing shapes
    for shape in shapes:
        cv2.polylines(frame, [shape], isClosed=True, color=(0, 255, 0), thickness=2)

    # Draw the current shape being drawn
    if len(current_shape) > 1:
        cv2.polylines(frame, [np.array(current_shape)], isClosed=False, color=(0, 0, 255), thickness=2)

    Key = cv2.waitKey(100) & 0xFF
    if Key == ord('s'):
        with open ("saved","wb") as f:
            data = {"shapes":shapes, "area_names":area_names }
            pickle.dump(data,f)
    cv2.imshow("FRAME", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Press 'Esc' to exit
        break
   

cap.release()
cv2.destroyAllWindows()
