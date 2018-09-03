<?php
    $count = intval(file_get_contents('so/count.txt'));
    file_put_contents('so/count.txt', ++$count);
    $file = 'so/PromID_Dist.zip';
	if (file_exists($file)) {
	    header("Location: $file");
		exit;
	}
?>
