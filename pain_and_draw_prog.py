import numpy as np
import cv2 as cv

def mouse_event_handler(event, x, y, flags, param):
    # Change 'mouse_state' (given as 'param') according to the mouse 'event'
    if event == cv.EVENT_LBUTTONDOWN:
        param[0] = True
        param[1] = (x, y)
    elif event == cv.EVENT_LBUTTONUP:
        param[0] = False
    elif event == cv.EVENT_MOUSEMOVE and param[0]:
        param[1] = (x, y)

def free_shape(canvas):
    img = canvas
    
    cv.rectangle(img, (0,0),(900,500),(255,225,85), -1)
    cv.rectangle(img, (0,500),(900,600),(75,180,70), -1)
    
    cv.circle(img, (200,150), 60, (0,255,255), -1)
    cv.circle(img, (200,150), 75, (220,255,255), 10)
    
    cv.line(img, (710, 500), (710, 420), (30,65,155), 15)
    
    triangle2 = np.array([[640,460],[780,460], [710,200]], dtype=np.int32)
    cv.fillPoly(img, [triangle2], (75,180,70))
    
    cv.line(img, (600, 500), (600, 420), (30,65,155), 25)
    
    triangle = np.array([[500,440],[700,440], [600,75]], dtype=np.int32)
    cv.fillPoly(img, [triangle], (75,200,70))
    
    return img
    

def free_drawing(canvas_width=900, canvas_height=600, init_brush_radius=3):
    canvas = np.full((canvas_height, canvas_width, 3), 255, dtype=np.uint8)
    palette = [(0, 0, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    
    canvas = free_shape(canvas)

    mouse_state = [False, (-1, -1)]
    brush_color = 0
    brush_radius = init_brush_radius

    cv.namedWindow('Free Drawing')
    cv.setMouseCallback('Free Drawing', mouse_event_handler, mouse_state)

    while True:
        mouse_left_button_click, mouse_xy = mouse_state
        if mouse_left_button_click:
            cv.circle(canvas, mouse_xy, brush_radius, palette[brush_color], -1)

        canvas_copy = canvas.copy()
        info = f'Brush Radius: {brush_radius}'
        cv.putText(canvas_copy, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (127, 127, 127), thickness=2)
        cv.putText(canvas_copy, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, palette[brush_color])
        cv.imshow('Free Drawing', canvas_copy)

        key = cv.waitKey(1)
        if key == 27:
            break
        elif key == ord('\t'):
            brush_color = (brush_color + 1) % len(palette)
        elif key == ord('+') or key == ord('='):
            brush_radius += 1
        elif key == ord('-') or key == ord('_'):
            brush_radius = max(brush_radius - 1, 1)

    cv.destroyAllWindows()

if __name__ == '__main__':
    free_drawing()