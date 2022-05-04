import json
import urllib.parse
import boto3
import csv
import requests
import datetime
import smtplib

s3 = boto3.client('s3')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    final_dict={}
    try:
        headers = {"Content-Type": "application/json"}
        URL= "https://7e8tdmhsh1.execute-api.us-east-2.amazonaws.com/items"
        
        response = s3.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read().decode('utf-8').splitlines()
        lines = csv.reader(data)
        next(lines) # skips the first(header) line
        for line in lines:
         PARAMS = {"Id":line[0], "Date":line[1], "Transaction":line[2]}
         # sending get request and saving the response as response object
         r = requests.put(url = URL, data=json.dumps(PARAMS), headers=headers)
         print(r.text)
         
        
        #After preserve all the info in the Database, proceed to calculate
        month_set=set()
        month_transactions=[]
        total_ammount=[]
        getResult=requests.get(url = URL).json()
        print('getResult: %s' %(getResult))
        for x in getResult['Items']:
            #print('element: %s' %(x))
            #print('elementType: %s' %(type(x)))
            month_set.add(x['Date'].split("/")[0])
            #print('month_set: %s' %(month_set))
            total_ammount.append((float(eval(x['Transaction'].replace('\'', '')))))
            #print('total_ammount: %s' %(total_ammount))
            month_transactions.append(x['Date'].split("/")[0])
            #print('month_transactions: %s' %(month_transactions))
    
    
        for month_num in month_set:
            datetime_object = datetime.datetime.strptime(month_num, "%m")
            full_month_name = datetime_object.strftime("%B")
            print('Number of transactions in {}: {}'.format(full_month_name,month_transactions.count(month_num)))
            #final_dict['month-']=month_transactions.count(month_num)
            
        
        total_balance=0
        debit_list=[]
        credit_list=[]
        for x in total_ammount:
            total_balance=total_balance+x
            if x <0:
                debit_list.append(x)
            else:
                credit_list.append(x)
        print('Total balance is: {}'.format(round(total_balance,2)))
        print('Average debit amount: {}'.format(round(sum(debit_list)/len(debit_list),2)))
        print('Average credit amount:  {}'.format(round(sum(credit_list)/len(credit_list),2)))
        final_dict["total_balance"]=round(total_balance,2)
        final_dict["avg_debit"]=round(sum(debit_list)/len(debit_list),2)
        final_dict["avg_credit"]=round(sum(credit_list)/len(credit_list),2)
        print(final_dict)
        #send_email()
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e



# =============================================================================
# SEND EMAIL FUNCTION
# =============================================================================
def send_email():
    
    gmail_user = 'gilvefi@gmail.com'
    gmail_app_password = "fwqltuutrfwdcicl"
    sent_from = gmail_user
    sent_to = ['gilbertovelazquez@live.com.mx']
    sent_subject = "Account balance for Stori"
    sent_body = """\
Greetings!

Cela ressemble à un excellent recipie[1] déjeuner.

[1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718

--Please don't respond to this email, instead you can contact to @stori_mx
"""

    email_text = """\
From: %s
To: %s
Subject: %s
%s
""" % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, email_text.encode("utf-8"))
        server.close()
        print(email_text)
        print('Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
# =============================================================================
# END OF SEND EMAIL FUNCTION
# =============================================================================
