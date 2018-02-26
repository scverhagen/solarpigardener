<?php
if ( isset($_GET['cmd']) )
{
	file_put_contents("/tmp-gardener/gardener.cmd",$_GET['cmd']);
	echo 'Command sent:<hr>';
	echo file_get_contents("/tmp-gardener/gardener.cmd");
	echo "<hr>";
	echo 'Go <a href="javascript: history.go(-1);">back</a>.';

} else {
	echo 'No command specified';
	exit();
}

?>