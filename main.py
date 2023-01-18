from PIL import Image, ImageDraw, ImageFont
import time
import random 
import cv2 as cv
import numpy as np
from colorsys import hsv_to_rgb
from Blocks import Blocks
from Character import Character
from Joystick import Joystick

# 블록 색상 info 초기화
block_info = [[random.randint(0,4) for i in range(7)] for j in range(7)]
#블록 위치값 지정
block_gps = [((20, 30),(45,30),(70,30),(95,30),(120,30),(145,30),(170,30)),
            ((20, 55),(45,55),(70,55),(95,55),(120,55),(145,55),(170,55)),
            ((20, 80),(45,80),(70,80),(95,80),(120,80),(145,80),(170,80)),
            ((20, 105),(45,105),(70,105),(95,105),(120,105),(145,105),(170,105)),
            ((20, 130),(45,130),(70,130),(95,130),(120,130),(145,130),(170,130)),
            ((20, 155),(45,155),(70,155),(95,155),(120,155),(145,155),(170,155)),
            ((20, 180),(45,180),(70,180),(95,180),(120,180),(145,180),(170,180))]
#색상값 지정
colors=["#00FF00","#0000FF","#FF0000","#FF00FF","#FFFF00","#D3D3D3","#FFFFFF"]
#블록 각각의 값 조합  
block_list  = [[Blocks(block_gps[i][j],block_info[i][j]) for j in range(7)] for i in range(7)]

#죽은 블록 판별시 호출, 죽은 블록 자리를 채워줄 블록을 한칸씩 아래로 내려주는 함수
def ck_black():
    ck2=1            
    while(ck2!=0):
        ck2=0
        for i in range(7):
            for j in range(7):
                if(block_info[i][j]==6):
                    ck2=1
                    if(i-1>=0):
                        block_info[i][j]=block_info[i-1][j]
                        block_info[i-1][j]=6
                        block_list[i][j].setcolor(block_info[i][j])
                        block_list[i-1][j].setcolor(block_info[i-1][j])
                    else:
                        block_info[i][j]=random.randint(0,4)
                        block_list[i][j].setcolor(block_info[i][j]) 

        print_block()

#블록 색상 업데이트 함수
def block_update():
    for i in range(7):
        for j in range(7):
            block_list[i][j].setcolor(block_info[i][j])

#블록 출력함수(과정 출력)
def print_block():
    ck2=1
    joystick = Joystick()
    my_image = Image.new("RGB", (joystick.width, joystick.height))
    my_draw = ImageDraw.Draw(my_image)
    while(ck2!=0):
        ck2=0
        block_update()
        for i in range(0,7):
            for blocks in block_list[i]:
                if blocks.state != 'die':
                    my_draw.ellipse(tuple(blocks.position),outline = blocks.outline, fill = blocks.inline )# #FF0000
                else:
                    my_draw.ellipse(tuple(blocks.position),outline = "#000000", fill = "#000000" )# #FF0000
       
    joystick.disp.image(my_image)

