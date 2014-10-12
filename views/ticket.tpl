{% include 'base_top.html' %}
    <div class="row">
        <div class="col-md-4">
            <h2><a href="./">{{ project }}</a></h2>
            <ul class="ticket" >
                {% for issue_key in issue_dict %}
                    <li><a href="issue/{{ issue_key }}/">{{ issue_dict[issue_key] }}</a></li>
                {% endfor %}
            </ul>
        </div>
        <div class="col-md-8">
            <form role="form" method="POST" enctype="multipart/form-data" accept-charset="UTF-8">
                <div class="form-group">
                    <label class="col-sm-2 control-labe">チケット名</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" name="subject" placeholder="チケット名を入力">
                    </div>
                    <label class="col-sm-2 control-labe">担当者</label>
                    <div class="col-sm-10">
                        <select class="form-control" name="assign">
                            {% for id in project_member_dict %}
                            <option value="{{ id }}">{{ project_member_dict[id] }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <label class="col-sm-2 control-labe">概要</label>
                    <div class="col-sm-10">
                        <textarea class="form-control" rows="5" name="ticket_description" placeholder="チケットの概要を入力"></textarea>
                    </div>
                    <div class="col-sm-offset-2 col-sm-10">
                        <button type="submit" class="btn btn-default">チケット登録</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
</body>
</html>
