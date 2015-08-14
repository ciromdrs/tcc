<?php
include 'db.php';

$id = intval($_GET['id']);

// Busca na cache
$memcache = new Memcache;
$img = $memcache->get($id);

if ($img === false) {
    $db = connect();

    $row = null;
    try {
      $query = $db->prepare('SELECT img FROM post WHERE id = ' . $id);
      $query->execute();
      $img = $query->fetch(1)['img'];
      $memcache->set($id, $img); // Adding image to cache
    } catch (PDOException $ex) {
      // Log error.
    }

    $db = null;
}

header("Content-Type: image/png"); 
echo $img;

?>

