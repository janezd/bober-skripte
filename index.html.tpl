<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>{title}</title>
    <script src="/static/js/jquery.js"></script>
    <script src="/static/js/taskfunctions.js"></script>
    <link rel="stylesheet" href="../task.css">
</head>
<body>
<div>
    <p>Besedilo</p>
    <img src="resources/FIX_ME.svg" width="500px"/>
    <img style="float: right; margin-left: 20px" src="resources/FIX_ME.svg" width="350px"/>
    <img src="resources/FIX_ME" />
    <p>Vprašanje</p>
</div>
<form action="get" onsubmit="return false;" style="margin-top: 20px">
    <div id="answers">
    {answers}
    </div>

</form>
</body>
</html>
