{% include 'base_top.html' %}
    <div class="row">
        <div class="col-md-4">
            <h2>プロジェクト一覧</h2>
            <ul class="project">
                {% for dict_key in project_dict %}
                    <li><a href="../puchimine/project/{{ dict_key }}/">{{ project_dict[dict_key] }}</a></li>
                {% endfor %}
            </ul>
        </div>
        <div class="col-md-8">
        </div>
    </div>
</div>
</body>
</html>
