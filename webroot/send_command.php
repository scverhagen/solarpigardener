<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<?php
if ( !isset($_GET['cmd']) )
{
	echo 'No command specified';
	exit();
}

	if ( !isset($_GET['args']) )
	{
		$args[] = "0";
		$argcount = '0';
	} else {
		$args = $_GET['args'];
		$argcount = count($args);
	}

	echo '<b>Command:</b><hr>';
	echo $_GET['cmd'];
	echo "<hr>";
	
	echo '<br>';
	echo '<b>Arguments passed:</b><hr>';
	print_r($args);
	echo '<hr>';

	// write files (write gardener.cmd last):
	file_put_contents("/tmp-gardener/gardener.cmd",$_GET['cmd']);
	file_put_contents("/tmp-gardener/gardener.cmdargcount",$argcount );
	for ($i = 0; $i < count($args); $i++)
	{
            file_put_contents("/tmp-gardener/gardener.cmdargs",$args[$i].PHP_EOL, FILE_APPEND );
	}
	
	echo 'Go <a href="http:/">back</a>.';



?>

</body>
<html>
