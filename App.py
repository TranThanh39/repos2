import mysql.connector as mc
import tkinter as tk
dtb1=mc.connect(
    host='localhost',
    user='root',
    password='Ncrosst2003@',
    database='english_lord'
)
mcr=dtb1.cursor()


def tu_da_hoc():
    wd=tk.Tk()
    wd.geometry('800x400')
    text1=tk.Text(wd, wrap='word')
    text1.place(width=800, height=300)
    mcr.execute('select * from vocabulary where learn is True')
    tmp=mcr.fetchall()
    for i in tmp:
        text1.insert(tk.END, '- {} ({})'.format(i[1], i[3]))
        mcr.execute('select * from mean where id_voc={}'.format(i[0]))
        tmp1=mcr.fetchall()
        for j in tmp1:
            text1.insert(tk.END, '\n\t+ ({}): {}'.format(j[2], j[3]))
            mcr.execute('select * from example where id_me={}'.format(j[1]))
            tmp2=mcr.fetchall()
            for z in tmp2:
                text1.insert(tk.END, '\n\t\tvd: {}'.format(z[2]))
        text1.insert(tk.END,'\n\n')
    def change(text2):
        text2=text2[:len(text2)-1]
        mcr.execute('update vocabulary set learn=False where word=\"{}\"'.format(text2))
        dtb1.commit()
    text2=tk.Text(wd)
    text2.place(width=350, height=20, x=120, y=310)
    but1=tk.Button(wd, text='Sửa thành chưa học', command=lambda: change(text2.get(1.0, tk.END)))
    but1.place(x=250, y=335)
    wd.mainloop()

def tu_chua_hoc():
    wd=tk.Tk()
    wd.geometry('800x400')
    text1=tk.Text(wd, wrap='word')
    text1.place(width=800, height=300)
    mcr.execute('select * from vocabulary where learn is False')
    tmp=mcr.fetchall()
    for i in tmp:
        text1.insert(tk.END, '- {} ({})'.format(i[1], i[3]))
        mcr.execute('select * from mean where id_voc={}'.format(i[0]))
        tmp1=mcr.fetchall()
        for j in tmp1:
            text1.insert(tk.END, '\n\t+ ({}): {}'.format(j[2], j[3]))
            mcr.execute('select * from example where id_me={}'.format(j[1]))
            tmp2=mcr.fetchall()
            for z in tmp2:
                text1.insert(tk.END, '\n\t\tvd: {}'.format(z[2]))
        text1.insert(tk.END,'\n\n')
    def change(text2):
        text2=text2[:len(text2)-1]
        mcr.execute('update vocabulary set learn=True where word=\"{}\"'.format(text2))
        dtb1.commit()
    text2=tk.Text(wd)
    text2.place(width=350, height=20, x=120, y=310)
    but1=tk.Button(wd, text='Sửa thành đã học', command=lambda: change(text2.get(1.0, tk.END)))
    but1.place(x=250, y=335)
    wd.mainloop()


