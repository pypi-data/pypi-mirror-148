import zipfile
import shutil
import os

#! Version = 0.0.1
#* 2022/4/27 22:09
# DONE将模块上传到pypi(https://pypi.org/) 参考:https://blog.csdn.net/weixin_43918046/article/details/124303554
# // def help():
# //   print("This is a tool for Scratch 3.0, which includes the ability to unzip files")


def Sb3Unzip(Filepath, Outpath, mode="A"):
    # * 功能正常，全部完成
    """
    Filepath : Original file path
    Outpath : Output path
    mode : A(All Files) B(project.json only) C(All resource files)
    return : If successful, return the path of project.json, if not, return the reason(ERROR:xxx)
    """
    if(IsSb3File(Filepath)):
        shutil.copy(Filepath, Outpath)
        Filename = os.path.split(Filepath)
        zpath = Outpath + "\\" + Filename[1]
        os.chdir(Outpath)
        try:
            if mode == 'A':
                # * 全部文件
                with zipfile.ZipFile(zpath) as f:
                    f.extractall()
            elif mode == 'B':
                # * 仅有json文件
                file = zipfile.ZipFile(Filepath)
                for i in file.namelist():
                    if i == "project.json":
                        file.extract(i)
            elif mode == 'C':
                # * 仅有资源文件
                file = zipfile.ZipFile(Filepath)
                for i in file.namelist():
                    if i != "project.json":
                        file.extract(i)
            else:
                return "ERROR : Invalid parameters(mode)"
        except:
            return "ERROR : Failed to unzip the file!"
        OutFilePath = Outpath + "\\project.json"
        # print(os.getcwd())
        os.remove(Filename[1])
        return OutFilePath
    return "ERROR:Not a valid Scratch file"


def IsSb3File(Filepath):
    """
    Filepath : Original file path
    return 1 or 0 
    """
    try:
        nsns = zipfile.ZipFile(Filepath, 'r')
    except:
        return 0
    # for i in nsns.namelist():
    #     print(i)
    # print("project.json" in nsns.namelist())
    if(zipfile.is_zipfile(Filepath) and "project.json" in nsns.namelist()):
        return 1
    return 0


def Sb3Zip(dirpath, outFullName):
    """
    :param dirpath: 
    :param outFullName: 
    :return: NULL
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename),
                      os.path.join(fpath, filename))
    zip.close()

#! 以下为测试
# if __name__ == "__main__":
#     Ipath = r"C:\Users\wondr\Desktop\time.txt"
#     Opath = r"C:\Users\wondr\Desktop\bp"
#     # print(IsSb3File(Ipath))
#     # Unzip(Filepath=Ipath, Outpath=Opath,mode="C")
#     z = Unzip(Ipath,Opath,mode="B")
#     print(z)
