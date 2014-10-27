# -*- coding: utf-8 -*-

import json
import requests
import datetime
import collections
import math
import datetime

def config_load():
    '''
    設定ファイルから必要なパラメータを取得する
    '''
    config = json.load(open('config.json'))
    redmine_url = config[0]['redmine_url']
    redmine_api_key = config[0]['redmine_api_key']

    return(redmine_url,redmine_api_key)

def load_project_name():
    '''
    プロジェクトのIDと名前をdictで返す
    '''

    redmine_url,redmine_api_key = config_load()
    project_dict = collections.OrderedDict()

    url = redmine_url + 'projects.json?limit=100'
    r = requests.get(url,headers={'Content-Type': 'application/json','X-Redmine-API-Key': redmine_api_key})
    data = json.loads(r.text)

    for i in range(0,len(data['projects'])):
        project_name = data['projects'][i]['name']
        project_id = data['projects'][i]['id']
        project_dict[project_id] = project_name

    return project_dict

def load_project_member(project_id):
    '''
    プロジェクトに参加しているメンバーのIDと名前をdictで返す
    '''
    redmine_url,redmine_api_key = config_load()
    project_member_dict = {}

    url = redmine_url + 'projects/' + project_id + '/memberships.json?limit=100'
    r = requests.get(url,headers={'Content-Type': 'application/json','X-Redmine-API-Key': redmine_api_key})
    data = json.loads(r.text)

    for i in range(0,len(data['memberships'])):
        user_name = data['memberships'][i]['user']['name']
        user_id = data['memberships'][i]['user']['id']
        project_member_dict[user_id] = user_name

    return project_member_dict

def load_ticket_per_page(project_id,page,tracker_id):
    '''
    プロジェクトに含まれるチケットの情報をjsonで返す
    '''
    redmine_url,redmine_api_key = config_load()
    issue_dict = collections.OrderedDict()

    # ページ数を確認する
    if tracker_id == '':
        url = redmine_url + 'issues.json?project_id=' + project_id
    else:
        url = redmine_url + 'issues.json?project_id=' + project_id + '&tracker_id=' + tracker_id

    r = requests.get(url,headers={'Content-Type': 'application/json','X-Redmine-API-Key': redmine_api_key})
    data = json.loads(r.text)
    pages = math.floor(data['total_count']/data['limit']) +1

    # 指定されたページのチケットを取得する
    if tracker_id == '':
        url = redmine_url + 'issues.json?project_id=' + project_id + '&page=' + page
    else:
        url = redmine_url + 'issues.json?project_id=' + project_id + '&page=' + page + '&tracker_id=' + tracker_id

    r = requests.get(url,headers={'Content-Type': 'application/json','X-Redmine-API-Key': redmine_api_key})
    data = json.loads(r.text)

    for i in range(0,len(data['issues'])):
        issue_name = data['issues'][i]['subject']
        issue_id = data['issues'][i]['id']
        issue_dict[issue_id] = issue_name

    return issue_dict,pages


def load_ticket_detail_summary(ticket_id):
    '''
    チケットIDを受け取り、チケットの詳細をdictで返す
    '''
    redmine_url,redmine_api_key = config_load()
    issue_detail_dict = {}

    url = redmine_url + 'issues/' + ticket_id + '.json?include=journals&limit=100'
    r = requests.get(url,headers={'Content-Type': 'application/json','X-Redmine-API-Key': redmine_api_key})
    data = json.loads(r.text)

    issue_detail_dict['id'] = data['issue']['id']
    issue_detail_dict['status'] = data['issue']['status']['name']

    # 担当者未割当を確認し-を代入しておく
    try:
        issue_detail_dict['assigned_to'] = data['issue']['assigned_to']['name']
    except KeyError:
        issue_detail_dict['assigned_to'] = '-'

    issue_detail_dict['subject'] = data['issue']['subject']
    issue_detail_dict['description'] = data['issue']['description']
    issue_detail_dict['journals'] = data['issue']['journals']

    # 開始日未設定を確認し、-を代入しておく。
    try:
        issue_detail_dict['start_date'] = data['issue']['start_date']
    except KeyError:
        issue_detail_dict['start_date'] = '-'

    # 終了日未設定を確認し、-を代入しておく。
    try:
        issue_detail_dict['due_date'] = data['issue']['due_date']
    except KeyError:
        issue_detail_dict['due_date'] = '-'

    # journalsを逆順にソートする。
    #issue_detail_dict['journals'] = list(reversed(issue_detail_dict['journals']))
    # 時刻をJST(+9)に変更。bottleがコードが渡す時にJSTにできないの？
    for journal in issue_detail_dict['journals']:
        created_on = journal['created_on']
        created_on = datetime.datetime.strptime(created_on,'%Y-%m-%dT%H:%M:%SZ')
        created_on = created_on + datetime.timedelta(hours=9)
        journal['created_on'] = created_on.strftime('%Y-%m-%d %H:%M:%S')

    return issue_detail_dict

