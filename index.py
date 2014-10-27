# -*- coding: utf-8 -*-

from bottle import route, run, static_file, default_app, request
import json
from bottle import jinja2_template as template
import sys
sys.path.append('../puchimine/lib/puchimine')
import puchimine

# ----------------------------------------------
# どのルートでも使う処理を関数化
# ----------------------------------------------

def get_project(project_id):
    '''
    プロジェクト名を取得する
    '''
    project_dict = puchimine.load_project_name()
    project = project_dict[int(project_id)]

    return project

# ----------------------------------------------

def get_ticket(project_id,page):

    # 表示するチケットを制限したい場合は、tracker_idを入力する
    tracker_id = ''

    issue_dict,pages = puchimine.load_ticket_per_page(project_id=project_id,page=page,tracker_id=tracker_id)

    return issue_dict,pages

# ----------------------------------------------
# ルートを設定
# ----------------------------------------------

@route('/puchimine/project/<project_id>/<page>/')
def project(project_id,page):

    project = get_project(project_id)
    issue_dict,pages = get_ticket(project_id=project_id,page=page)

    project_member_dict = puchimine.load_project_member(project_id)

    return template('ticket',issue_dict = issue_dict, project = project,project_member_dict = project_member_dict, page=int(pages)+1)

# ----------------------------------------------

@route('/puchimine/project/<project_id>/<page>/', method="POST")
def project(project_id,page):

    #チケット追加処理。textareaの入力を受け取る。
    ticket_assign = request.POST.get('assign')
    ticket_subject = request.POST.get('subject')
    ticket_description = request.POST.get('ticket_description')

    puchimine.create_ticket(project_id,ticket_subject,ticket_assign,ticket_description)

    project = get_project(project_id)
    issue_dict,pages = get_ticket(project_id=project_id,page=page)

    project_member_dict = puchimine.load_project_member(project_id)

    return template('ticket',issue_dict = issue_dict, project = project, project_member_dict = project_member_dict, page=int(pages)+1)

# ----------------------------------------------

@route('/puchimine/project/<project_id>/<page>/issue/<issue_id>/', method="GET")
def project(project_id,issue_id,page):

    project = get_project(project_id)
    issue_dict,pages = get_ticket(project_id=project_id,page=page)

    issue_detail_dict = puchimine.load_ticket_detail_summary(issue_id)
    status_dict = puchimine.show_status()

    # チケットの詳細の中で入力されていない項目は-を代入しておく
    for key in issue_detail_dict:
        if issue_detail_dict[key] is None:
            issue_detail_dict[key] = '-'

    return template('ticket_detail',issue_dict = issue_dict, issue_detail_dict = issue_detail_dict,project = project,page=int(pages)+1,status_dict = status_dict )

# ----------------------------------------------

@route('/puchimine/project/<project_id>/<page>/issue/<issue_id>/' ,method="POST")
def project(project_id,issue_id,page):

    #更新処理。textareaの入力を受け取る。
    journal_update = request.forms.get('journal_update')
    status_update = request.forms.get('status')
    puchimine.update_journal(issue_id,journal_update,status_update)

    project = get_project(project_id)
    issue_dict,pages = get_ticket(project_id=project_id,page=page)

    issue_detail_dict = puchimine.load_ticket_detail_summary(issue_id)
    status_dict = puchimine.show_status()

    return template('ticket_detail',issue_dict = issue_dict, issue_detail_dict = issue_detail_dict ,project = project,page=int(pages)+1,status_dict = status_dict )

# ----------------------------------------------

@route('/puchimine/')
def index():
    project_dict = puchimine.load_project_name()
    return template('index',project_dict=project_dict)

# ----------------------------------------------
# テスト
# ----------------------------------------------

@route('/puchimine/cal/<project_id>/')
def index(project_id):
    var_data = puchimine.make_calendar_var(project_id=project_id,page="1",tracker_id="")

    return template('cal',var_data=var_data )

@route('/puchimine/cal/codebase/<filename:path>')
def static(filename):
    return static_file(filename, root='./views/codebase/')


# ----------------------------------------------

run(host='127.0.0.1', port=8082)
