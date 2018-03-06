<html>
<head>
<title>Solar Pi Gardener</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<h2>
Solar Pi Gardener
</h2>
<?php
echo 'Battery voltage reading: ' . file_get_contents("/tmp-gardener/gardener_battery_voltage") . 'V ( ' . file_get_contents("/tmp-gardener/gardener_battery_percentage") . '% )<br>';
echo 'Moisture sensor reading: ' . file_get_contents("/tmp-gardener/gardener_moisture_sensor_value") . ' ( ' . file_get_contents("/tmp-gardener/gardener_moisture_sensor_percentage") . '% )<br>';
echo '<hr>';
echo '<b>Test Commands:</b><br>';
echo '<a href="send_command.php?cmd=water_pump_on&args[]=1">Pump water for 1 second</a><br>';
echo '<a href="send_command.php?cmd=water_pump_on&args[]=5">Pump water for 5 seconds</a><br>';
echo '<br>';
echo '<a href="send_command.php?cmd=ping">Send ping command</a><br>';
echo '<br>';
echo '<a href="send_command.php?cmd=system_reboot">Reboot system</a><br>';
?>

</body>
</html>
