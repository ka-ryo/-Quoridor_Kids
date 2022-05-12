from distutils.log import info
from tkinter.constants import E
from tkinter.tix import Tree
from turtle import Turtle, color
import numpy as np
import math
import tkinter as tk
import random
import time
import copy

class State(tk.Frame):
    
    def __init__(self,master=None,model=None):
        

        #番手のPlayerを把握(Red or Yellow)
        self.Player_Color = "#FF0000"
        #クリック位置
        self.x = 0
        self.y = 0

        #ゲーム情報
        self.Player_A = "Player"
        self.Player_B = "CPU"
        self.Turn = 0
        self.Turn_Change = True
        self.Win = False

        #壁の枚数
        self.Player_Count_Wall =[8,8]

        #盤面用変数
        self.width = 7
        self.height = 7

        #駒の位置
        self.Player_Piece_Place = [[0,3],[6,3]]
        # self.Player_Piece_Place = [[1,2],[1,3]]
        
        #ゴールのマス
        self.A_Goal = []
        for i in range(self.height):
            self.A_Goal.append([self.width -1 ,i])
            
        self.B_Goal = []
        for i in range(self.height):
            self.B_Goal.append([0 ,i])
        

        #マス用リスト
        self.Mas_List = []

        for _ in range(self.width):
            tmp_list = []
            for _ in range(self.height):
                tmp_list.append(Mass_Info())
            self.Mas_List.append(tmp_list)
        
        #初期位置の設定
        #Player1
        self.Mas_List[self.Player_Piece_Place[0][0]][self.Player_Piece_Place[0][1]].Piece_Exsist = True
        self.Mas_List[self.Player_Piece_Place[0][0]][self.Player_Piece_Place[0][1]].Piece_self = "Red"

        #Player2
        self.Mas_List[self.Player_Piece_Place[1][0]][self.Player_Piece_Place[1][1]].Piece_Exsist = True
        self.Mas_List[self.Player_Piece_Place[1][0]][self.Player_Piece_Place[1][1]].Piece_self = "Blue"

        #通路用リスト
        self.Width_Path_List = []

        for _ in range(self.width+1):
            tmp_list = []
            for _ in range(self.height):
                tmp_list.append(Path_Info())
            self.Width_Path_List.append(tmp_list)

        self.Height_Path_List = []

        for _ in range(self.width+1):
            tmp_list = []
            for _ in range(self.height):
                tmp_list.append(Path_Info())
            self.Height_Path_List.append(tmp_list)              

        #デバッグ用
        # self.Width_Path_List[3][0].Wall_Exsist = True
        # self.Width_Path_List[4][0].Wall_Exsist = True
        # self.Height_Path_List[1][3].Wall_Exsist = True
        # self.Height_Path_List[2][3].Wall_Exsist = True

        #キャンバスの生成
        tk.Frame.__init__(self,master)
        self.c = tk.Canvas(self,width=750,height=600,highlightthickness=0)

        self.start_x = tk.StringVar()
        self.start_y = tk.StringVar()    

        self.c.bind('<Button-1>',self.Click_Event)
        self.c.pack()

        #ゲーム進行時に必要なテキスト
        self.geme_txt = tk.StringVar()
        self.geme_txt.set("")

        #ターン表示用
        self.Turn_txt = tk.StringVar()
        self.Turn_txt.set("Red")

        self.on_draw()

                 

    def Move_Piece(self,Before,After):
        #盤面情報の更新
        self.Mas_List[After[0]][After[1]].Piece_Exsist = self.Mas_List[Before[0]][Before[1]].Piece_Exsist
        self.Mas_List[After[0]][After[1]].Piece_self = self.Mas_List[Before[0]][Before[1]].Piece_self  

        #駒位置情報の更新
        self.Player_Piece_Place[self.Turn%2][0] = After[0]
        self.Player_Piece_Place[self.Turn%2][1] = After[1]

        self.Mas_List[Before[0]][Before[1]].Piece_Exsist = False
        self.Mas_List[Before[0]][Before[1]].Piece_self = None

    #状況を一旦リセット
    def Reset_State(self):
        self.Turn_Change = False
        self.flag_Wall = False
        self.flag_Piece= False
        #壁選択時に記録
        self.Choice_Path_List = []  
        self.geme_txt.set("...")   


    #盤面の描画
    def on_draw(self):
        self.ini_x = 200
        self.ini_y = 90
        self.Mass_size = 50
        
        self.c.delete('all')
        
        #リセットボタン
        button = tk.Button(text="リセット",font=("",18), command=self.Reset_State).place(x = 60, y = 480)
        
       
        #横線の描画
        for x in range(self.width+1):
            for y in range(self.height):
                color = 'Black'
                if  self.Width_Path_List[x][y].Wall_Exsist:
                    color = 'Red'

                self.c.create_line(self.ini_x+(y*self.Mass_size),self.ini_y+x*self.Mass_size,self.ini_x+(y*self.Mass_size+self.Mass_size),self.ini_y+x*self.Mass_size,width=2.0,fill=color)
        
        #縦線の描画
        for x in range(self.width+1):
            for y in range(self.height):
                color = 'Black'
                if  self.Height_Path_List[x][y].Wall_Exsist:
                    color = 'Red'

                self.c.create_line(self.ini_x+x*self.Mass_size,self.ini_y+(y*self.Mass_size),self.ini_x+x*self.Mass_size,self.ini_y+(y*self.Mass_size+self.Mass_size),width=2.0,fill= color)
        
        #駒の描画
        for x,tmp in enumerate(self.Mas_List):
            for y,Mas_info in enumerate(tmp):
                if Mas_info.Piece_Exsist:
                    self.c.create_oval(self.ini_x+self.Mass_size*x+7.5,self.ini_y+self.Mass_size*y+7.5,self.ini_x+self.Mass_size*x+40,self.ini_y+self.Mass_size*y+40,fill=Mas_info.Piece_self)
                

        #壁の描画
        #Player A
        self.c.create_rectangle(20, self.ini_y + self.Mass_size * 3 + 5, 150, self.ini_y + self.Mass_size * 4 -5, fill = '#800000')#塗りつぶし
        
        Player_A_Wall_Label = tk.Label(text=u'x{}'.format(self.Player_Count_Wall[0]), font=("MSゴシック", "20", "bold"))
        Player_A_Wall_Label.place(x=int(self.ini_x/2), y=self.ini_y + self.Mass_size *4)     

        #Player B
        self.c.create_rectangle(20+self.ini_x+self.Mass_size*self.width, self.ini_y + self.Mass_size * 3+ 5, 150+self.ini_x+self.Mass_size*self.width, self.ini_y + self.Mass_size * 4 -5, fill = '#800000')#塗りつぶし
        
        Player_B_Wall_Label = tk.Label(text=u'x{}'.format(self.Player_Count_Wall[1]), font=("MSゴシック", "20", "bold"))
        Player_B_Wall_Label.place(x=self.ini_x+self.Mass_size*self.width+int((750-(self.ini_x+self.Mass_size*self.width))/2) , y=self.ini_y + self.Mass_size *4)   

        #ゲーム進行時に必要なテキスト 
        self.game_label = tk.Label(self.c, textvariable=self.geme_txt, font=("MSゴシック", "20", "bold"))
        self.game_label.place(x=self.ini_x+self.Mass_size*2, y=self.ini_y+self.Mass_size*self.height+20)   

        #ターン表示テキスト 
        self.Turn_label = tk.Label(self.c, textvariable=self.Turn_txt, font=("MSゴシック", "20", "bold"))
        self.Turn_label.place(x=20, y=20)   

    #ボタンクリック時に呼び出す関数
    def Click_Event(self,event):
        if self.Turn_Change:
            self.Reset_State()

        self.Trun_Player(event)

    #壁の存在を判定
    #上:0 下:1 左:2 右:3
    #壁がある場合Trueが返り値

    def Wall_Check(self,coordinate,direction):
        #上
        if direction == 0:
            return self.Width_Path_List[coordinate[1]][coordinate[0]].Wall_Exsist
        #下
        elif direction == 1:
            return self.Width_Path_List[coordinate[1]+1][coordinate[0]].Wall_Exsist
        #左
        elif direction == 2:
            return self.Height_Path_List[coordinate[0]][coordinate[1]].Wall_Exsist
        #右
        elif direction ==3:
            return self.Height_Path_List[coordinate[0]+1][coordinate[1]].Wall_Exsist

    #四近傍で壁を置けるかを確認
    def Check_Can_Put_Wall(self,Height_or_Width):
        
        #確認したマスを保存
        Checked_Mas_List = []

        #クロスになっているかの確認
        #Path_Listの第2要素の値が大きい方を取得
        Max_Path = None
        

        

        if Height_or_Width == "Height":
            if self.Path_List[0][1] <self.Path_List[1][1]:
                Max_Path = self.Path_List[1]
            else:
                Max_Path = self.Path_List[0]
            print('Max_Path:',Max_Path)
            if self.Width_Path_List[Max_Path[1]][Max_Path[0]].Wall_Exsist and self.Width_Path_List[Max_Path[1]][Max_Path[0]-1].Wall_Exsist :
                print("クロス検知")
                return False

        elif Height_or_Width == "Width":  
            if self.Path_List[0][0] <self.Path_List[1][0]:
                Max_Path = self.Path_List[1]
            else:
                Max_Path = self.Path_List[0]
            print('Max_Path:',Max_Path)

            if self.Height_Path_List[Max_Path[0]][Max_Path[1]].Wall_Exsist and self.Height_Path_List[Max_Path[0]][Max_Path[1]-1].Wall_Exsist :
                print("クロス検知")
                return False

        #壁を設置
        if Height_or_Width == "Height":
            if self.Height_Path_List[self.Path_List[0][0]][self.Path_List[0][1]].Wall_Exsist or self.Height_Path_List[self.Path_List[1][0]][self.Path_List[1][1]].Wall_Exsist :
                return False

        elif Height_or_Width == "Width":
            if self.Width_Path_List[self.Path_List[0][1]][self.Path_List[0][0]].Wall_Exsist or self.Width_Path_List[self.Path_List[1][1]][self.Path_List[1][0]].Wall_Exsist :
                return False

        #壁を設置
        if Height_or_Width == "Height":
            self.Height_Path_List[self.Path_List[0][0]][self.Path_List[0][1]].Wall_Exsist =True
            self.Height_Path_List[self.Path_List[1][0]][self.Path_List[1][1]].Wall_Exsist =True

        elif Height_or_Width == "Width":
            self.Width_Path_List[self.Path_List[0][1]][self.Path_List[0][0]].Wall_Exsist =True
            self.Width_Path_List[self.Path_List[1][1]][self.Path_List[1][0]].Wall_Exsist =True
        
        #色塗り
        A_Check_Mas_List = [[self.Player_Piece_Place[0][0],self.Player_Piece_Place[0][1]]]
        B_Check_Mas_List = [[self.Player_Piece_Place[1][0],self.Player_Piece_Place[1][1]]]

        #最終判定:移動可能マスにゴールが含まれているか
        Can_Goal_A = False
        Can_Goal_B = False

        #四近傍開始
        for Mas in A_Check_Mas_List:
            #上
            #確認済みかを確認
            if not Mas in Checked_Mas_List :
                #上方向に壁があるか
                if Mas[1]-1 >= 0:
                    if not self.Wall_Check(coordinate=Mas,direction=0):
                        #Check_Mas_Listに追加
                        if not [Mas[0],Mas[1]-1] in Checked_Mas_List :
                            A_Check_Mas_List.append([Mas[0],Mas[1]-1])
                #下
                if Mas[1]+1 <= self.width -1 :
                    if not self.Wall_Check(coordinate=Mas,direction=1):
                        if not [Mas[0],Mas[1]+1] in Checked_Mas_List :
                            A_Check_Mas_List.append([Mas[0],Mas[1]+1])
                #左
                if Mas[0]-1 >= 0 :
                    if not self.Wall_Check(coordinate=Mas,direction=2):
                        if not [Mas[0]-1,Mas[1]] in Checked_Mas_List :
                            A_Check_Mas_List.append([Mas[0]-1,Mas[1]])
                #右
                if Mas[0]+1 <= self.width -1 :
                    if not self.Wall_Check(coordinate=Mas,direction=3):
                        if not [Mas[0]+1,Mas[1]] in Checked_Mas_List :
                            A_Check_Mas_List.append([Mas[0]+1,Mas[1]])

                Checked_Mas_List.append(Mas)        
        
        #プレイヤーAの場合        
        for Goal in self.A_Goal:
            if Goal in A_Check_Mas_List:
                Can_Goal_A = True
                break
                
        Checked_Mas_List = []

        #四近傍開始
        for Mas in B_Check_Mas_List:
            #上
            #確認済みかを確認
            if not Mas in Checked_Mas_List :
                #上方向に壁があるか
                if Mas[1]-1 >= 0:
                    if not self.Wall_Check(coordinate=Mas,direction=0):
                        #Check_Mas_Listに追加
                        if not [Mas[0],Mas[1]-1] in Checked_Mas_List :
                            B_Check_Mas_List.append([Mas[0],Mas[1]-1])
                #下
                if Mas[1]+1 <= self.width -1 :
                    if not self.Wall_Check(coordinate=Mas,direction=1):
                        if not [Mas[0],Mas[1]+1] in Checked_Mas_List :
                            B_Check_Mas_List.append([Mas[0],Mas[1]+1])
                #左
                if Mas[0]-1 >= 0 :
                    if not self.Wall_Check(coordinate=Mas,direction=2):
                        if not [Mas[0]-1,Mas[1]] in Checked_Mas_List :
                            B_Check_Mas_List.append([Mas[0]-1,Mas[1]])
                #右
                if Mas[0]+1 <= self.width -1 :
                    if not self.Wall_Check(coordinate=Mas,direction=3):
                        if not [Mas[0]+1,Mas[1]] in Checked_Mas_List :
                            B_Check_Mas_List.append([Mas[0]+1,Mas[1]])

                Checked_Mas_List.append(Mas)

        #プレイヤーBの場合
        for Goal in self.B_Goal:
            if Goal in B_Check_Mas_List:
                Can_Goal_B = True
                break

        if Can_Goal_A and Can_Goal_B:
            return True
        else:
            #NGな壁設置の場合
            #壁を破棄
            if Height_or_Width == "Height":
                self.Height_Path_List[self.Path_List[0][0]][self.Path_List[0][1]].Wall_Exsist =False
                self.Height_Path_List[self.Path_List[1][0]][self.Path_List[1][1]].Wall_Exsist =False

            elif Height_or_Width == "Width":
                self.Width_Path_List[self.Path_List[0][1]][self.Path_List[0][0]].Wall_Exsist =False
                self.Width_Path_List[self.Path_List[1][1]][self.Path_List[1][0]].Wall_Exsist =False

            print(self.Width_Path_List[self.Path_List[0][0]][self.Path_List[0][1]].Wall_Exsist)


            return False

    #勝利判定
    def Win_Check(self):
        #プレイヤーAの勝利判定
        if self.A_or_B == 0:
            if self.Player_Piece_Place[0] in self.A_Goal:
                self.Win = True
                self.geme_txt.set("A Win")
        elif self.A_or_B == 1:
            if self.Player_Piece_Place[1] in self.B_Goal:
                self.Win = True
                self.geme_txt.set("B Win")        

        

    #Playerのターン実行
    def Trun_Player(self, event):
        self.start_x =(event.x)
        self.start_y =(event.y)

        #どっちのターンか。Aなら0、Bなら1
        self.A_or_B = self.Turn%2 

        print("Click_Position:",self.start_x,self.start_y)    
        print(self.Player_Piece_Place[self.A_or_B][0],self.Player_Piece_Place[self.A_or_B][1]) 
        
        #駒のGUIの座標を取得
        Piece_x_start = self.ini_x+self.Player_Piece_Place[self.A_or_B][0]*self.Mass_size
        Piece_x_end = self.ini_x+(self.Player_Piece_Place[self.A_or_B][0]+1)*self.Mass_size

        Piece_y_start=self.ini_y+self.Player_Piece_Place[self.A_or_B][1]*self.Mass_size
        Piece_y_end=self.ini_y+(self.Player_Piece_Place[self.A_or_B][1]+1)*self.Mass_size

        #Choice_Path_List の数が3以上の時リセ
        if len(self.Choice_Path_List)>2:
            self.Choice_Path_List = []

        # print(Piece_x_start,Piece_x_end,Piece_y_start,Piece_y_end)
        #ゲーム終了時は何もしない用に設定
        if self.Win:
            return 

        #駒が選択された場合
        if Piece_x_start < self.start_x and self.start_x < Piece_x_end and Piece_y_start < self.start_y and self.start_y < Piece_y_end:
            self.geme_txt.set("Choice Piece")
            #壁選択情報がある場合リセット
            self.Choice_Path_List = []
            print(self.Player_Piece_Place[self.A_or_B][0],self.Player_Piece_Place[self.A_or_B][1])
            print(self.Mas_List[self.Player_Piece_Place[self.A_or_B][0]][self.Player_Piece_Place[self.A_or_B][1]-1].Piece_Exsist)

            self.flag_Wall = False
            self.flag_Piece= True 

            #移動可能場所を網羅
            self.Can_Move_Point = []   
            
            #上          
           
            #上にマスが無い場合
            if self.Player_Piece_Place[self.A_or_B][1] -1 < 0:
                pass
            #上に駒が無いことを確認
            elif not self.Mas_List[self.Player_Piece_Place[self.A_or_B][0]][self.Player_Piece_Place[self.A_or_B][1]-1].Piece_Exsist:
                #壁の確認                
                if not self.Wall_Check(coordinate=self.Player_Piece_Place[self.A_or_B],direction=0):
    
                    self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0],self.Player_Piece_Place[self.A_or_B][1]-1]) 

            #駒があるときに飛び越えの処理
            elif self.Mas_List[self.Player_Piece_Place[self.A_or_B][0]][self.Player_Piece_Place[self.A_or_B][1]-1].Piece_Exsist and self.Player_Piece_Place[self.A_or_B][1]-2 >= 0:
                #壁の確認.
                 if not  self.Wall_Check(coordinate=self.Player_Piece_Place[self.A_or_B],direction=0):
                    if not self.Width_Path_List[self.Player_Piece_Place[self.A_or_B][1]-1][self.Player_Piece_Place[self.A_or_B][0]].Wall_Exsist:
                        self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0],self.Player_Piece_Place[self.A_or_B][1]-2]) 
                    #左上右上移動
                    else:
                        #左上
                        # if self.Player_Piece_Place[self.A_or_B][0]-1 >= 0 and  self.Player_Piece_Place[self.A_or_B][1]-1 >= 0:
                        if not self.Height_Path_List[self.Player_Piece_Place[self.A_or_B][0]][self.Player_Piece_Place[self.A_or_B][1]-1].Wall_Exsist:
                                self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0]-1,self.Player_Piece_Place[self.A_or_B][1]-1])
                        #右上
                        # if self.Player_Piece_Place[self.A_or_B][0]+1 < self.width -1 and  self.Player_Piece_Place[self.A_or_B][1]-1 >= 0:
                        if not self.Height_Path_List[self.Player_Piece_Place[self.A_or_B][0]+1][self.Player_Piece_Place[self.A_or_B][1]-1].Wall_Exsist:
                                self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0]+1,self.Player_Piece_Place[self.A_or_B][1]-1])

                        
            #上移動不可
            else:
                pass

            #下
            #下にマスが無い場合
            if self.Player_Piece_Place[self.A_or_B][1] +1 >= self.height:
                pass
            #下に駒が無いことを確認
            elif not self.Mas_List[self.Player_Piece_Place[self.A_or_B][0]][self.Player_Piece_Place[self.A_or_B][1]+1].Piece_Exsist:
                #壁の確認
                if not self.Wall_Check(coordinate=self.Player_Piece_Place[self.A_or_B],direction=1):
                    self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0],self.Player_Piece_Place[self.A_or_B][1]+1]) 

            #駒があるときに飛び越えの処理
            elif self.Mas_List[self.Player_Piece_Place[self.A_or_B][0]][self.Player_Piece_Place[self.A_or_B][1]+1].Piece_Exsist and self.Player_Piece_Place[self.A_or_B][1]+2 < self.height:
                #壁の確認.
                if not self.Wall_Check(coordinate=self.Player_Piece_Place[self.A_or_B],direction=1):
                    if not self.Width_Path_List[self.Player_Piece_Place[self.A_or_B][1]+2][self.Player_Piece_Place[self.A_or_B][0]].Wall_Exsist:
                        self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0],self.Player_Piece_Place[self.A_or_B][1]+2]) 
                    else:                    
                        #左下
                        if not self.Height_Path_List[self.Player_Piece_Place[self.A_or_B][0]][self.Player_Piece_Place[self.A_or_B][1]+1].Wall_Exsist:
                            self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0]-1,self.Player_Piece_Place[self.A_or_B][1]+1])
                        #右下
                        if not self.Height_Path_List[self.Player_Piece_Place[self.A_or_B][0]+1][self.Player_Piece_Place[self.A_or_B][1]+1].Wall_Exsist:
                            self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0]+1,self.Player_Piece_Place[self.A_or_B][1]+1])

                    
                    pass
            #下移動不可
            else:
                pass

            #左
            #左にマスが無い場合
            if self.Player_Piece_Place[self.A_or_B][0] - 1 < 0:
                pass
            #左に駒が無いことを確認
            elif not self.Mas_List[self.Player_Piece_Place[self.A_or_B][0]-1][self.Player_Piece_Place[self.A_or_B][1]].Piece_Exsist:
                #壁の確認
                if not self.Wall_Check(coordinate=self.Player_Piece_Place[self.A_or_B],direction=2):
                    self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0]-1,self.Player_Piece_Place[self.A_or_B][1]]) 

            #駒があるときに飛び越えの処理
            elif self.Mas_List[self.Player_Piece_Place[self.A_or_B][0]-1][self.Player_Piece_Place[self.A_or_B][1]].Piece_Exsist and self.Player_Piece_Place[self.A_or_B][0]-2 >= 0:
                #壁の確認.
                 if not self.Wall_Check(coordinate=self.Player_Piece_Place[self.A_or_B],direction=2):
                    if not self.Height_Path_List[self.Player_Piece_Place[self.A_or_B][0]-1][self.Player_Piece_Place[self.A_or_B][1]].Wall_Exsist:
                        self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0]-2,self.Player_Piece_Place[self.A_or_B][1]]) 
                    else:
                        #左上
                        if not self.Width_Path_List[self.Player_Piece_Place[self.A_or_B][1]][self.Player_Piece_Place[self.A_or_B][0]-1].Wall_Exsist:
                            self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0]-1,self.Player_Piece_Place[self.A_or_B][1]-1])

                        #左下
                        # self.Width_Path_List[coordinate[1]+1][coordinate[0]].Wall_Exsist
                        if not self.Width_Path_List[self.Player_Piece_Place[self.A_or_B][1]+1][self.Player_Piece_Place[self.A_or_B][0]-1].Wall_Exsist:
                            self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0]-1,self.Player_Piece_Place[self.A_or_B][1]+1])
            #左移動不可
            else:
                pass

            #右
            #右にマスが無い場合
            if self.Player_Piece_Place[self.A_or_B][0] + 1 >= self.width:
                pass
            #右に駒が無いことを確認
            elif not self.Mas_List[self.Player_Piece_Place[self.A_or_B][0]+1][self.Player_Piece_Place[self.A_or_B][1]].Piece_Exsist:
                #壁の確認
                if not self.Wall_Check(coordinate=self.Player_Piece_Place[self.A_or_B],direction=3):
                    self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0]+1,self.Player_Piece_Place[self.A_or_B][1]]) 

            #駒があるときに飛び越えの処理
            elif self.Mas_List[self.Player_Piece_Place[self.A_or_B][0]+1][self.Player_Piece_Place[self.A_or_B][1]].Piece_Exsist and self.Player_Piece_Place[self.A_or_B][1]+2 < self.width:
                #壁の確認.
                 if not self.Wall_Check(coordinate=self.Player_Piece_Place[self.A_or_B],direction=3):
                    if not self.Height_Path_List[self.Player_Piece_Place[self.A_or_B][0]+2][self.Player_Piece_Place[self.A_or_B][1]].Wall_Exsist:
                        self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0]+2,self.Player_Piece_Place[self.A_or_B][1]]) 
                    else:
                        #右上
                        if not self.Width_Path_List[self.Player_Piece_Place[self.A_or_B][1]][self.Player_Piece_Place[self.A_or_B][0]+1].Wall_Exsist:
                            self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0]+1,self.Player_Piece_Place[self.A_or_B][1]-1])

                        #右下
                        # self.Width_Path_List[coordinate[1]+1][coordinate[0]].Wall_Exsist
                        if not self.Width_Path_List[self.Player_Piece_Place[self.A_or_B][1]+1][self.Player_Piece_Place[self.A_or_B][0]+1].Wall_Exsist:
                            self.Can_Move_Point.append([self.Player_Piece_Place[self.A_or_B][0]+1,self.Player_Piece_Place[self.A_or_B][1]+1])

            #右移動不可
            else:
                pass

            #移動可能マスの描画が欲しい
        
            print(self.Can_Move_Point)

        #壁が選択された場合
        elif self.A_or_B==0 and 20 < self.start_x and self.start_x <150 and (self.ini_y + self.Mass_size * 3 + 5) < self.start_y and self.start_y < (self.ini_y + self.Mass_size * 4 -5) or self.A_or_B == 1 and  20+self.ini_x+self.Mass_size*self.width < self.start_x and self.start_x <  150+self.ini_x+self.Mass_size*self.width and self.ini_y + self.Mass_size * 3+ 5 < self.start_y and   self.start_y < self.ini_y + self.Mass_size * 4 -5 :
            #壁の残りがあるか
            if self.Player_Count_Wall[self.A_or_B] <= 0:            
                self.geme_txt.set("No Wall")
            else:
                self.flag_Wall = True
                self.flag_Piece= False
                self.geme_txt.set("Choice Wall")
        
        #駒選択時移動場所選択
        elif self.flag_Piece :
            #マウス座標から盤面座標へ
            Choice_Place_x = math.floor((self.start_x - self.ini_x )/50)
            Choice_Place_y = math.floor((self.start_y - self.ini_y )/50)


            #選択箇所が移動可能かの確認
            if [Choice_Place_x,Choice_Place_y] in self.Can_Move_Point:
                self.Move_Piece([self.Player_Piece_Place[self.A_or_B][0],self.Player_Piece_Place[self.A_or_B][1]],[Choice_Place_x,Choice_Place_y])
                self.Turn_Change = True
                self.Turn += 1
                self.Can_Move_Point = []
                self.flag_Piece= False
                self.geme_txt.set("Move Piece")


        elif self.flag_Wall:
            #クリック座標をリストに追加
            self.Choice_Path_List.append((self.start_x,self.start_y))
            print("Choice_Path_List",self.Choice_Path_List)

            #通路を２つ選択している場合
            if (len(self.Choice_Path_List) == 2 ):
                #横の選択or縦の選択を判定
                # 差を取ってxが小さい場合縦選択、yが小さい場合横選択と定義
                # 小さい方の差が10を超えていた場合エラーとする

                #誤差の定義
                Threshold = 15
                
                Loss = [abs(self.Choice_Path_List[0][0] - self.Choice_Path_List[1][0]),abs(self.Choice_Path_List[0][1] - self.Choice_Path_List[1][1])]

                #横軸選択時
                if Loss[0] > Loss[1]:
                    
                    if Threshold < Loss[1]:
                        self.Choice_Path_List = []
                        self.geme_txt.set("滅茶苦茶な選択困ります")
                    else :
                        self.geme_txt.set("X軸選択")
                        #選択した道をリストに追加
                        self.Path_List =[[math.floor((self.Choice_Path_List[0][0] - self.ini_x ) / self.Mass_size ),round((self.Choice_Path_List[0][1] - self.ini_y ) / self.Mass_size )],[math.floor((self.Choice_Path_List[1][0] - self.ini_x ) / self.Mass_size ),round((self.Choice_Path_List[1][1] - self.ini_y ) / self.Mass_size )]]
                        print("Path_List:",self.Path_List)
                        #選択した道が範囲ないかを判定
                        if self.Path_List[0][0] < 0 or self.Path_List[0][0] > self.height-1 or  self.Path_List[0][1] <= 0 or self.Path_List[0][1] > self.width -1:
                            self.Choice_Path_List = []
                            self.geme_txt.set("壁設置不可")
                        elif self.Path_List[1][0] < 0 or self.Path_List[1][0] > self.height-1 or  self.Path_List[1][1] <= 0 or self.Path_List[1][1] > self.width -1:
                            self.Choice_Path_List = []
                            self.geme_txt.set("壁設置不可")
                        else:
                            #選択された道が連続されているか？
                            if abs(self.Path_List[0][0]-self.Path_List[1][0]) == 1 and  abs(self.Path_List[0][1]-self.Path_List[1][1]) == 0:
                                #四傍で選択可能な壁を判定
                                if self.Check_Can_Put_Wall(Height_or_Width="Width"):
                                    self.Player_Count_Wall[self.A_or_B]-= 1                
                                    self.Turn_Change = True
                                    self.Turn+=1
                                else:
                                    self.Choice_Path_List = []
                                    self.geme_txt.set("詰みます")
                            else:
                                self.Choice_Path_List = []
                                self.geme_txt.set("壁設置不可")

                
                #縦軸選択時
                elif Loss[0] < Loss[1]:
                    if Threshold < Loss[0]:
                        self.geme_txt.set("滅茶苦茶な選択困ります")
                    else :
                        self.geme_txt.set("y軸選択")
                        #選択した道をリストに追加
                        self.Path_List =[[round((self.Choice_Path_List[0][0] - self.ini_x ) / self.Mass_size ),math.floor((self.Choice_Path_List[0][1] - self.ini_y ) / self.Mass_size )],[round((self.Choice_Path_List[1][0] - self.ini_x ) / self.Mass_size ),math.floor((self.Choice_Path_List[1][1] - self.ini_y ) / self.Mass_size )]]
                        print("Path_List:",self.Path_List)
                        #選択した道が範囲ないかを判定
                        if self.Path_List[0][0] <= 0 or self.Path_List[0][0] > self.height-1 or  self.Path_List[0][1] < 0 or self.Path_List[0][1] > self.width -1:
                            self.Choice_Path_List = []
                            self.geme_txt.set("壁外:壁設置不可")

                        elif self.Path_List[1][0] <= 0 or self.Path_List[1][0] > self.height-1 or  self.Path_List[1][1] < 0 or self.Path_List[1][1] > self.width -1:
                            self.Choice_Path_List = []
                            self.geme_txt.set("壁外:壁設置不可")
                        else:
                            #選択された道が連続されているか？
                            if abs(self.Path_List[0][1]-self.Path_List[1][1]) == 1 and  abs(self.Path_List[0][0]-self.Path_List[1][0]) == 0:
                                #四傍で選択可能な壁を判定
                                if self.Check_Can_Put_Wall(Height_or_Width="Height"):
                                    self.Player_Count_Wall[self.A_or_B]-= 1                
                                    self.Turn_Change = True
                                    self.Turn+=1
                                else:
                                    self.Choice_Path_List = []
                                    self.geme_txt.set("詰みます")
                            else:
                                    self.Choice_Path_List = []
                                    self.geme_txt.set("非連続:壁設置不可")

                else:
                    self.geme_txt.set("同じ場所を選択しています")
                    self.Choice_Path_List = []
                

    
        if self.Turn_Change:
            if self.A_or_B == 0:
                self.Turn_txt.set("Blue")
            else:
                self.Turn_txt.set("Red")

            self.Win_Check()

        self.on_draw()
        
          
        
class Path_Info:
    def __init__(self):
        #障害物の有無
        self.Wall_Exsist = False

class Mass_Info:
    def __init__(self):
        #駒の有無（Red,Yellow,White）
        self.Piece_Exsist = False
        #駒のPlayer
        self.Piece_self = None




boad = State() 
boad.pack()
boad.mainloop()