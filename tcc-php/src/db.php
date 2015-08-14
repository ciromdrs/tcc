<?php

function connect()
{
    if (isset($_SERVER['SERVER_SOFTWARE']) &&
    strpos($_SERVER['SERVER_SOFTWARE'],'Google App Engine') !== false) {
        // Connect from App Engine.
        try{
            $db = new pdo('mysql:unix_socket=/cloudsql/tcc-ciro:tcc-inst;dbname=tcc_db', 'root', '');
        }catch(PDOException $ex){
            die(json_encode(
                array('outcome' => false, 'message' => 'Unable to connect.')
                )
            );
        }
    } else {
        // Connect from a development environment.
        try{
            $db = new pdo('mysql:host=127.0.0.1:3306;dbname=tcc_db', 'root', 'root');
        }catch(PDOException $ex){
            die(json_encode(
                array('outcome' => false, 'message' => 'Unable to connect')
                )
            );
        }
    }
    return $db;
}
?>
