from __future__ import print_function
from django.shortcuts import HttpResponse, render,redirect
from django.http import FileResponse
from resume_maker.resume import generate_data
from mailmerge import MailMerge
from datetime import date
import os
from zipfile import ZipFile
import sys
from os import listdir

def cleanup():
    test = os.listdir()
    for item in test:
        if item.endswith(".zip"):
            os.remove(item)

def home(req):
    cleanup()
    if(req.method == "POST"):
        name = req.POST['name']
        email = req.POST['email']
        contact = req.POST['num']
        linkedin_url = req.POST['linkedin']
        
        about_button = req.POST.get('abt','off')
        bio_button = req.POST.get('bio','off')
        achieve_button = req.POST.get('ach','off')
        skill_btn = req.POST.get('skill','off')
        about = ""
        
        ach1 = ""
        ach2 = ""
        ach3 = ""
        skill_1 = req.POST["skill_1"]
        skill_2 = req.POST["skill_2"]
        skill_3 = req.POST["skill_3"]
        skill_4 = req.POST["skill_4"]
        edu_button = req.POST.get('edu','off')
        exp_button = req.POST.get('exp','off')
        edu_1 = ""
        edu_2 = ""
        edu_3 = ""
        exp_1 = ""
        exp_2 = ""
        exp_3 = ""
        exp_4 = ""
        
        try:
            data = generate_data(linkedin_url)
            if(about_button=="on"):
                about = data["About"]
            elif(bio_button=="on"):
                about = data["Bio"]
            else:
                about = req.POST.get("about","")
        


            if(achieve_button=="on"):
                if(len(data["Honors & awards"]) >= 3):
                    ach1 = data["Honors & awards"][0]
                    ach2 = data["Honors & awards"][1]
                    ach3 = data["Honors & awards"][2]
                elif(len(data["Honors & awards"]) == 2):
                    
                    ach1 = data["Honors & awards"][0]
                    ach2 = data["Honors & awards"][1]
                else:
                    ach1 = data["Honors & awards"][0]
                    

            else:
                ach1 = req.POST.get("ach_1","")
                ach2 = req.POST.get("ach_2","")
                ach3 = req.POST.get("ach_3","")
            
            if(edu_button == "on"):
                if(len(data["Education"]) >= 3):
                    edu_1 = data["Education"][0]
                    edu_2 = data["Education"][1]
                    edu_3 = data["Education"][2]
                elif(len(data["Education"]) == 2):
                    
                    edu_1 = data["Education"][0]
                    edu_2 = data["Education"][1]
                else:
                    edu_1 = data["Education"][0]
            else:
                edu_1 = req.POST.get("12","")
                edu_2 = req.POST.get("ug","")
                edu_3 = req.POST.get("pg","")

            if(exp_button=="on"):
                if(len(data["Experience"]) >= 4):
                    exp_1 = data["Experience"][0]
                    exp_2 = data["Experience"][1]
                    exp_3 = data["Experience"][2]
                    exp_4 = data["Experience"][3]
                elif(len(data["Experience"]) == 3):
                    
                    exp_1 = data["Experience"][0]
                    exp_2 = data["Experience"][1]
                    exp_3 = data["Experience"][2]
                elif(len(data["Experience"]) == 2):
                    
                    exp_1 = data["Experience"][0]
                    exp_2 = data["Experience"][1]
                else:
                    exp_1 = data["Experience"][0]
            else:
                exp_1 = req.POST.get("exp_1","")
                exp_2 = req.POST.get("exp_2","")
                exp_3 = req.POST.get("exp_3","")
                exp_4 = req.POST.get("exp_4","")


            if(skill_btn=="on"):
                if(len(data["Skills"]) >= 4):
                    skill_1 = data["Skills"][0]
                    skill_2 = data["Skills"][1]
                    skill_3 = data["Skills"][2]
                    skill_4 = data["Skills"][3]
                elif(len(data["Skills"]) == 3):
                    
                    skill_1 = data["Skills"][0]
                    skill_2 = data["Skills"][1]
                    skill_3 = data["Skills"][2]
                elif(len(data["Skills"]) == 2):
                    
                    skill_1 = data["Skills"][0]
                    skill_2 = data["Skills"][1]
                else:
                    skill_1 = data["Skills"][0]
            else:
                skill_1 = req.POST.get("skill_1","")
                skill_2 = req.POST.get("skill_2","")
                skill_3 = req.POST.get("skill_3","")
                skill_4 = req.POST.get("skill_4","")


            template = r"finallayout1.docx"
            template2 = r"finallayout.docx"
            template3 = r"exp2.docx"
            document = MailMerge(template)
            document2 = MailMerge(template2)
            document3 = MailMerge(template3)

            document.merge(about=about,ach_1=ach1,ach_2=ach2,ach_3=ach3,contact=str(contact),edu_1=edu_1,edu_2=edu_2,edu_3=edu_3,email=email,exp_1=exp_1,exp_2=exp_2,exp_3=exp_3,exp_4=exp_4,linkedin=linkedin_url,name=name,skill_1=skill_1,skill_2=skill_2,skill_3=skill_3,skill_4=skill_4)

            document.write(r"{}1.docx".format("resume_"+name))
            document3.merge(about=about,ach_1=ach1,ach_2=ach2,ach_3=ach3,contact=str(contact),edu_1=edu_1,edu_2=edu_2,edu_3=edu_3,email=email,exp_1=exp_1,exp_2=exp_2,exp_3=exp_3,exp_4=exp_4,linkedin=linkedin_url,name=name,skill_1=skill_1,skill_2=skill_2,skill_3=skill_3,skill_4=skill_4)

            document3.write(r"{}3.docx".format("resume_"+name))
            document2.merge(about=about,ach_1=ach1,ach_2=ach2,ach_3=ach3,contact=str(contact),edu_1=edu_1,edu_2=edu_2,edu_3=edu_3,email=email,exp_1=exp_1,exp_2=exp_2,exp_3=exp_3,exp_4=exp_4,linkedin=linkedin_url,name=name,skill_1=skill_1,skill_2=skill_2,skill_3=skill_3,skill_4=skill_4)

            document2.write(r"{}2.docx".format("resume_"+name))
            with ZipFile(r'resume_{}.zip'.format(name), 'w') as zip_object:
                # Adding files that need to be zipped
                zip_object.write(r"{}1.docx".format("resume_"+name))
                zip_object.write(r"{}2.docx".format("resume_"+name))
                zip_object.write(r"{}3.docx".format("resume_"+name))

                # Check to see if the zip file is created
                if os.path.exists(r'resume_{}.zip'.format(name)):
                    print("ZIP file created")
                    os.remove(r"{}1.docx".format("resume_"+name))
                    os.remove(r"{}2.docx".format("resume_"+name))
                    os.remove(r"{}3.docx".format("resume_"+name))
                else:
                    print("ZIP file not created")
            
            
            return FileResponse(open(r'resume_{}.zip'.format(name), 'rb'))
        except:
            return HttpResponse("Either You have selected those entries which do not exist on your linkedin profile or you dont have GoogleChrome installed on your machine, Update the entries or install google chrome before proceeding also let the new chrome window run for atleast a minute (depending on speed of internet connection) before closing the window.")

        # return HttpResponse("Everything worked")
    return render(req,"home.html")


