<?php
use google\appengine\api\users\User;
use google\appengine\api\users\UserService;
include 'db.php';

$user = UserService::getCurrentUser();
$name = '';
if ($user) {
    $name = $user->getNickname();
}

try {
  if (array_key_exists('content', $_POST)) {
    $result = null;
    if ($_POST['url']) {
        $context = [
        'http' => [
        'method' => 'GET',
        ]
      ];
        $context = stream_context_create($context);
      $result = file_get_contents($_POST['url'], false, $context);
    }
    
    $db = connect();
    $stmt = $db->prepare('INSERT INTO post (author, content, img) VALUES (:name, :content, :img)');
    $stmt->execute(array(':name' => htmlspecialchars($name),
      ':content' => htmlspecialchars($_POST['content']),
      ':img' => $result));
    $affected_rows = $stmt->rowCount();
  }
} catch (PDOException $ex) {
  syslog(LOG_INFO, 'error storing data');// Log error.
}
$db = null;
header('Location: '."/");
?>
