# -*- coding: utf-8 -*-
import wx
import wx.lib.buttons as buttons
import ctypes
import wave_reader
import os
from pydub import AudioSegment
# Query DPI Awareness (Windows 10 and 8)
awareness = ctypes.c_int()
errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
#print(awareness.value)
# Set DPI Awareness  (Windows 10 and 8)
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
# the argument is the awareness level, which can be 0, 1 or 2:
# for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 2)
# Set DPI Awareness  (Windows 7 and Vista)
success = ctypes.windll.user32.SetProcessDPIAware()
# behaviour on later OSes is undefined, although when I run it on my Windows 10 machine, it seems to work with effects identical to SetProcessDpiAwareness(1

class mainFrame(wx.Frame):
    def __init__(self , parent , id , title , size):
        #初始化
        wx.Frame.__init__(self , parent , id , title)
        self.SetSize(size)#设置对话框的大小
        self.Center()#设置弹窗在屏幕中间

        #使用尺寸器写,拉大或者缩小窗口，中间的控件会随着窗口的大小已固定的尺寸而改变
        panel = wx.Panel(self)#self表示实例即mainFrame，创建一个面板
        
        #定义panel中的元件
        self.buttonList = ['wav', 'mp3', 'flv', 'ogg']
        self.handlerList = ['null', 'high', 'mid', 'low']
        self.checkBox = wx.CheckBox(panel, -1, "denoise", (35, 40), (150, 20))
        self.checkBox.SetValue(True)
        self.fmtBox = wx.RadioBox(panel, -1, '输出文件格式', wx.DefaultPosition, wx.DefaultSize,  
                        self.buttonList, 5, wx.RA_SPECIFY_COLS)
        self.fmtBox1 = wx.RadioBox(panel, -1, '调节选项', wx.DefaultPosition, wx.DefaultSize,  
                        self.handlerList, 5, wx.RA_SPECIFY_COLS)
        self.glance1 = buttons.GenButton(panel , -1 , label = '浏览')
        self.glance2 = buttons.GenButton(panel , -1 , label = '浏览')
        self.start  = buttons.GenButton(panel , -1 , label = '开始')
        self.inText = wx.TextCtrl(panel , -1 , '' , wx.DefaultPosition)
        self.outText = wx.TextCtrl(panel , -1 , '' , wx.DefaultPosition)
        self.inputLabel = wx.StaticText(panel,label="输入文件目录")
        self.outputLabel = wx.StaticText(panel,label="输出文件目录")
        # self.slider = wx.Slider(panel , -1 , 50 , 0 , 100 ,
        #                         style = wx.SL_AUTOTICKS | wx.SL_LABELS)#初始值，最小值，最大值
        # self.GPA = wx.StaticText(panel,label="调节指标")
        
        #绑定事件
        self.Bind(wx.EVT_BUTTON , self.OnIn , self.glance1)
        self.Bind(wx.EVT_BUTTON , self.OnOut , self.glance2)
        self.Bind(wx.EVT_BUTTON , self.OnStart , self.start)
        self.Bind(wx.EVT_RADIOBOX , self.OnFmt , self.fmtBox)
        
        #设置布局
        self.box1 = wx.BoxSizer()
        self.box1.Add(self.inputLabel , proportion=2 , flag=wx.EXPAND | wx.ALL , border=5)
        self.box1.Add(self.inText , proportion=8 , flag=wx.EXPAND | wx.ALL , border=5)
        self.box1.Add(self.glance1 , proportion=2 , flag=wx.EXPAND | wx.ALL , border=5)
        
        self.box2 = wx.BoxSizer()
        self.box2.Add(self.outputLabel , proportion=2 , flag=wx.EXPAND | wx.ALL , border=5)
        self.box2.Add(self.outText , proportion=8 , flag=wx.EXPAND | wx.ALL , border=5)
        self.box2.Add(self.glance2 , proportion=2 , flag=wx.EXPAND | wx.ALL , border=5)
        
        # self.box3 = wx.BoxSizer()
        # self.box3.Add(self.GPA , proportion=3 , flag=wx.EXPAND | wx.ALL , border=5)
        # self.box3.Add(self.slider , proportion=7 , flag=wx.EXPAND | wx.ALL , border=5)
        
        self.v_box = wx.BoxSizer(wx.VERTICAL)
        self.v_box.Add(self.fmtBox, proportion=8,flag=wx.EXPAND | wx.ALL,border=5)
        self.v_box.Add(self.fmtBox1, proportion=8,flag=wx.EXPAND | wx.ALL,border=5)
        # self.v_box.Add(self.box3, proportion=1,flag=wx.EXPAND | wx.ALL,border=5)
        self.v_box.Add(self.checkBox, proportion=1,flag=wx.EXPAND | wx.ALL,border=5)
        self.v_box.Add(self.box1, proportion=1,flag=wx.EXPAND | wx.ALL,border=5)
        self.v_box.Add(self.box2, proportion=1,flag=wx.EXPAND | wx.ALL,border=5)
        self.v_box.Add(self.start, proportion=2,flag=wx.EXPAND | wx.ALL,border=5)
        
        panel.SetSizer(self.v_box)
        
        #菜单
        self.menubar = wx.MenuBar()
        self.menu = wx.Menu()
        self.info = self.menu.Append(-1, '用户手册')
        self.menubar.Append(self.menu, '帮助')
        self.Bind(wx.EVT_MENU, self.OnMenu, self.info)
        self.SetMenuBar(self.menubar)
        
        #图标
        self.icon = wx.Icon('D://Desktop//lab//bitbug_favicon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        
        self.Show()
        self.dirname = ''
        self.filename = ''        
    def OnIn(self,event):
        dialog = wx.FileDialog(self , '选择输入文件' , self.dirname ,'','*.*',wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            self.inText.Value = dialog.GetPath()
        dialog.Destroy()
        
    def OnOut(self,event):
        self.select = self.fmtBox.GetStringSelection()
        fmt = '*.' + self.select
        '''
        self.splitFilename = self.filename.split('.')
        if len(self.splitFilename) == 2:
        self.filename = self.splitFilename[0] + '.' + self.select
        '''
        dialog = wx.FileDialog(self , '选择输出文件' ,self.dirname ,
                               'new_'+self.filename,fmt,wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT )
        if dialog.ShowModal() == wx.ID_OK:
            self.dirname = dialog.GetDirectory()
            self.outText.Value = dialog.GetPath()
        dialog.Destroy()
        self.OnFmt(self)
    
    def OnStart(self,event):#这里以后可能要加进度条
        try:
            #先检查输入输出文件路径是否合法
            #splitext分割后缀名，返回列表，取后缀并[1:]去掉'.'
            input_ext = os.path.splitext(self.inText.Value)[-1][1:]
            if input_ext in self.buttonList and \
                os.path.splitext(self.outText.Value)[-1][1:] == self.fmtBox.GetStringSelection():
                pass
            else:
                raise Exception
            #先转化成wav
            temp_in = os.path.splitext(self.inText.Value)[0]+'.wav'
            temp_out = os.path.splitext(self.outText.Value)[0]+'.wav'
            input_not_wav = 0
            if input_ext !='wav':
                input_not_wav = 1
                if input_ext == 'mp3':
                    song_in = AudioSegment.from_mp3(self.inText.Value)
                elif input_ext == 'flv':
                    song_in = AudioSegment.from_flv(self.inText.Value)
                elif input_ext == 'raw':
                    song_in = AudioSegment.from_raw(self.inText.Value)
                elif input_ext == 'ogg':
                    song_in = AudioSegment.from_ogg(self.inText.Value)
                else:
                    raise IOError
                song_in.export(temp_in, format = 'wav')
            #进行处理
            wave_reader.wave_reader(temp_in , temp_out, \
                                    self.fmtBox1.GetStringSelection(), self.checkBox.GetValue())
            #进行格式转换
            if self.fmtBox.GetStringSelection() != 'wav':
                song_out = AudioSegment.from_wav(temp_out)
                song_out.export(self.outText.Value, format = self.fmtBox.GetStringSelection())
                os.remove(temp_out)
            if input_not_wav == 1:
                os.remove(temp_in)
            #展示成功
            dialog = wx.MessageDialog(self, '新的文件已经生成在指定路径下','任务完成！',wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        except ValueError:
            dialog = wx.MessageDialog(self, '传入处理方式错误','错误!',wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        except IOError:
            dialog = wx.MessageDialog(self, '请检查您的文件路径','错误!',wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            
    def OnFmt(self,event):
        self.outText.Value = os.path.splitext(self.outText.Value)[0]+'.'+self.fmtBox.GetStringSelection()
        #self.pathlist = self.outText.Value.split('.')
        #if len(self.pathlist) >= 2:
        #    self.pathlist[-1] = self.fmtBox.GetStringSelection()
        #self.outText.Value = '.'.join(self.pathlist)
        #self.outText.Value = self.outText.Value.replace(self.outText.Value[-3:] , self.fmtBox.GetStringSelection())
    
    def OnMenu(self, event):
        text = '''
        made by CBJ HJX RBL WCX CKY
        null:不进行音效修改         high:截取高音部分
        mid:截取中间部分            low:截取低音部分
        denoise:进行降噪（可选）
        '''
        text = ''
        f = open('./info.txt', 'r', encoding='utf-8')
        line = f.readline()
        while line:
            text+=line
            line=f.readline()
        info = wx.MessageDialog(self, text,'用户手册',wx.OK)
        
        #info = wx.GenericMessageDialog(self, text, '帮助', style=wx.OK)
        info.ShowModal()
        info.Destroy()

if __name__ == '__main__':
    app = wx.App()
    myTitle = 'hitsz大一项目——音频处理器'
    mySize  = (600,450)
    frame = mainFrame(None , -1 , myTitle , mySize)
    app.MainLoop()