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
echo 'Voltage reading: ' . file_get_contents("/tmp-gardener/gardener_battery_voltage") . 'V ( ' . file_get_contents("/tmp-gardener/gardener_battery_percentage") . '% )<br>';
echo '<hr>';
echo '<b>Test Commands:</b><br>';
echo '<a href="send_command.php?cmd=water_pump_on&args[]=1">Pump water for 1 second</a><br>';
echo '<a href="send_command.php?cmd=water_pump_on&args[]=5">Pump water for 5 seconds</a><br>';
echo '<br>';
echo '<a href="send_command.php?cmd=system_reboot">Reboot system</a><br>';
echo '<a href="send_command.php?cmd=system_poweroff">Power system OFF</a><br>';
?>

</body>
</html>
