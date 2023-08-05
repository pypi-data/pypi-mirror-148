import tkinter
from ..TkPackByMe import sqlite_api
class data_option():
    def __init__(self,base_tk,base_tree,e):
        self.tk = base_tk
        self.sq=sqlite_api.sqlite_deal()
        self.tree=base_tree
        # self.e = 
        self.entry_init(e)
    def entry_init(self,e):
        self.x_pos=str(e.x_root)
        self.y_pos=str(e.y_root)
        # print('111'+str()) 
        print('x坐标:'+self.x_pos)
        print('y坐标:'+self.y_pos)
        self.x_index = self.tree.identify_column(e.x)
        self.y_index = self.tree.identify_row(e.y)
        print('x_idx:',self.x_index)
        print('y_idx:',self.y_index)
        print(self.tree.identify_column(e.x))
        self.row_data_get=self.tree.item(self.tree.identify_row(e.y),"values")
        self.x_int = int(self.x_index[1:])-1
        self.y_int = int(self.row_data_get[0])
        print('x_int',str(self.x_int))
        # self.id_int=self.row_data_get
        print(self.row_data_get)
        # print(self.tree.focus())
    def treeview_delete(self):
        item=self.tree.get_children()
        for x in item:
            self.tree.delete(x)
    def treeview_update(self):
        self.treeview_delete()
        data = self.sq.get_all_data()
        for x in data:
            self.tree.insert('','end',value=x)
        self.tk.update()
    def create_row_destroy(self,base_last):
        base_last.destroy()
        self.sq.create_row()
        # self.sq.get_all_data()
        self.treeview_update()
        # sq.delete()
    def delete_row_destroy(self,base_last):
        base_last.destroy()
        self.sq.delete(self.row_data_get[0])
        self.treeview_update()
    def change_row_single_data(self,update_data,base_top):
        # id=self.row_data_get[0]
        self.sq.change_single_item(self.y_int,self.x_int, update_data)
        self.treeview_update()
        base_top.destroy()
    def right_key_menu(self):
        r_k_m= tkinter.Toplevel(self.tk)
        r_k_m.geometry('+{}+{}'.format(self.x_pos,self.y_pos))
        # r_k_m.overrideredirect(True)
        r_k_m.wm_overrideredirect(True)
        # r_k_m.transient(self.tk) #模态
        r_k_m.grab_set()      #模态
        text_button1 = tkinter.Button(r_k_m,text='创建',command=lambda: self.create_row_destroy(r_k_m))
        text_button2 = tkinter.Button(r_k_m,text='删除',command=lambda: self.delete_row_destroy(r_k_m))
        # text_button3 = tkinter.Button(r_k_m,text='查询',command=lambda: self.sq.serch_by_create_time())
        text_button4 = tkinter.Button(r_k_m,text='取消',command=r_k_m.destroy)
        text_button1.pack()
        text_button2.pack()
        # text_button3.pack()
        text_button4.pack()
        # top_fx.close()
        r_k_m.mainloop()
    def double_click_change_row_data(self):
        top_fx = tkinter.Toplevel(self.tk)
        top_fx.geometry('+'+self.x_pos+'+'+self.y_pos)
        top_fx.overrideredirect(True)
        top_fx.grab_set()      #模态
        text_label_get=tkinter.StringVar()
        text_label_get.set(self.row_data_get[int(self.x_index[1:])-1])
        text_label = tkinter.Label(top_fx,text=text_label_get.get())
        text_label.grid(row=0,column=0,columnspan=2)
        text_in = tkinter.Entry(top_fx)
        text_in.grid(row=1,column=0,columnspan=2)
        text_button1 = tkinter.Button(top_fx,text='确认',command=lambda: self.change_row_single_data(text_in.get(),top_fx))
        text_button1.grid(row=2,column=0,sticky='WE')
        text_button2 = tkinter.Button(top_fx,text='取消',command=top_fx.destroy)
        text_button2.grid(row=2,column=1,sticky='WE')
        top_fx.mainloop()
    def addrow(self):
        pass
    def change_row_data(self):
        pass
    def delete_row(self):
        pass

class update_treeveiw():
    def __init__(self,base_tk,base_tree):
        self.tk = base_tk
        self.sq=sqlite_api.sqlite_deal()
        self.tree=base_tree
    def treeview_delete(self):
            item=self.tree.get_children()
            for x in item:
                self.tree.delete(x)
    def treeview_update(self):
        self.treeview_delete()
        data = self.sq.get_all_data()
        for x in data:
            self.tree.insert('','end',value=x)
        self.tk.update()