#매칭되는 블록이 있는지 검사하는 함수
def blocks_ck_all():
    ck=1
    tmp_score=0
    while(ck!=0):
        ck=0
        for i in range(7):
            if(ck==1):
                break
            for j in range(7):
                if(block_info[i][j]==6):# 이미 매칭되어 죽은 블록이 있을경우
                    ck_black()
                    ck=1
                    break                     
                else: 
                    if(j<5):#j는 0~6 범위이고 j+1,j+2와 비교하므로 j<5까지.   
                        if(block_info[i][j]==block_info[i][j+1] and block_info[i][j+1]==block_info[i][j+2]):
                            #3개 매칭잡으면... 가로 매칭
                            if(j<3):
                                if(block_info[i][j]==block_info[i][j+3] and block_info[i][j+1]==block_info[i][j+4]):
                                    #5개 일자 매칭일 경우... 
                                    block_info[i][j]=6
                                    block_info[i][j+1]=6
                                    block_info[i][j+2]=5
                                    block_info[i][j+3]=6
                                    block_info[i][j+4]=6
                                    block_list[i][j].state='die'
                                    block_list[i][j+1].state='die'
                                    block_list[i][j+3].state='die'
                                    block_list[i][j+4].state='die'
                                    tmp_score+=1000
                                    ck=1
                                    break
                            if(i<5):
                                for k in range(3):
                                    if(block_info[i][j]==block_info[i+1][j+k] and block_info[i][j]==block_info[i+2][j+k]):
                                        #5개 매칭 고려, for문 통한 if문
                                        block_info[i][j]=5
                                        block_info[i][j+1]=6
                                        block_info[i][j+2]=6
                                        block_info[i+1][j+k]=6
                                        block_info[i+2][j+k]=6
                                        block_list[i][j+1].state='die'
                                        block_list[i][j+2].state='die'
                                        block_list[i+1][j+k].state='die'
                                        block_list[i+2][j+k].state='die'
                                        tmp_score+=1000
                                        ck=1
                                        break
                            #추가적인 일치값이 없을때...       
                            block_info[i][j]=6
                            block_info[i][j+1]=6
                            block_info[i][j+2]=6
                            block_list[i][j].state='die'
                            block_list[i][j+1].state='die'
                            block_list[i][j+2].state='die'
                            tmp_score+=300
                            ck=1
                            break 
                    if(i<5):#i는 0~6 범위이고 i+1,i+2와 비교하므로 i<5까지.
                        if( block_info[i][j]==block_info[i+1][j] and block_info[i+1][j]==block_info[i+2][j]):
                            #3개 매칭잡으면... 세로 매칭
                            if(i<3):
                                if(block_info[i][j]==block_info[i+3][j] and block_info[i][j]==block_info[i+4][j]):
                                    #5개 일자 매칭일 경우...
                                    block_info[i][j]=6
                                    block_info[i+1][j]=6
                                    block_info[i+2][j]=5
                                    block_info[i+3][j]=6
                                    block_info[i+4][j]=6
                                    block_list[i][j].state='die'
                                    block_list[i+1][j].state='die'
                                    block_list[i+3][j].state='die'
                                    block_list[i+4][j].state='die'
                                    tmp_score+=1000
                                    ck=1
                                    break
                            if(j<5):
                                for k in range(1,3):
                                    if(block_info[i][j]==block_info[i+k][j+1] and block_info[i][j]==block_info[i+k][j+2]):
                                        #5개 매칭 고려, for문 통한 if문
                                        block_info[i][j]=5
                                        block_info[i+k][j+1]=6
                                        block_info[i+k][j+2]=6
                                        block_info[i+1][j]=6
                                        block_info[i+2][j]=6
                                        block_list[i+k][j+1].state='die'
                                        block_list[i+k][j+2].state='die'
                                        block_list[i+1][j].state='die'
                                        block_list[i+2][j].state='die'
                                        tmp_score+=1000
                                        ck=1
                                        break
                            if(j>1):# 위 for문으로 커버하지 못한 모양들
                                for k in range(1,3):
                                    if(block_info[i][j]==block_info[i+k][j-1] and block_info[i][j]==block_info[i+k][j-2]):
                                        block_info[i][j]=5
                                        block_info[i+k][j-1]=6
                                        block_info[i+k][j-2]=6
                                        block_info[i+1][j]=6
                                        block_info[i+2][j]=6
                                        block_list[i+k][j-1].state='die'
                                        block_list[i+k][j-2].state='die'
                                        block_list[i+1][j].state='die'
                                        block_list[i+2][j].state='die'
                                        tmp_score+=1000
                                        ck=1
                                        break
                            if(j>0 and j<6):
                                for k in range(1,3):
                                    if(block_info[i][j]==block_info[i+k][j+1] and block_info[i][j]==block_info[i+k][j-1]):
                                        block_info[i][j]=5
                                        block_info[i+k][j+1]=6
                                        block_info[i+k][j-1]=6
                                        block_info[i+1][j]=6
                                        block_info[i+2][j]=6
                                        block_list[i+k][j+1].state='die'
                                        block_list[i+k][j-1].state='die'
                                        block_list[i+1][j].state='die'
                                        block_list[i+2][j].state='die'
                                        tmp_score+=1000
                                        ck=1
                                        break
                            #추가적인 일치값이 없을때... 
                            block_info[i][j]=6
                            block_info[i+1][j]=6
                            block_info[i+2][j]=6
                            block_list[i][j].state='die'
                            block_list[i+1][j].state='die'
                            block_list[i+1][j].state='die'
                            tmp_score+=300
                            ck=1
                            break
    return tmp_score

