import sys
import cv2
import os.path
import glob
import os


# グローーバル変数
drawing = False
complete_region = False
ix,iy,width,height = -1,-1,0,0





# マウスコールバック関数(正方形)
def my_mouse_callback_square(event,x,y,flags,param):
    global ix,iy,width,height,box,drawing,complete_region

    if event == cv2.EVENT_MOUSEMOVE:      # マウスが動いた時
        if(drawing == True):
            width = x - ix
            height = y - iy



            #オリジナルから追加した分            
            length = max(abs(width), abs(height))

            if width>=0:
                width = length
            else:
                width = -length

            if height>=0:
                height = length
            else:
                height = -length


    elif event == cv2.EVENT_LBUTTONDOWN:  # マウス左押された時
        drawing = True

        ix = x
        iy = y
        width = 0
        height = 0

    elif event == cv2.EVENT_LBUTTONUP:    # マウス左離された時
        drawing = False
        complete_region = True

        if(width < 0):
            ix += width
            width *= -1

        if(height < 0):
           iy += height
           height *= -1









def main(filename):
    num = 0
    global ix,iy,width,height,drawing,complete_region

    source_window = "draw_rectangle"

    img = cv2.imread(filename)  # 画像の読み込み
    img_original = img.copy()   #切り取り用の画像
    temp = img.copy()                # 画像コピー

    cv2.namedWindow(source_window)
    cv2.setMouseCallback(source_window, my_mouse_callback_square)

    while(1):
        cv2.imshow(source_window,temp)

        if(drawing):             # 左クリック押されてたら
            temp = img.copy()    # 画像コピー
            cv2.rectangle(temp,(ix,iy),(ix + width, iy+ height),(0,255,0),2)  # 矩形を描画


        if(complete_region): # 矩形の選択が終了したら
            complete_region = False

            cv2.rectangle(img,(ix,iy),(ix + width, iy+ height),(0,0,255),2)
            cv2.rectangle(temp,(ix,iy),(ix + width, iy+ height),(0,0,255),2)


            if width==0:
                continue

            roi = img_original[iy:iy+height, ix:ix+width] # 元画像から選択範囲を切り取り

            #画像を保存
            output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(filename))[0]+'_hand{0}.jpg'.format(num))
            cv2.imwrite(output_path,roi)
            num +=1

        # キー操作
        k = cv2.waitKey(1) & 0xFF
        if k == 27:          # esc押されたら終了
            cv2.destroyAllWindows()
            sys.exit()

        if k == 13:          # enter押されたら次へ
            break

        elif k ==ord('s'):   # 's'押されたら進行状況を保存
            print(filename)
            with open("save.txt", "w") as f:
                f.write(filename)


    cv2.destroyAllWindows()




#過去のセーブを読み込む
def open_save():
    if not os.path.exists("save.txt"):
        return False

    with open("save.txt", "r") as f:
        last_img = f.read()
    return last_img


#セーブ内容から始めるようにする
def list_posision(last_img, files):
    if last_img == False:
        return 0
    for i, file in enumerate(files):
        if file == last_img:
            return i




output_dir = "./hand_cut_images/"
imgs_dir = "./painted_images/*"
files = glob.glob(imgs_dir)

del files[0:list_posision(open_save(), files)]
for filename in files:
    main(filename)


