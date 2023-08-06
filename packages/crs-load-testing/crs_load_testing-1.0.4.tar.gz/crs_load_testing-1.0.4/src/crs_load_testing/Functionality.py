from email import header
import glob
from crs_load_testing import Authorize
import os
import json
import pandas as pd
import jsonpath

# This function creates case with the required subjects and downloads the excel sheet of all created subjects.
def Create_Case_With_Subjects():
    #region header data
    directory = os.getcwd()
    directory = directory + "\TestData\Createcase.json"
    file = open(directory,'r')
    json_input = file.read()
    request_json_case = json.loads(json_input)
    print(request_json_case)
    processed_token, oauth = Authorize.Get_AccessToken()  
    headers = {"Authorization":processed_token,"accept":"application/json"}
    #endregion

    #region Create case and capture case id
    CaseID = oauth.post('https://crs-api-qa.kroll.com/v1/cases', verify=False, headers=headers, json=request_json_case)
    print(str(CaseID))
    # print(CaseID.status_code)
    #endregion

    #region Create subjects
    exceldata = {"SubjectId":[],"SubjectName":[],"SubjectType":[]}
    directory = os.getcwd()
    directory = directory + "\TestData\SubjectsData"
    for files in glob.glob(directory+'\*'):
        print(files)
        file = open(files,'r')
        json_input = file.read()
        request_json_subject = json.loads(json_input)
        request_json_subject["caseId"] = str(CaseID.text).replace("\"","")
        print(request_json_subject)
        if request_json_subject["subjectType"] == 1:
            exceldata["SubjectName"].append(str(request_json_subject["entityName"]).replace("%20"," ").replace("%2C",","))
            exceldata["SubjectType"].append(str(request_json_subject["subjectType"]))
        else:
            exceldata["SubjectName"].append(str(request_json_subject["individualName"]["fullName"]))
            exceldata["SubjectType"].append(str(request_json_subject["subjectType"]))
        subject_id = oauth.post("https://crs-api-qa.kroll.com/v1/subjects", verify=False,headers=headers,json=request_json_subject)
        print(subject_id.status_code)
        print(subject_id.text)
        exceldata["SubjectId"].append(str(subject_id.text).replace("\"",""))
    #endregion

    #region Create Excel
    df = pd.DataFrame(exceldata)
    print(df)
    df.to_excel('SubjectsOutput.xlsx')
    #endregion

# This function gets the subjects from a particular case. Case number is currently hardcoded in the passing url currently.
def Get_Subjects_From_Case(caseid):
    processed_token, oauth = Authorize.Get_AccessToken()  
    headers = {"Authorization":processed_token,"accept":"application/json"}
    caseurl = 'https://crs-api-qa.kroll.com/v1/cases/details/' + str(caseid)
    subjectsdata = oauth.get(caseurl, verify=False, headers=headers)
    subjectsdata_json = json.loads(subjectsdata.text)
    onlysubjects = jsonpath.jsonpath(subjectsdata_json,'subjectDetails')
    subjectids = []
    for i in range(len(onlysubjects[0])):
        subjectids.append(onlysubjects[0][i]['id'])
    print(subjectids)

    for i in range(len(subjectids)):
        url = 'https://crs-api-qa.kroll.com/v1/subjects/' + subjectids[i]
        subjectdetails = oauth.get(url,verify=False, headers=headers)
        subjectdetailsjson = json.loads(subjectdetails.text)
        subjectdetailsjson = str(subjectdetailsjson)
        subjectdetailsjson = subjectdetailsjson.rsplit("enrichment")[0].replace("'","\"").replace("False","false").replace("None","null")
        subjectdetailsjson = subjectdetailsjson[:-3]
        subjectdetailsjson = subjectdetailsjson + "}"
        json_subjectdetails = json.loads(subjectdetailsjson)
        del json_subjectdetails["accountId"]
        json_subjectdetails["caseId"] = ""
        json_subjectdetails = str(json_subjectdetails).replace("'","\"").replace("False","false").replace("None","null")
        directory = os.getcwd()
        directory = directory + "\TestData\SubjectsData\\"
        f = open(directory+"subject"+ str(i+1) +".json","w")
        f.write(json_subjectdetails)
        f.close()

def Enrich_Subjects():
    processed_token, oauth = Authorize.Get_AccessToken()  
    headers = {"Authorization":processed_token,"accept":"application/json","Content-Type":"application/json"}
    df = pd.read_excel('SubjectsOutput.xlsx')
    print(len(df))
    for i in range(len(df)):
        if df["SubjectType"][i] == 1:
            getenrichmenturl = "https://crs-api-qa.kroll.com/v1/subjects/"+ df["SubjectId"][i] +"/enrich/entity"
            enrichentity = oauth.get(getenrichmenturl, verify=False, headers=headers)
            enrichentity_json = json.loads(enrichentity.text)
            idslist = []
            for j in range(len(enrichentity_json)):
                idslist.append(enrichentity_json[j]['id'])
            postenrichmenturl = "https://crs-api-qa.kroll.com/v1/subjects/"+ df["SubjectId"][i] +"/enrich?type=entity"
            idlist10 = idslist[:10]
            print(idlist10)
            idjson10 = str(idlist10)
            postenrichmententity = oauth.post(postenrichmenturl, verify=False, headers=headers, data=idjson10)
            print(postenrichmententity.status_code)

        else:
            getenrichmenturl = "https://crs-api-qa.kroll.com/v1/subjects/"+ df["SubjectId"][i] +"/enrich/individual"
            enrichindividual = oauth.get(getenrichmenturl, verify=False, headers=headers)
            enrichindividual_json = json.loads(enrichindividual.text)
            idslist = []
            for j in range(len(enrichindividual_json)):
                idslist.append(enrichindividual_json[j]['id'])
            postenrichmenturl = "https://crs-api-qa.kroll.com/v1/subjects/"+ df["SubjectId"][i] +"/enrich?type=individual"
            idlist10 = idslist[:10]
            print(idlist10)
            idjson10 = str(idlist10)
            postenrichmentindividual = oauth.post(postenrichmenturl, verify=False, headers=headers, data=idjson10)
            print(postenrichmentindividual)

def Start_Research():
    processed_token, oauth = Authorize.Get_AccessToken()  
    headers = {"Authorization":processed_token,"accept":"application/json","Content-Type":"application/json"}
    df = pd.read_excel('SubjectsOutput.xlsx')
    print(len(df))
    for i in range(len(df)):
        reasearchurl = "https://crs-api-qa.kroll.com/v1/subjects/" + df["SubjectId"][i] + "/research"
        researchsubject = oauth.post(reasearchurl, verify=False, headers=headers)
        print(researchsubject)