def show_status():
    '''
    ステータスを取得する
    '''
    redmine_url,redmine_api_key = config_load()
    status_dict = {}

    url = redmine_url + 'issue_statuses.json'
    r = requests.get(url,headers={'Content-Type': 'application/json','X-Redmine-API-Key': redmine_api_key})
    data = json.loads(r.text)

    for i in range(0,len(data['issue_statuses'])):
        status_id = data['issue_statuses'][i]['id']
        status_name = data['issue_statuses'][i]['name']
        status_dict[status_id] = status_name

    return status_dict

def update_journal(issue_id,journal_update,status_update):
    '''
    チケットIDと更新履歴を受け取り、チケットを更新する
    '''

    journal_update = journal_update.replace('\r\n','<br />')
    data = {
                    "issue": {
                        "notes": "{0}".format(journal_update),
                        "status_id" : "{0}".format(status_update)
                    }
                }

    data = json.dumps(data, ensure_ascii=False)
    redmine_url,redmine_api_key = config_load()
    url = redmine_url + 'issues/' + issue_id + '.json'
    r = requests.put(url,headers={'Content-Type': 'application/json','X-Redmine-API-Key': redmine_api_key},data=data.encode('utf-8'))

def create_ticket(project_id,ticket_subject,ticket_assign,ticket_description):
    '''
    チケットを追加する
    '''

    ticket_description = ticket_description.replace('\r\n','<br />')

    data = {
                    "issue": {
                        "project_id": "{0}".format(project_id),
                        "subject": "{0}".format(ticket_subject),
                        "assigned_to_id": "{0}".format(ticket_assign),
                        "description": "{0}".format(ticket_description)
                    }
                }

    data = json.dumps(data, ensure_ascii=False)
    redmine_url,redmine_api_key = config_load()
    url = redmine_url + 'issues.json'

    requests.post(url,headers={'Content-Type': 'application/json','X-Redmine-API-Key':redmine_api_key},data=data.encode('utf-8'))

def make_calendar_var(project_id,page,tracker_id):

    calendar_list = []

    # プロジェクトIDに含まれるチケットのページ数を確認する
    issue_dict,pages = load_ticket_per_page(project_id,page,tracker_id)

    # ページ数でforを回して、全てのチケットIDを配列に入れる。
    for page in range(1,int(pages)+1):
        issue_dict,page = load_ticket_per_page(project_id,str(page),tracker_id)
        # チケットIDでforをまわして、全てのカレンダーに必要な情報をjsonにしリストに入れる
        for i in list(issue_dict.keys()):
            issue_detail_dict = load_ticket_detail_summary(str(i))

            # 開始日と終了日が-でなければ、日付が入っていると判断。
            if  issue_detail_dict['start_date']  != '-' and issue_detail_dict['due_date']  != '-':
                # fullday表示にするために、終了日に1日足しこむ
                tmp = datetime.datetime.strptime( issue_detail_dict['due_date'], "%Y-%m-%d") + datetime.timedelta(days=1)
                issue_detail_dict['due_date'] = tmp.strftime("%Y-%m-%d")
            # 開始日か終了日が-であれば、仮の日付を入れる。
            else:
                issue_detail_dict['start_date'] = '2000-01-01'
                issue_detail_dict['due_date'] = issue_detail_dict['start_date']

            var_line = '{id:'+ str(issue_detail_dict['id']) + ', text:"【'+ issue_detail_dict['assigned_to'] + '】'  + issue_detail_dict['subject'] + '", start_date:"' + issue_detail_dict['start_date'] + ' 00:00", end_date:"' + issue_detail_dict['due_date'] +' 00:00"}'

            calendar_list.append(var_line)

    return calendar_list

if __name__ == '__main__':
    project_dict = load_project_name()
    #print(project_dict)

    #issue_dict = load_ticket_summary("1")
    #print(issue_dict)

    #issue_dict = load_ticket_per_page("1","1","")

    #issue_detail_dict = load_ticket_detail_summary("12")
    #print(issue_detail_dict)

    #project_member_dict = load_project_member("1")
    #print(project_member_dict)
    #update_journal("7","pythonで更新")
    #print(show_status())

    make_calendar_var("1","1","")
