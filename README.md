# denoise
大一立项降噪
介绍一下各个部分，很多东西都懒得改了

myApp.py:主程序，UI界面，转码，把OnStart里面的“进行处理”附近修改一下，即可只实现单纯的转码。91行图标为我自己桌面的路径，要修改一下才能运行。

wave_reader.py:主处理脚本，调用其他的处理函数，单独运行可以实现批处理

wave_modify.py:各种滤波器

SpectralSub.py:谱减法滤波

watcher.py:查看波形和频率分布，需要指定声道和起始点（只能看一秒），可以同时加载多个文件。

其他的文件都没怎么用
