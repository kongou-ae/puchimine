# -*- coding: utf-8 -*-

from bottle import route, run, static_file, default_app, request
import json
from bottle import jinja2_template as template
import sys
sys.path.append('../puchimine/lib/puchimine')
import puchimine

@route('/puchimine/project/<project_id>/')
def project(project_id):

    project_dict = puchimine.load_project_name()
    project = project_dict[int(project_id)]
    issue_dict = puchimine.load_ticket_summary(project_id)

    project_member_dict = puchimine.load_project_member(project_id)

    return template('ticket',issue_dict = issue_dict, project = project,project_member_dict = project_member_dict)

@route('/puchimine/project/<project_id>/', method="POST")
def project(project_id):

    #チケット追加処理。textareaの入力を受け取る。
    ticket_assign = request.POST.get('assign')
    ticket_subject = request.POST.get('subject')
    ticket_description = request.POST.get('ticket_description')

    puchimine.create_ticket(project_id,ticket_subject,ticket_assign,ticket_description)

    project_dict = puchimine.load_project_name()
    project = project_dict[int(project_id)]
    issue_dict = puchimine.load_ticket_summary(project_id)
    return template('ticket',issue_dict = issue_dict, project = project,project_member_dict = project_member_dict)

@route('/puchimine/project/<project_id>/issue/<issue_id>/', method="GET")
def project(project_id,issue_id):

    project_dict = puchimine.load_project_name()
    project = project_dict[int(project_id)]
    issue_dict = puchimine.load_ticket_summary(project_id)
    issue_detail_dict = puchimine.load_ticket_detail_summary(issue_id)

    # チケットの詳細の中で入力されていない項目は-を代入しておく
    for key in issue_detail_dict:
        if issue_detail_dict[key] is None:
            issue_detail_dict[key] = '-'

    return template('ticket_detail',issue_dict = issue_dict, issue_detail_dict = issue_detail_dict,project = project)

@route('/puchimine/project/<project_id>/issue/<issue_id>/' ,method="POST")
def project(project_id,issue_id):

    #更新処理。textareaの入力を受け取る。
    journal_update = request.forms.get('journal_update')
    puchimine.update_journal(issue_id,journal_update)

    issue_dict = puchimine.load_ticket_summary(project_id)
    issue_detail_dict = puchimine.load_ticket_detail_summary(issue_id)

    return template('ticket_detail',issue_dict = issue_dict, issue_detail_dict = issue_detail_dict  )

@route('/puchimine/')
def index():
    project_dict = puchimine.load_project_name()
    return template('index',project_dict=project_dict)

run(host='127.0.0.1', port=8082)
