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

echo '<hr>';
echo '<b>Watering Schedule for ' . file_get_contents("/tmp-gardener/gardener_plant_name") . ' plant:</b><br>';
echo 'At ' . file_get_contents("/tmp-gardener/gardener_plant_sched_hour") . ':00, apply water to plant (for ' . file_get_contents("/tmp-gardener/gardener_plant_water_duration") . ' seconds) if soil moisture percentage is below ' . file_get_contents("/tmp-gardener/gardener_plant_soil_min_moisture_percentage") . '%<br>';
echo 'Current moisture sensor reading: ' . file_get_contents("/tmp-gardener/gardener_moisture_sensor_value") . ' ( ' . file_get_contents("/tmp-gardener/gardener_moisture_sensor_percentage") . '% )<br>';
echo '<hr>';
echo '<a href="index.php">Refresh</a><br><br>';
echo '<a href="debug.php">Debug Menu</a><br>';
?>

</body>
</html>
