<!DOCTYPE html>
<html>
<head>
   <title>How to start</title>
   <script src="../codebase/dhtmlxscheduler.js" type="text/javascript"></script>
   <link rel="stylesheet" href="../codebase/dhtmlxscheduler.css" type="text/css">
</head>
<style type="text/css" media="screen">
	html, body{
		margin:0px;
		padding:0px;
		height:100%;
		overflow:hidden;
	}
</style>


<body>
    <div id="scheduler_here" class="dhx_cal_container" style='width:100%; height:100%;'>
        <div class="dhx_cal_navline">
            <div class="dhx_cal_prev_button">&nbsp;</div>
            <div class="dhx_cal_next_button">&nbsp;</div>
            <div class="dhx_cal_today_button"></div>
            <div class="dhx_cal_date"></div>
            <div class="dhx_cal_tab" name="day_tab" style="right:204px;"></div>
            <div class="dhx_cal_tab" name="week_tab" style="right:140px;"></div>
            <div class="dhx_cal_tab" name="month_tab" style="right:76px;"></div>
        </div>
        <div class="dhx_cal_header"></div>
        <div class="dhx_cal_data"></div>
    </div>

    <script type="text/javascript" charset="utf-8">

        scheduler.config.xml_date="%Y-%m-%d %H:%i";
        scheduler.config.first_hour = 8;
        scheduler.config.last_hour = 17;
        scheduler.config.start_on_monday = true;
        scheduler.config.full_day = true; 
        scheduler.init('scheduler_here',new Date(),"month");

        var events = [
        {% for data in var_data %}{{ data }},
        {% endfor %}
        ];

        scheduler.parse(events, "json");//takes the name and format of the data source

    </script>
</body>
</html>