def tu_theo_chu_cai():
    def hien_thi(w):
        wd2=tk.Tk()
        wd2.geometry('800x400')
        text1=tk.Text(wd2, wrap='word')
        text1.place(height=300, width=800)
        mcr.execute('select * from vocabulary where tfchr=\'{}\''.format(w))
        tmp=mcr.fetchall()
        list1=[]
        for i in tmp:
            text1.insert(tk.END, '- {} ({}) - {}'.format(i[1], i[3], 'done' if i[4]==1 else 'not done'))
            list1.append(i[1])
            mcr.execute('select * from mean where id_voc={}'.format(i[0]))
            tmp1=mcr.fetchall()
            for j in tmp1:
                text1.insert(tk.END, '\n\t+ ({}): {}'.format(j[2], j[3]))
                mcr.execute('select * from example where id_me={}'.format(j[1]))
                tmp2=mcr.fetchall()
                for z in tmp2:
                    text1.insert(tk.END, '\n\t\tvd: {}'.format(z[2]))
            text1.insert(tk.END,'\n\n')
        def change2(tx1):
            tx=tx1.get(1.0, tk.END)
            while tx[-1].isalpha()==False: 
                tx=tx[:len(tx)-1]
                if len(tx)==0: return
            if tx not in list1: return
            wd3=tk.Tk()
            wd3.geometry('750x500')
            mcr.execute('select * from vocabulary where word=\'{}\''.format(tx))
            tmp3=mcr.fetchall()[0]
            tx2=tk.Text(wd3)
            tx3=tk.Text(wd3)
            tx2.place(x=10, y=10, width=130, height=25)
            tx3.place(x=200, y=10, width=130, height=25)
            tx2.insert(1.0,tmp3[1])
            tx3.insert(1.0,tmp3[3])
            mcr.execute('select * from mean where id_voc={}'.format(tmp3[0]))
            tmp4=mcr.fetchall()
            list2=[]
            space=40
            for i in tmp4:
                tx4=tk.Text(wd3)
                tx4.place(x=100, y=space, width=600, height=25)
                tx5=tk.Text(wd3)
                tx5.place(x=10, y=space, width=80, height=25)
                tx5.insert(1.0, i[2])
                tx4.insert(1.0, i[3])
                space+=35
                mcr.execute('select * from example where id_me={}'.format(i[1]))
                tmp5=mcr.fetchall()
                litmp=[tx4, tx5, i[1], i[2], i[3], []]
                for j in tmp5:
                    tx4=tk.Text(wd3)
                    tx4.place(x=30, y=space, width=600, height=25)
                    tx4.insert(1.0, j[2])
                    litmp[5].append([tx4, j[1], j[2]])
                    space+=35
                list2.append(litmp)
            def change3():
                tmp6=tx2.get(1.0, tk.END)
                while tmp6[-1].isalpha()==False:
                    tmp6=tmp6[:len(tmp6)-1]
                    if len(tmp6)==0: return
                if tmp6!=tmp3[1]:
                    mcr.execute('update vocabulary set word=\'{}\' where id={}'.format(tmp6, tmp3[0]))
                tmp6=tx3.get(1.0, tk.END)
                while tmp6[-1].isalpha()==False:
                    tmp6=tmp6[:len(tmp6)-1]
                    if len(tmp6)==0: return
                if tmp6!=tmp3[3]:
                    mcr.execute('update vocabulary set pronou=\'{}\' where id={}'.format(tmp6, tmp3[0]))
                for i in list2:
                    tmp6=i[0].get(1.0, tk.END)
                    while tmp6[-1].isalpha()==False:
                        tmp6=tmp6[:len(tmp6)-1]
                        if len(tmp6)==0: return
                    if tmp6!=i[4]:
                        mcr.execute('update mean set t_mean=\'{}\' where id_me={}'.format(tmp6, i[2]))
                    tmp6=i[1].get(1.0, tk.END)
                    while tmp6[-1].isalpha()==False:
                        tmp6=tmp6[:len(tmp6)-1]
                        if len(tmp6)==0: return
                    if tmp6!=i[3]:
                        mcr.execute('update mean set typechr=\'{}\' where id_me={}'.format(tmp6, i[2]))
                    for j in i[5]:
                        tmp6=j[0].get(1.0, tk.END)
                        while tmp6[-1].isalpha()==False:
                            tmp6=tmp6[:len(tmp6)-1]
                            if len(tmp6)==0: return
                        if tmp6!=j[2]:
                            mcr.execute('update example set t_exam=\'{}\' where id_ex={}'.format(tmp6, j[1]))
                dtb1.commit()
            but1=tk.Button(wd3, text='Sửa', command=lambda: change3())
            but1.place(x=400, y=space+10)
        tx1=tk.Text(wd2)
        tx1.place(x=200, y=310, width=300, height=25)
        bu1=tk.Button(wd2, text='Sửa', command=lambda: change2(tx1))
        bu1.place(x=310, y=350)           
    wd=tk.Tk()
    wd.geometry('540x100')
    position=10
    for i in range(65, 91):
        tmp=chr(i)
        but=tk.Button(wd, text=tmp, height=1, width=1, font='Arial 10', command=lambda ch=tmp: hien_thi(ch))
        but.place(x=position, y=20)
        position+=20
    wd.mainloop()


