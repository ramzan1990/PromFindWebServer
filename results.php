<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>PromID</title>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.6/flatly/bootstrap.min.css" crossorigin="anonymous">
    <link rel="stylesheet" href="css/main.css"> 
</head>
<body>
<div class="container">
        <div class="top" id="centered">
        </div>
        <div class="navdiv" id="centered">

        </div>

        <div  id="centered">
        <div  id="rm1">Please wait and do not press refresh. For large input, feel free to contact the developer directly to run the job!. </div>
        </div>
  <footer>    
  </footer>
        <script src="https://code.jquery.com/jquery-2.2.4.min.js" integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44=" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
        <script type="text/javascript" src="js/header.js"></script>
        <script type="text/javascript" src="js/navbar.js"></script>
        <script type="text/javascript" src="js/footer.js"></script>
        <script type="text/javascript">
            $('#indexNav').attr("class", "active");
        </script>

        <script type="text/javascript">
            $.post('result.php', {params: <?php 
             echo  json_encode($_POST)
                ?>, files: <?php            
             echo  json_encode($_FILES)
                ?>}
            ).then(function(htmlData) {
                $('#rm1').html(htmlData);
            });
        </script>   
</div>
</body>
</html>
