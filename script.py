import requests
from bs4 import BeautifulSoup
import pandas as pd
#import numpy as np
from datetime import date,timedelta
from dateutil.relativedelta import relativedelta
import re
import yaml
def active():
  for index, row in df_new.iterrows():
    if row['posted_time'].find('Hot')!=-1:
        df_new.loc[index, 'actively_hiring/hiring'] = 'Actively hiring'
    else:
        df_new.loc[index, 'actively_hiring/hiring'] = 'hiring'
def extractexp(i):
  result=re.findall(r'\d+',i)
  if result:
    return tuple(int(x) for x in result)
  else:
    return 0
def convertingdate(integer_value):
  current_date=date.today()
  for i in range(0,len(integer_value)):
    if 'days' or 'day' in df_new['posted_time'][i]:
      new_date=current_date-timedelta(days=integer_value[i])
    elif 'week' or 'weeks' in df_new['posted_time'][i]:
      new_date=current_date-timedelta(weeks=integer_value[i])
      #print(new_date)
    elif 'month' in df_new['posted_time'][i]:
      new_date=current_date-relativedelta(months=integer_value[i])
    #print(new_date)
    new_dates.append(new_date)

def extract_integer(i):
  result=re.search(r'\d',i)
  if result:
        return int(result.group())
  else:
    return 0
def all_description(all_links):
  #print(len(all_links))
  for i in all_links:
    #print(i)
    u=i
    try:
      res=requests.get(u)
      res.raise_for_status()
      #creating beautiful soup object
      s=BeautifulSoup(res.text,'html.parser')
      #finding details of the job
      company=s.find('div',class_='JobDetailWidget_jobCard_cName__qvsdW').text
      #print(company)

      experience=s.find('div',class_='JobDetailWidget_jobCard_lists_item__w6Yow JobDetailWidget_jobIcon__mjaNB undefined').text

      type_of_job=s.find('ul',class_='JobDetailWidget_jobCard_jobDetail__Yyn2o').text

      job_detail=s.find('div',class_='jobDetail_jsrpRightDetail_text__jqs8a').text

      city=s.find('div',class_='JobDetailWidget_jobCard_lists_item__w6Yow JobDetailWidget_locationIcon__u85a7').text

      skill=s.find('ul',class_='keyskills_keySkills_items__ej9_3')
      sk=skill.find_all('li')
      skill_li=[]
      for l in sk:
        skill_li.append(l.text)
      skill_string=','.join(skill_li)



      recruter_detail=s.find('div',class_='recruiterDetails_recruiterDetails__rL2nh white-box-border').text

      job_link=i


      post_t=s.find('div',class_='JobDetailWidget_jobCard_features__iHE_w').text


      #appending all the data into lists
      companys.append(company)
      experiences.append(experience)
      type_of_jobs.append(type_of_job)
      job_details.append(job_detail)
      citys.append(city)
      skills.append(skill_string)
      recruter_details.append(recruter_detail)
      job_links.append(job_link)
      posted_time.append(post_t)




    except requests.exceptions.HTTPError as err:
      print(f"http err occured:{err}")
    except Exception as err:
      print(f"other error occured:{err}")





def items(container):
  box=container.find_all('meta')
  #print(box)
  for i in range(0,len(box),2):
    all_links.append(box[i]['content'])
    #print(box[i]['content'])
  #print(all_links)
def get(url):
  try:
   response=requests.get(url)
   response.raise_for_status()
  except requests.exceptions.HTTPError as err:
   print(f"http error occured :{err}")
  except Exception as err:
   print(f'Other error occurred: {err}')
  soup=BeautifulSoup(response.text,"html.parser")
  #print(soup.prettify())
  container=soup.find('div',class_='parentClass position-relative')
  #print(container.prettify())
  items(container)


if __name__=='__main__':
    companys=[]
    experiences=[]
    type_of_jobs=[]
    job_details=[]
    citys=[]
    skills=[]
    recruter_details=[]
    job_links=[]
    posted_time=[]
    all_links=[]
    new_dates=[]
    #reading yaml
    with open("config.yaml") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    type=cfg['type']
    pages=cfg['pages']
    filename=cfg['filename']
    for i in range(1,pages+1):
        url=f"https://www.shine.com/job-search/data-analyst-jobs-{i}?q={type}"
        get(url)
    all_description(all_links)
    df=pd.DataFrame({
   'company':companys,
   'experience':experiences,
   'type':type_of_jobs,
   'rec_details':recruter_details,
   'job details':job_details,
   'city':citys,
    'skills':skills,
    'details':recruter_details,
    'job_link':job_links,
    'posted_time':posted_time,})
    df_new=df.drop_duplicates()
    #for date
    integer_value=[extract_integer(i) for i in df_new['posted_time']]
    convertingdate(integer_value)
    df_new.loc[:, 'posted_date'] = new_dates
    #for experience
    integer=[extractexp(i) for i in df_new['experience']]
    df_new['experience in int']=integer
    
    active()
    df_sorted=df_new.sort_values(by='experience in int')
    df_sorted.drop(columns=['experience'],inplace=True)
    df_sorted.to_csv(f'{filename}{type}.csv',index=False)
    
    
    
    
    

    
    