import tkinter as tk
from tkinter import ttk

from ..TkPackByMe import sqlite_api
from ..TkPackByMe import fix
sw=sqlite_api.sqlite_deal()

class TableFrame(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.Show()
    def Show(self):
        column_name =('id','create_time','lastchange_time',
            'PCC_Band','PCC_BandWidth','PCC_Channel',
            'SCC1_Band','SCC1_BandWidth','SCC1_Channel',
            'SCC2_Band','SCC2_BandWidth','SCC2_Channel',
            'SCC3_Band','SCC3_BandWidth','SCC3_Channel')
        # menuBar = Menu(self) # 1------------开辟菜单并生成对象
        # menuBar.add_command(label='创建行',command=self.create_new_row)
        # self.config(menu=menuBar)#----------配置生效
        self.tree = ttk.Treeview(self,height=10,show='headings',columns=column_name,selectmode='extended')
        for i_1 in range(len(column_name)):
            self.tree.heading(str(i_1),text=column_name[i_1])
            self.tree.column(str(i_1),width=100,anchor='center')
            print(i_1)
            print(column_name[i_1])
        # sw.create_row()
        data = sw.get_all_data()
        def p_out(e):
            t_meun=fix.data_option(self,self.tree,e)
            t_meun.double_click_change_row_data()
        def r_k(e):
            t_meun=fix.data_option(self,self.tree,e)
            t_meun.right_key_menu()
        self.tree.bind('<Double-Button-1>',p_out)
        self.tree.bind('<Button-3>',r_k)
        print(data)
        for x in data:
            self.tree.insert('','end',value=x)
        self.tree.pack()
    def create_new_row(self):
        sw.create_row()
        fix.update_treeveiw(self,self.tree).treeview_update()

if __name__=="__main__":
    xe = tk.Tk()
    TableFrame(xe).pack()
    xe.mainloop()

