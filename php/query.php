<?php

session_start();

header("content-type:application/json");

$fileName = $_FILES['file']['name'];
$fileType = $_FILES['file']['type'];
$fileError = $_FILES['file']['error'];
$fileContent = file_get_contents($_FILES['file']['tmp_name']);



if($fileError == UPLOAD_ERR_OK){
	$inp = $_FILES['file']['tmp_name'];
}else{
	$seq = $_POST["sequence"];
	$ec = $_POST["ec_number"];
	$file = tmpfile();
	$path = stream_get_meta_data($file)['uri'];
	fwrite($file, $seq . ',' . $ec);
	$inp  = $file;
}





// $bc = "cd jars; java -jar search.jar " . $ste;
// $bt = shell_exec($bc);
// $lines = explode(PHP_EOL, $bt);
// $prefix = "";
// $vt = "(";
// foreach ($lines as $line)
// {
// $vt .= $prefix . "'" . $line . "'";
// $prefix = ", ";
// }
// $vt .= ")";


echo json_encode(['ec' => $ec, 'file' => $fileName]);

exit();

?>
