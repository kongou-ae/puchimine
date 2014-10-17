{% include 'base_top.html' %}
    <div class="row">
        <div class="col-md-4">
            <h2><a href="../../">{{ project }}</a></h2>
            <ul class="ticket">
                {% for issue_key in issue_dict %}
                    <li><a href="../{{ issue_key }}/">{{ issue_dict[issue_key] }}</a></li>
                    {% endfor %}
            </ul>
            <ul class="pagination">
                <li class="disabled"><a href="#">&laquo;</a></li>
                {% for i in range(1,page) %}
                <li><a href="../../../{{ i }}/">{{ i }}</a></li>
                <li><a href="#">&raquo;</a></li>
                {% endfor %}
            </ul>
        </div>
        <div class="col-md-8">
            <!-- <div data-spy="affix" data-offset-top="60" data-offset-bottom="200"> -->
                <table class="table table-bordered table-hover">
                    <tbody>
                    <tr>
                        <th colspan="4">#{{ issue_detail_dict['id']  }} : {{ issue_detail_dict['subject'] }}</th>
                    </tr>
                    <tr>
                        <th>概要</th><td colspan="3">{{ issue_detail_dict['description'] }}</td>
                    </tr>
                    <tr>
                        <th>担当者</th><td>{{ issue_detail_dict['assigned_to'] }}</td>
                        <th>ステータス</th><td>{{ issue_detail_dict['status'] }}</td>
                    </tr>
                    </tbody>
                </table>
                <form  role="form" method="POST" enctype="multipart/form-data" accept-charset="UTF-8">
                    <div class="form-group">
                        <textarea class="form-control" rows="3" name="journal_update" placeholder="更新内容を入力"></textarea>
                    </div>
                    <div class="form-group">
                        <select class="form-control" name="status">
                            {% for id in status_dict  %}
                                {% if status_dict[id] == issue_detail_dict['status'] %}
                                    <option value="{{ id }}" selected>{{ status_dict[id] }}</option>
                                {% else%}
                                    <option value="{{ id }}">{{ status_dict[id] }}</option>
                                {% endif %}
                            {% endfor %}
                        </select>
                    </div>
                    <div class="form-group">
                        <button type="submit" class="btn btn-default">更新</button>
                    </div>
                </form>
                {% for journal in issue_detail_dict['journals'] %}
                <table class="table table-bordered table-hover table-condensed">
                    <tbody>
                    <tr>
                        <td>{{ journal['created_on'] }}</td><td>{{ journal['user']['name'] }}</td>
                    </tr>
                    <tr>
                        <td colspan="2">{{ journal['notes'] }}</td>
                    </tr>
                </tbody>
                </table>
                {% endfor %}
            <!--  </div> -->
        </div>
    </div>
</body>
</html>
