<?php
    if(!file_exists($_FILES['file']['tmp_name']) || !is_uploaded_file($_FILES['file']['tmp_name'])) {
        $query_name = "single_" . time();
        $new_file = "PromID/files/" . $query_name .'.fasta';
        $content = ">" . $_POST["knowledge"] . "\n" . $_POST["sequence"];
        file_put_contents($new_file, $content);
    }else {
        $tmp_name = $_FILES['file']['tmp_name'];   
        $path_parts = pathinfo($_FILES["file"]["name"]);
        $fn = $path_parts['filename'];
        $fn = preg_replace("/[^-_a-z0-9]+/i", "_", $fn);
        $query_name = $fn .'_'.time();
        $new_file = "PromID/files/" . $query_name .'.'. $path_parts['extension'];
        move_uploaded_file($_FILES['file']['tmp_name'], $new_file);
    }
    putenv("PATH=/usr/local/cuda/bin:/usr/local/cuda-8.0/bin:/usr/local/cuda-9.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:");
    putenv("LD_LIBRARY_PATH=/usr/local/cuda/lib64");
    $data = shell_exec ( 'PromID/main.sh ' . "$new_file 2>&1" );
    $needle = "This is the final result!!";
    if(strrpos ( $data , $needle) !== false){
        $sdata = substr($data, strrpos ( $data , $needle) + strlen($needle) + 1);
        file_put_contents("PromID/files/" . $query_name . ".res", $sdata);
        $rows = str_getcsv($sdata, "\n"); 
        foreach($rows as &$Row) $Row = str_getcsv($Row, ","); 
        $table1 = "<table class='table'><col span='1' class='wide'>";
        $table1 .= "<tr><th>Sequence</th></tr>";  
        foreach ($rows as $row) {
            $table1 .= "<tr>";
            for ($x = 0; $x < 1; $x++) {
	        	$column = $row[$x];
                $table1 .=  "<td>$column</td>";
            }
            $table1 .= "</tr>";
        } 
        $table1 .= "</table>";
        $table1 .= "<a href='PromID/files/" . $query_name . ".res' download>Download the results</a>";
        echo  $table1;
    }else{
        $eout = 'PromID could not run with the provided input!';
        $needle = 'This is the final error message!!';
        if(strrpos ( $data , $needle) !== false){
            $eout = substr($data, strrpos ( $data , $needle) + strlen($needle) + 1);
            $eout = preg_replace('/\r\n|\r|\n/', ' <br /> ', trim($eout));
        }
        echo $eout; 
    }
    #echo $data;
?>
