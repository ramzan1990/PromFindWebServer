<?php
    if(!file_exists($_FILES['file']['tmp_name']) || !is_uploaded_file($_FILES['file']['tmp_name'])) {
        $query_name = "single_" . time();
        $new_file = "PromID/files/" . $query_name .'.fasta';
        $content = $_POST["sequence"];
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
    clearstatcache();
    if(filesize($new_file) > 10000000 || filesize($new_file) < 20){
        echo "File size is too big! Maximum size is 10 MB";
        unlink($new_file);
    }else{
        putenv("PATH=/usr/local/cuda/bin:/usr/local/cuda-8.0/bin:/usr/local/cuda-9.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:");
        putenv("LD_LIBRARY_PATH=/usr/local/cuda/lib64");
        $dt = $_POST["dt"];
        $md = $_POST["md"];
        $resfile = $new_file . ".res";
        #$resfile = str_replace("PromID/files/","",$resfile);
        $data = shell_exec ("bash PromID/main.sh " . $new_file . " " . $resfile .  " " . $dt  . " " . $md . " > /dev/null 2>/dev/null &");
        echo $resfile;
        die();
    }
    #echo $data;
?>
