import rich.console
import sys
import os
import time

console = rich.console.Console()

def outlog(*value):
    """输出log内容"""
    out = ""
    for v in value:
        out += f"{v} "

    console.print(out[0:-1])

def initlog(log):
    """替换字符串引用内容"""
    pos = log.find("${")
    if pos == -1:
        return log.replace("$$.$$.","${")
    else:
        content = log[pos+2:log.find("}",pos)]
        content_data = "${" + content + "}"
        data = content.split(",")
        msg = ""
        if data[0] == "unixtime":
            msg = log.replace(content_data, str(int(time.time())))
        elif data[0] == "time":
            msg = log.replace(
                    content_data,
                    time.strftime(
                        data[1],
                        time.localtime(time.time())
                    )
                )
        elif data[0] == "shell":
            shell = os.popen(data[1])
            dat = shell.read()
            if dat[dat.__len__() - 1:] == "\n":
                dat = dat[0:-1]
            msg = log.replace(content_data,dat)
        elif data[0] == "osname":
            msg = log.replace(content_data,os.name)
        elif data[0] == "argv":
            if data[1] == "all":
                msg = log.replace(content_data, str(sys.argv))
            else:
                msg = log.replace(content_data, sys.argv[int(data[1])])
        else:
            msg = log.replace(content_data, f"$$.$$.{content}" + "}")

        return initlog(msg)



class XPyLogger(object):
    def __init__(self, sender, style, file):
        self.style = style
        self.sender = sender
        if file:
            try:
                ldir = ""
                for d in file.split("/")[0:-1]:
                    ldir += d
                    ldir += "/"
                os.mkdir(ldir)
            except:
                pass
            self.file = open(file,"w",encoding = "utf-8")
        else:
            self.file = False
    def initmsg(self,message):
         # 处理MSG
        msg = ""
        for m in message:
            msg += str(m)
        msg = msg[0:-1]
        return msg
    def outlog(self,message,level = 1):
        log = ""
        
        msg = message
        # 初始化style
        log = self.style["log"]
        log = log.replace("${log}",msg)
        ## 处理引用
        log = initlog(log)
        log = log1 = log.replace("${sender}",self.sender)
        log = log.replace("${color}",self.style["color"][level])
        log = log1 = log.replace("${level}",self.style["level"][level])
        # PRINT
        outlog(log)
        # WRITE
        if self.file:
            self.file.write(log1)
    def __del__(self):
        if self.file:
            self.file.close()
    def log(self,message,level):
        msg = self.initmsg(message)
        for i in msg.split("\n"):
            self.outlog(i,level)


    def info(self,*message):
        self.log(message,0)
    def warn(self,*message):
        self.log(message,2)
    def error(self, *message):
        self.log(message,1)
        

        

class styles:
    default = {
            "log":"${color}[${time,%H:%M:%S}][${sender} / ${level}] ${log}",
            "level":[
                "INFO",
                "ERROR",
                "WARN"
            ],
            "color":[
                "",
                "[bold red]"
                "[bold yellow]"
            ]
        }

    frpc = {
            "log":"[${time,%H:%M:%S}] [${sender}] ${color}${level}[\]: %{log}",
            "level":[
                "I",
                "E",
                "W"
            ],
            "color":[
                "[bold blue]",
                "[bold red]",
                "[bold yellow]"
            ]
        }

default_logfile = f"./logs/{time.time()}.log"

def getLogger(sender = "Main Thread",
        style = styles.default,
        file = default_logfile):
    """初始化log对象"""
    return XPyLogger(sender,style,file)
