<?php
$op = shell_exec('cat /var/log/syslog | grep gardener');
$op = str_replace(["\r\n", "\r", "\n"], "<br/>", $op);
echo $op;

echo '<hr>';
echo 'Go <a href="http:/">back</a>.';
?>