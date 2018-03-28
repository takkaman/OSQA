
import subprocess

def isidvalid(user):
    idcmd = ["/usr/local/bin/tdph -w -h email=%s empcode=Active return name" %(user) ,]
    child = subprocess.Popen(idcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    streamdata = child.communicate()[0]
    if streamdata == '':
        return False
    return True

def getIdFullName(user):
    """
        returns the family Name and first Name from snps id
        for example:
                Family, First = getIdFullName("id")
    """
    idcmd = ["/usr/local/bin/tdph -w -h email=%s return name" %(user), ]
    child = subprocess.Popen(idcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    streamdata = child.communicate()[0]
    if streamdata == '':
        return ["", ""]
    return map(str.strip, streamdata.split(',' ,1))

