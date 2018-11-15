import winrm
import traceback
import sys
windows_host = windows_host.splitlines()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[0;93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def is_number(uchar):  
    """判断一个unicode是否是数字"""  
    if uchar >= u'\u0030' and uchar<=u'\u0039':  
        return True  
    return False  
def is_alphabet(uchar):  
    """判断一个unicode是否是英文字母"""  
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):  
        return True  
    return False  
def gbkwordlen(u):  
    if is_number(u) or is_alphabet(u):  
        return 1  
    return 2  
# 计算文本显示宽度  
def gbkwordslen(uw):  
    i = 0  
    for u in uw:  
        i += gbkwordlen(u)  
    return i  
def logging_stage(text,color=None):
    logging_width = 60
    filling_string = "="
    text_length = gbkwordslen(text)
    if color is not None:
        text = color + text +bcolors.ENDC
    string_num = int((logging_width-text_length)/2)
    print("{}{}{}".format(filling_string*string_num,text,filling_string*string_num))

def run_ps_and_logging(winrmsession,ps_script,
    start_message,failed_message,success_message):
    logging_stage(start_message,bcolors.BOLD)
    try:
        r = winrmsession.run_ps(ps_script)
        print(r.status_code)
        if int(r.status_code) != 0:
            print(r.std_err)
            logging_stage(failed_message,bcolors.UNDERLINE)
        else:
            print(r.std_out)
            print(r.std_err)
            logging_stage(success_message,bcolors.OKGREEN)
        return {'status_code':str(r.status_code),'std_out':r.std_out,'std_err':r.std_err}
    except winrm.exceptions.InvalidCredentialsError:
        print(bcolors.UNDERLINE+u'认证失败，请检查用户名密码'+bcolors.ENDC)
        return {'status_code':1,'critical':True}
    except:
        print(bcolors.UNDERLINE+u"Unexpected error:{}".format(sys.exc_info()[0])+bcolors.ENDC)
        traceback.print_exc()  
        return {'status_code':1,'critical':True}
    
def do_filebeat_stuff(winrmsession):
    # 查看服务状态, 如果在C盘, 中止, 报错, 没有服务, 报错
    check_service_exist_script = """
if (Get-Service "filebeat" -ErrorAction SilentlyContinue)
{
    "service exists"
}
else {
    "service not found"
}
    """
    check_filebeat_at_c_disk = """
if(Test-Path -Path C:\\filebeat ) 
{
    "service at C DISK !"
}
else {
    "service at D DISK !"
}
    """
    ps_scripts = [check_service_exist_script, check_filebeat_at_c_disk]
    for p in ps_scripts:
        run_ps_and_logging(winrmsession, p,'stage1','success','failed')
    # 分发配置文件
    # get file
    # 调整权限
    # 重启服务
    

def get_user_passwd():
    return ('deploy','zy8oF^uZT')

def get_correct_login_method(ip):
    try:
        (machine_user, machine_passwd) = get_user_passwd()
        s = winrm.Session(ip, auth=(machine_user, machine_passwd),server_cert_validation='ignore')
        r = s.run_cmd('ipconfig', ['/all'])
    except winrm.exceptions.InvalidCredentialsError:
        print('We use NTLM in this authorize')
        user = 'YZCYP\\' + machine_user
        s = winrm.Session(ip, auth=(user, machine_passwd),transport='ntlm',server_cert_validation='ignore')
    except:
        return None
    try:
        r = s.run_cmd('ipconfig', ['/all'])
    except:
        s =None
    return s

if __name__ == '__main__':
    for h in windows_host:
        session = get_correct_login_method(h)
        if session:
            print(h)
            do_filebeat_stuff(session)
    
