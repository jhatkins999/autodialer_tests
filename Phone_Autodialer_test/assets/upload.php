<?php
$target_dir "csvfiles/";
$target_fiel = $target_dir . basename($_FILES["myfile"]["name"]);
$uploadOK = 1;
$FileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

if (file_exists($target_file)
{
    echo "file has already been submitted";
    $uploadOK = 0;
}

if ($_FILES["myfile"]["size"] > 500000)
{
    echo "File is too large to upload";
    $uploadOK = 0;
}

if ($FileType != 'csv')
{
    echo "Only csv files are allowed, please convert to a csv";
    $uploadOK = 0;
}

if ($uploadOk == 0) {
  echo "File failed to upload";
// if everything is ok, try to upload file
} else {
  if (move_uploaded_file($_FILES["myfile"]["tmp_name"], $target_file)) {
    echo "The file ". basename( $_FILES["myfile"]["name"]). " has been uploaded.";
  } else {
    echo "Sorry, there was an error uploading your file.";
  }
}
?>


