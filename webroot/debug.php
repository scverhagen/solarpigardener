<html>
<head>
<title>Solar Pi Gardener - DEBUG</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<h2>Solar Pi Gardener</h2>
<h3>DEBUG Menu</h3>

<?php
echo 'Battery voltage reading: ' . file_get_contents("/tmp-gardener/gardener_battery_voltage") . 'V ( ' . file_get_contents("/tmp-gardener/gardener_battery_percentage") . '% )<br>';
echo '<hr>';
echo '<b>Test Commands:</b><br>';
echo '<a href="send_command.php?cmd=check_moisture">Force update of moisture param</a><br><br>';
echo '<a href="send_command.php?cmd=do_maint">Force plant maintenance</a><br><br>';
echo '<a href="send_command.php?cmd=water_pump_on&args[]=5">Pump water for 5 seconds</a><br><br>';
echo '<a href="send_command.php?cmd=ping">Send ping command</a><br><br>';
echo '<a href="syslog.php">View syslog</a><br><br>';
echo '<a href="send_command.php?cmd=system_reboot">Reboot system</a><br>';


echo '<hr>';
echo 'Go <a href="http:/">back</a>.';
?>
