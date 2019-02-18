<?php
$result=$_GET['jobid'];
$result = trim($result,"'"); 
$result = trim($result,'"'); 
$result = preg_replace('/\s+/', '', $result);

if(!file_exists($result . "_cf")){
    echo "RUNNING";
    die();
}

$data = file_get_contents($result);

$needle = "This is the final result!!";
if(strrpos ( $data , $needle) !== false){
    $sdata = substr($data, strrpos ( $data , $needle) + strlen($needle) + 1);
    file_put_contents($result, strip_tags($sdata));
    $rows = str_getcsv($sdata, "\n"); 
    foreach($rows as &$Row) $Row = str_getcsv($Row, ","); 
    $table1 = "<p style='text-align:right;'>Promoter elements: <span style='background-color:#b3ccff;'>TSS </span>&nbsp;&nbsp;<span style='background-color:#ffe0b3;'>Initiator </span>&nbsp;&nbsp;<span style='background-color:#c2efc2;'>TCT </span>&nbsp;&nbsp;<span style='background-color:#ffb3b3;'>TATA-box</span>&nbsp;&nbsp;<span style='background-color:#b3ffff;'>CCAAT-box</span></p>";
    $table1 .= "<table class='table'><col span='1' class='wide'>";
    $table1 .= "<tr><th><h3>Results</h3></th></tr>";  
    foreach ($rows as $row) {
        $table1 .= "<tr>";
        for ($x = 0; $x < 1; $x++) {
        	$column = $row[$x];
            $table1 .=  "<td>$column</td>";
        }
        $table1 .= "</tr>";
    } 
    $table1 .= "</table>";
    $table1 .= "<a href='$result' download>Download the results</a>";
    echo  $table1;
}else{
    $eout = 'PromID could not run with the provided input!';
    $needle = 'This is the final error message!!';
    if(strrpos ( $data , $needle) !== false){
        $eout = substr($data, strrpos ( $data , $needle) + strlen($needle) + 1);
        $eout = preg_replace('/\r\n|\r|\n/', ' <br /> ', trim($eout));
    }
    #echo $eout;
    #echo "\n";
    echo $result;
    #echo "\n";
    #echo $data;
} 
?>