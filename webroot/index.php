<html>
<head>
<title>Solar Pi Gardener</title>
</head>
<body>
<h2>
Solar Pi Gardener
</h2>
<?php
echo 'Voltage reading: ' . file_get_contents("/tmp-gardener/gardener_battery_voltage") . '<br>';
echo '<hr>';
echo '<b>Commands:</b><br>';
echo '<a href="send_command.php?cmd=fanon">Case Fan On</a><br>';
echo '<a href="send_command.php?cmd=fanoff">Case Fan Off</a>';
?>

</body>
</html>
