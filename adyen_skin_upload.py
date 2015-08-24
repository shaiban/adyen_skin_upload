import requests
import sys
import config
import os.path



print 'ADYEN skin upload v. 0.1'


merch_env_codes = config.merch_env_codes
moto_env_codes = config.moto_env_codes

ssl_verify=True




def upload_skin(skin_file, account_data, env_code) :
    url_0 = "https://ca-test.adyen.com/ca/ca/login.shtml"
    url = "https://ca-test.adyen.com/ca/ca/config/j_security_check"
    headers={"Host":"ca-test.adyen.com","Referer": "https://ca-test.adyen.com/ca/ca/skin/uploadskin.shtml?skinCode="+env_code,"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding":"gzip, deflate"}
    result = False
    print "login"
    s = requests.session()
    r= s.get(url_0,verify=ssl_verify, headers=headers) #####################################
    print "INFO: login to admin console"
    pos=r.text.find("j_formHash")
    formhash= r.text[pos+19:pos+19+31]
    data["j_formHash"]=formhash
    #print "DEBUG:formhash:" +formhash
    #print "DEBUG: cookies:" + str(s.cookies)
    r = s.post(url, data, headers=headers) ##########################################
    #print r.text

    print "INF:open skin menu"

    r=s.get("https://ca-test.adyen.com/ca/ca/skin/skins.shtml", headers=headers, verify=ssl_verify)

    print "INFO: open skin "  + env_code
    r = s.get ("https://ca-test.adyen.com/ca/ca/skin/uploadskin.shtml?skinCode="+env_code, verify=ssl_verify, headers=headers) ################################
    #print r.text

    pos=r.text.find("formHash")
    pos=r.text.find("formHash", pos+1)
    pos=r.text.find("formHash", pos+1)
    formhash= r.text[pos+17:pos+17+31]

    #print "DEBUG: form hash:" + formhash

    print "INFO: upload  skin "  + env_code
    files = {'uploadFile': (skin_file.name,skin_file,'application/x-zip-compressed',{'Expires': '0'})}
    #files = dict(foo='bar')
    #"activeAccount":"MerchantAccount.DeTuinenATG"
    #data1={"uploadFile":env_code+".zip"}
    data1={"skinCode":env_code,"formHash":formhash}
    upload_url="https://ca-test.adyen.com/ca/ca/skin/processkin.shtml"
    r=s.post(upload_url,files=files,  headers=headers,verify=ssl_verify,  data=data1)
    #print r.text

    #if (r.text.find("Your Skin file has been uploaded")!=-1):
    if (r.text.find("No files were accepted")!=-1):
        print "UPLOAD ERROR"
        exit(1)
    else :
        print "UPLOADED OK"
    #print r.headers
    print "INFO: confirm  skin "  + env_code
    pos=r.text.find("formHash")
    pos=r.text.find("formHash", pos+1)
    pos=r.text.find("formHash", pos+1)
    formhash= r.text[pos+17:pos+17+31]
    print formhash

    data2={"skinCode":env_code, "submit":"Confirm" ,"formHash":formhash,"activate":"true" }
    r=s.post(upload_url, headers=headers,verify=ssl_verify,  data=data2)
    #print r.text
    if (r.text.find("Skin processed and submitted to the test system")!=-1):
        print "ACTIVATED OK"
    else :
        exit (1)


    return result




#print len(sys.argv)

if ((len(sys.argv)!=4)):
    print "USAGE: " + sys.argv[0] + " [env code e.g. DEV2]  [file name e.g. ./moto-skin.zip] [account type moto or merch]"
    exit(1)

env_name= sys.argv[1]
skin_file_name = sys.argv[2]
account_mode = sys.argv[3]
#file
if (not os.path.isfile(skin_file_name)):
    print "ERROR: file does not exit:" + skin_file_name
    exit(1)
file1=open(skin_file_name, 'rb')
print file1.name



if (not (env_name in moto_env_codes.keys())):
    print "Bad env name"
    exit (1)

if (account_mode=="merch") :
    data=config.merch_data
    env_code=merch_env_codes[env_name]

if (account_mode=="moto") :
    data=config.moto_data
    env_code=moto_env_codes[env_name]


upload_skin (file1, data, env_code=env_code)