def xem_tu():
    wd=tk.Tk()
    wd.geometry('400x450')
    button1=tk.Button(wd, text='Xem từ đã học', height=2, width=14, font='Arial 15', command=tu_da_hoc)
    button1.place(x=115, y=10)
    button2=tk.Button(wd, text='Xem từ chưa học', height=2, width=14, font='Arial 15', command=tu_chua_hoc)
    button2.place(x=115, y=150)
    button3=tk.Button(wd, text='Xem theo chữ cái', height=2, width=14, font='Arial 15',command=tu_theo_chu_cai)
    button3.place(x=115, y=290)
    wd.mainloop()


def tim_kiem():
    def read_tx(tx):
        tmp=tx.split()
        tmp=list('{}'.format(i) for i in tmp)
        tmp.append('')
        tmp=tuple(tmp)
        wd2=tk.Tk()
        wd2.geometry('800x300')
        text1=tk.Text(wd2)
        text1.place(height=200, width=800)
        print(tmp)
        mcr.execute('select * from vocabulary where word in {}'.format(tmp))
        tmp=mcr.fetchall()
        
        list1=[]
        for i in tmp:
            text1.insert(tk.END, '- {} ({}) - {}'.format(i[1], i[3], 'done' if i[4]==1 else 'not done'))
            list1.append(i[1])
            mcr.execute('select * from mean where id_voc={}'.format(i[0]))
            tmp1=mcr.fetchall()
            for j in tmp1:
                text1.insert(tk.END, '\n\t+ ({}): {}'.format(j[2], j[3]))
                mcr.execute('select * from example where id_me={}'.format(j[1]))
                tmp2=mcr.fetchall()
                for z in tmp2:
                    text1.insert(tk.END, '\n\t\tvd: {}'.format(z[2]))
            text1.insert(tk.END,'\n\n')
        def change(mode, tx1):
            tx=tx1.get(1.0, tk.END)
            while tx[-1].isalpha()==False: 
                tx=tx[:len(tx)-1]
                if len(tx)==0: return
            if tx not in list1: return
            tx1.delete(1.0, tk.END)
            mcr.execute('update vocabulary set learn={} where word=\'{}\''.format('True' if mode==1 else 'False', tx))
        def change2(tx1):
            tx=tx1.get(1.0, tk.END)
            while tx[-1].isalpha()==False: 
                tx=tx[:len(tx)-1]
                if len(tx)==0: return
            if tx not in list1: return
            wd3=tk.Tk()
            wd3.geometry('750x500')
            mcr.execute('select * from vocabulary where word=\'{}\''.format(tx))
            tmp3=mcr.fetchall()[0]
            tx2=tk.Text(wd3)
            tx3=tk.Text(wd3)
            tx2.place(x=10, y=10, width=130, height=25)
            tx3.place(x=200, y=10, width=130, height=25)
            tx2.insert(1.0,tmp3[1])
            tx3.insert(1.0,tmp3[3])
            mcr.execute('select * from mean where id_voc={}'.format(tmp3[0]))
            tmp4=mcr.fetchall()
            list2=[]
            space=40
            for i in tmp4:
                tx4=tk.Text(wd3)
                tx4.place(x=100, y=space, width=600, height=25)
                tx5=tk.Text(wd3)
                tx5.place(x=10, y=space, width=80, height=25)
                tx5.insert(1.0, i[2])
                tx4.insert(1.0, i[3])
                space+=35
                mcr.execute('select * from example where id_me={}'.format(i[1]))
                tmp5=mcr.fetchall()
                litmp=[tx4, tx5, i[1], i[2], i[3], []]
                for j in tmp5:
                    tx4=tk.Text(wd3)
                    tx4.place(x=30, y=space, width=600, height=25)
                    tx4.insert(1.0, j[2])
                    litmp[5].append([tx4, j[1], j[2]])
                    space+=35
                list2.append(litmp)
            def change3():
                tmp6=tx2.get(1.0, tk.END)
                while tmp6[-1].isalpha()==False:
                    tmp6=tmp6[:len(tmp6)-1]
                    if len(tmp6)==0: return
                if tmp6!=tmp3[1]:
                    mcr.execute('update vocabulary set word=\'{}\' where id={}'.format(tmp6, tmp3[0]))
                tmp6=tx3.get(1.0, tk.END)
                while tmp6[-1].isalpha()==False:
                    tmp6=tmp6[:len(tmp6)-1]
                    if len(tmp6)==0: return
                if tmp6!=tmp3[3]:
                    mcr.execute('update vocabulary set pronou=\'{}\' where id={}'.format(tmp6, tmp3[0]))
                for i in list2:
                    tmp6=i[0].get(1.0, tk.END)
                    while tmp6[-1].isalpha()==False:
                        tmp6=tmp6[:len(tmp6)-1]
                        if len(tmp6)==0: return
                    if tmp6!=i[4]:
                        mcr.execute('update mean set t_mean=\'{}\' where id_me={}'.format(tmp6, i[2]))
                    tmp6=i[1].get(1.0, tk.END)
                    while tmp6[-1].isalpha()==False:
                        tmp6=tmp6[:len(tmp6)-1]
                        if len(tmp6)==0: return
                    if tmp6!=i[3]:
                        mcr.execute('update mean set typechr=\'{}\' where id_me={}'.format(tmp6, i[2]))
                    for j in i[5]:
                        tmp6=j[0].get(1.0, tk.END)
                        while tmp6[-1].isalpha()==False:
                            tmp6=tmp6[:len(tmp6)-1]
                            if len(tmp6)==0: return
                        if tmp6!=j[2]:
                            mcr.execute('update example set t_exam=\'{}\' where id_ex={}'.format(tmp6, j[1]))
                dtb1.commit()
            but1=tk.Button(wd3, text='Sửa', command=lambda: change3())
            but1.place(x=400, y=space+10)
                    
                    

        tx1=tk.Text(wd2)
        tx1.place(x=200, y=210,width=300, height=25)
        bu1=tk.Button(wd2, text='Đánh dấu đã học', command=lambda: change(1, tx1))
        bu2=tk.Button(wd2, text='Đánh dấu chưa học', command=lambda: change(1, tx1))
        bu3=tk.Button(wd2, text='Sửa', command=lambda: change2(tx1))
        bu1.place(x=210, y=250)
        bu2.place(x=330, y=250)
        bu3.place(x=460, y=250)
        #wd2.mainloop()
    wd=tk.Tk()
    wd.geometry('400x100')
    tx=tk.Text(wd)
    tx.place(x=10,y=10, height=30, width=380)
    but=tk.Button(wd, text='Tìm kiếm', command=lambda: read_tx(tx.get(1.0, tk.END)))
    but.place(x=170, y=70)
    wd.mainloop()