def main():
    joystick = Joystick()
    my_image = Image.new("RGB", (joystick.width, joystick.height))
    my_draw = ImageDraw.Draw(my_image)
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(255, 0, 0, 100))
    joystick.disp.image(my_image)
   
    my_circle = Character(joystick.width-50, joystick.height-30)
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))

    score = 0
    ck1=1
    #첫화면 블록 초기화 과정, 처음부터 매칭되는 블록이 있는상태로 출력되지 않도록 함.
    while(ck1!=0):
        ck1=0
        for i in range(7):
            for j in range(7):
                if(j<5):
                    if(block_info[i][j]!=6 and block_info[i][j]==block_info[i][j+1] and block_info[i][j+1]==block_info[i][j+2]):
                        block_info[i][j]=6
                        block_info[i][j+1]=6
                        block_info[i][j+2]=6
                        ck1=1
                if(i<5):                
                    if(block_info[i][j]!=6 and block_info[i][j]==block_info[i+1][j] and block_info[i+1][j]==block_info[i+2][j]):
                        block_info[i][j]=6
                        block_info[i+1][j]=6
                        block_info[i+2][j]=6
                        ck1=1
        ck2=1            
        while(ck2!=0):
            ck2=0
            for i in range(7):
                for j in range(7):
                    if(block_info[i][j]==6):
                        ck2=1
                        if(i-1>=0):
                            block_info[i][j]=block_info[i-1][j]
                            block_info[i-1][j]=6
                            block_list[i][j].setcolor(block_info[i][j])
                            block_list[i-1][j].setcolor(block_info[i-1][j])
                        else:
                            block_info[i][j]=random.randint(0,4)
                            block_list[i][j].setcolor(block_info[i][j]) 
 
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (0, 0, 0, 100))
    joystick.disp.image(my_image)
    #main loop문
    while True:
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        #컨트롤러 조작으로 인한 이동
        if not joystick.button_U.value:  # up pressed
            command['up_pressed'] = True
            command['move'] = True

        if not joystick.button_D.value:  # down pressed
            command['down_pressed'] = True
            command['move'] = True

        if not joystick.button_L.value:  # left pressed
            command['left_pressed'] = True
            command['move'] = True

        if not joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True
        #폭탄 생성 코드, 폭탄생성 조건인 5개 매칭이 실력적으로 힘들어 만든 임시 코드, 치트성플레이
        if not joystick.button_B.value: # B pressed
            block_info[3][3]=5
            block_list[3][3].setcolor(block_info[3][3])
            print_block()
        #블록 선택 코드
        if not joystick.button_A.value: # A pressed
            while True:
                p = my_circle.xy
                y=int(p[1])
                x=int(p[0])
                print(p)
                #B 버튼을 통해 폭탄 작동
                if not joystick.button_B.value: # B pressed
                    if(block_info[y][x]==5):
                        y_min = y-1 if y>0 else y
                        y_max = y+2 if y<6 else y+1
                        x_min = x-1 if x>0 else x
                        x_max = x+2 if x<6 else x+1  
                        for i in range(y_min,y_max):
                            for j in range(x_min,x_max):
                                block_info[i][j]=6
                                block_list[i][j].state='die'
                                score+=2500
                                print(score)
                        t_score=0
                        t_score=blocks_ck_all()
                        score+=t_score
                        print(score)
                        print_block()
                if not joystick.button_U.value:  # up pressed
                    if(y>0):#위로 바꾸고(y==0일 경우 바꿀수 없으므로)
                        tmp_c=block_info[y][x]
                        block_info[y][x]=block_info[y-1][x]
                        block_info[y-1][x]=tmp_c
                        print_block()
                        t_score=0
                        t_score=blocks_ck_all()#블록 매칭 검사후 추가점수 값 리턴
                        score+=t_score
                        print(score)
                        print_block()                           
                        if(t_score==0):#매칭된 블록이 없어 추가점수가 나지 않으면 되돌리기
                            tmp_c1=block_info[y][x]
                            block_info[y][x]=block_info[y-1][x]
                            block_info[y-1][x]=tmp_c1
                            print_block()
                    break

                if not joystick.button_D.value:  # down pressed
                    if(y<6):
                        tmp_c=block_info[y][x]
                        block_info[y][x]=block_info[y+1][x]
                        block_info[y+1][x]=tmp_c
                        print_block()
                        t_score=0
                        t_score=blocks_ck_all()
                        score+=t_score
                        print(score)
                        print_block()                           
                        if(t_score==0):
                            tmp_c1=block_info[y][x]
                            block_info[y][x]=block_info[y+1][x]
                            block_info[y+1][x]=tmp_c1
                            print_block()
                    break

                if not joystick.button_L.value:  # left pressed
                    if(x>0):
                        tmp_c=block_info[y][x]
                        block_info[y][x]=block_info[y][x-1]
                        block_info[y][x-1]=tmp_c
                        print_block()
                        t_score=0
                        t_score=blocks_ck_all()
                        score+=t_score
                        print(score)
                        print_block()                           
                        if(t_score==0):
                            tmp_c1=block_info[y][x]
                            block_info[y][x]=block_info[y][x-1]
                            block_info[y][x-1]=tmp_c1
                            print_block()
                    break

                if not joystick.button_R.value:  # right pressed
                    if(x<6):
                        tmp_c=block_info[y][x]
                        block_info[y][x]=block_info[y][x+1]
                        block_info[y][x+1]=tmp_c
                        print_block()
                        t_score=0
                        t_score=blocks_ck_all()
                        score+=t_score
                        print(score)
                        print_block()                           
                        if(t_score==0):
                            tmp_c1=block_info[y][x]
                            block_info[y][x]=block_info[y][x+1]
                            block_info[y][x+1]=tmp_c1
                            print_block()
                    break
                
        my_circle.move(command)
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (0, 0, 0, 100))
        my_draw.rectangle(tuple(my_circle.position), outline = my_circle.outline, fill = (0, 0, 0,100))
        
        #과정이 끝난후의 출력
        for i in range(0,7):
            for blocks in block_list[i]:
                if blocks.state != 'die':
                    my_draw.ellipse(tuple(blocks.position),outline = blocks.outline, fill = blocks.inline )# #FF0000
                else:
                    my_draw.ellipse(tuple(blocks.position),outline = "#000000", fill = "#000000" )# #FF0000
        #점수 출력
        my_draw.text((200,20),'score',"#FFFFFF")
        my_draw.text((200,30),str(score),"#FFFFFF")
      
        joystick.disp.image(my_image) #모두 담아서 출력(앞 출력들을 모아 출력)
        time.sleep(0.05)#컨트롤러의 빠른 이동으로 인한 속도제한.


if __name__ == '__main__':
    main()