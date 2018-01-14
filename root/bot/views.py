# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
import json
import numpy
import ast 

json_data = """{
    "function":"sample-text-function",
    "questions":[
        {
            "instruction":"Hello! I'm Elth. I'm your algorithms bot."
        },
        {
            "text":"Before starting please tell me your first name",
            "var":"first_name"
        },
        {
            "text":"Please tell me your last name",
            "var":"last_name"
        },
        {
            "text":"And your gender?",
            "options":[
                "Male",
                "female"
            ],
            "var":"gender"
        },
        {
            "text":"May I know your age?",
            "var":"age"
        },
        {
            "conditions":[
                [
                    "age.isdigit() == False"
                ]
            ],
            "text":"I couldn't quite get how that response can be your age :/ Please enter your valid age.",
            "var":"age"
        },
        {
            "instruction":"Congratulations! Registration Successful."
        },
        {
            "calculated_variable":"True",
            "formula":"first_name + ' ' + last_name",
            "var":"full_name"
        },
        {
            "instruction":"Hello %s , How are you? For a sample of my work I can show you how to make a transpose of a 3X3 matrix.",
            "instruction_var":[
                "full_name"
            ]
        },
        {
            "calculated_variable":"True",
            "formula":"[]",
            "var":"rows"
        },
        {
            "text":"Enter the first row of the matrix(3 integers space seperated).",
            "var":"rows[0]"
        },
        {
            "text":"Enter the second row of the matrix(3 integers space seperated).",
            "var":"rows[1]"
        },
        {
            "text":"Enter the third row of the matrix(3 integers space seperated).",
            "var":"rows[2]"
        },
        {
            "calculated_variable":"True",
            "formula":"[map(int, i.split()) for i in row]",
            "var":"matrix"
        },
        {
            "calculated_variable":"True",
            "formula":"[[matrix[j][i] for j in xrange(3)] for i in xrange(3)]",
            "var":"t_matrix"
        },
        {
            "instruction":"This is the transpose of the input matrix"
        },
        {
            "list_var":"True",
            "list_length":"3",
            "instruction":"Row %s : %s",
            "instruction_var":[
                "i+1",
                "str(t_matrix[i])"
            ]
        }
    ]
}"""

bot_answer="""[{}]"""
format_data = {}
first_name = ""
last_name = ""
full_name = ""
row = []
def bot_question(request, id=1):
   
    json_dict = json.loads(json_data)
    questions = json_dict.get("questions")
    
    if int(id) >= len(questions):
        return HttpResponseNotFound("Not Found")
    
#    for question in questions:
    question = questions[int(id)-1]
    if (question.get("text") == None and question.get("instruction") == None):
        question = questions[int(id)-1]
        
    
    question.update({"id":int(id)})
    question.update({"full_name":full_name})
    
#    return HttpResponse(question, content_type='application/json')
    return render(request, 'bot/question.html',question)
#    return(request, 'bot/question.html', {'question':question})
        
    
def answer_bot(request, id):
    data = {}
    json_dict = json.loads(json_data)
    questions = json_dict.get("questions")
    if int(id) >= len(questions):
        return HttpResponseNotFound("Not Found")
    
    if request.method == "POST":
        question = questions[int(id)].get('text')
        if(question == None):
            question = questions[int(id)].get('instruction')
        answer = request.POST['answer']
        data = {"stage"+ str(id) :{
    "Bot Says": [
      {
        "message": {
          "text": question
            
        }
      }
    ],
    "User Says": answer
  }}
        
#        For Gender
        if(str(question).find('gender')== True): 
           data = {"stage"+ str(id) :{
    "Bot Says": [
      {
        "message": {
          "text": question,
            "quick_replies": [
            {
              "content_type": "text",
              "title": "Male",
              "payload": "male"
            },
            {
              "content_type": "text",
              "title": "Female",
              "payload": "female"
            }]
            
        }
      }
    ],
    "User Says": answer
  }}
        if(str(question).find('first name')==True): 
            first_name = answer
        if(str(question).find('last name')==True): 
            last_name = answer
#            for Age
        if(str(question).find('age')==True): 
            answer_string = str(answer)
            if(answer_string.isdigit() == True):
                data = {"stage"+ str(id) :{
    "Bot Says": [
      {
        "message": {
          "text": question,
            "quick_replies": [
            {
              "content_type": "text",
              "title": "Male",
              "payload": "male"
            },
            {
              "content_type": "text",
              "title": "Female",
              "payload": "female"
            }]
            
        }
      }
    ],
    "User Says": answer
  }}
        
        
                id = int(id)+1
                full_name= first_name + last_name
                
#        Getting Each row of matrix
        if(str(question).find('row of the matrix') == True): 
            row.append(answer.split(" "))
            row.append([map(int, i.split()) for i in row])
            
#        For Calculating Transpose of matrix
        if(str(question).find('transpose of the input matrix') == True): 
            result  = numpy.transpose(row)
            data = {"stage"+ str(id) :
    {"Bot Says": [
        {
            "message":{
                "text":"This is the transpose of the input matrix"
            }
        },
        {
            "message":{
                "text":"Row 1 : " + str(result[0])
            }
        },
        {
            "message":{
                "text":"Row 2 : "+ str(result[1])
            }
        },
        {
            "message": {
                "text": "Row 3 : "+ str(result[2])
            }
        }

    ]}
     }
        
#    Write to json object
    with open("result.json", "a") as fp:
        json.dump(data,fp)
    page = str(int(id)+1)
    return redirect("/"+page)