def them_tu():
    global mcr
    def them_nghia(word):
        def them_vd(word, wd):
            def vd(tmp3):
                tmp=tx5.get(1.0, tk.END)
                index=-1
                while tmp[index].isalpha()==False: index-=1
                tmp=tmp[:len(tmp)+index+1]
                mcr.execute('insert into example(id_me, t_exam) values ({}, \"{}\")'.format(tmp3, tmp))
                dtb1.commit()
                tx5.delete(1.0, tk.END)
            tmp1=tx3.get(1.0, tk.END)
            tmp2=tx4.get(1.0, tk.END)
            tx3.delete(1.0, tk.END)
            tx4.delete(1.0, tk.END)
            index=-1
            while tmp1[index].isalpha()==False: index-=1
            tmp1=tmp1[:len(tmp1)+index+1]
            index=-1
            while tmp2[index].isalpha()==False: index-=1
            tmp2=tmp2[:len(tmp2)+index+1]
            mcr.execute('insert into mean(id_voc, typechr, t_mean) select id, \"{1}\",\"{2}\" from vocabulary where word=\"{0}\"'.format(word, tmp1, tmp2))
            dtb1.commit()
            mcr.execute('select last_insert_id()')
            tmp3=mcr.fetchone()[0]
            lb3=tk.Label(wd, text='Ví dụ')
            lb3.place(x=1, y=130)
            tx5=tk.Text(wd, height=2, width=35, wrap='word')
            tx5.place(x=55, y=130)
            but5=tk.Button(wd, text='Thêm ví dụ', command =lambda: vd(tmp3))
            but5.place(x=160, y=170)
        wd=tk.Tk()
        wd.geometry('400x200')
        lb1=tk.Label(wd, text='Loại từ')
        lb1.place(x=1, y=20)
        lb2=tk.Label(wd, text='Mô tả')
        lb2.place(x=1, y=60)
        tx3=tk.Text(wd,height=1, width=35)
        tx3.place(x=60, y=20)
        tx4=tk.Text(wd, height=2, width=35, wrap='word')
        tx4.place(x=60, y=60)
        but4=tk.Button(wd, text='Thêm',command=lambda: them_vd(word, wd))
        but4.place(x=160, y=100)
        wd.mainloop()

    def them_tu(word, pronou, but2):
        global mcr
        pronou=pronou[:len(pronou)-1]
        mcr.execute('insert into vocabulary(word, tfchr, pronou, learn) values (\"{}\",\"{}\",\"{}\",{})'.format(word, word[0], pronou, 'False'))
        dtb1.commit()
        but2.place(x=160, y=90)

    def check_tu(word):
        global mcr
        word=word[:len(word)-1]
        mcr.execute('select count(*) from vocabulary where word=\"{}\"'.format(word))
        tmp=mcr.fetchone()[0]
        if(tmp==0):
            wd=tk.Tk()
            wd.geometry('400x150')
            lb1=tk.Label(wd, text='Cách phát âm')
            lb1.place(x=1, y=20)
            tx2=tk.Text(wd)
            tx2.place(height=20, width=200, x=130, y=20)
            but2=tk.Button(wd, text='Thêm nghĩa', command=lambda: them_nghia(word))
            but1=tk.Button(wd, text='Thêm', command=lambda: them_tu(word, tx2.get(1.0, tk.END), but2))
            but1.place(x=160, y=60)
            wd.mainloop()
        elif tmp==1: them_nghia(word)

    wd=tk.Tk()
    wd.geometry('400x100')
    tx=tk.Text(wd)
    tx.place(x=10,y=10, height=30, width=380)
    but=tk.Button(wd, text='Thêm từ', command=lambda: check_tu(tx.get(1.0, tk.END)))
    but.place(x=170, y=70)
    wd.mainloop()


root=tk.Tk()
root.geometry('400x500')
button1=tk.Button(root, text='Xem từ', height=2, width=10, font='Arial 20', command=xem_tu)
button1.place(x=115, y=10)
button2=tk.Button(root, text='Thêm từ', height=2, width=10, font='Arial 20', command=them_tu)
button2.place(x=115, y=150)
button3=tk.Button(root, text='Tìm kiếm từ', height=2, width=10, font='Arial 20', command=tim_kiem)
button3.place(x=115, y=290)
root.mainloop()
