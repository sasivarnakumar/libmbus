<?php
    $url = "https://myserver.mydomain.local/get_somedata.php";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);

//These next lines are for the magic "good cert confirmation"
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);
    curl_setopt($ch, CURLOPT_VERBOSE, true);

//for local domains:
//you need to get the pem cert file for the root ca or intermediate CA that you signed all the domain certificates with so that PHP curl can use it...sorry batteries not included
//place the pem or crt ca certificate file in the same directory as the php file for this code to work
    curl_setopt($ch, CURLOPT_CAINFO, __DIR__.'/cafile.pem');
    curl_setopt($ch, CURLOPT_CAPATH, __DIR__.'/cafile.pem');

//DEBUG: remove slashes on the next line to prove "SSL verify" is the cause       
//curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

//Error handling and return result
    if (curl_exec($ch) === false)
      {
       $result = curl_error($ch);
      }
    else
      {
       $result = curl_exec($ch);
      }
    // Close handle
    curl_close($ch);
    return $result;