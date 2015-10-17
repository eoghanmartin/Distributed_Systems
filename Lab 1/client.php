<?php

$host    = "localhost";
$port    = 8000;

$message = "GET /echo.php?message=caps HTTP/1.1\r\n\r\n\r\n";

$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Socket wasn't created.\n");
echo "socket created\n";

$result = socket_connect($socket, $host, $port) or die("Server connection failure.\n");
echo "socket connected\n"; 

socket_write($socket, $message, strlen($message)) or die("Data not sent to server.\n");

$result = socket_read ($socket, 1024) or die("Server response error.\n");
echo $result;

socket_close($socket);

?>