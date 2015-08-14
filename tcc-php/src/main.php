<?php
use google\appengine\api\users\User;
use google\appengine\api\users\UserService;
include 'db.php';

$user = UserService::getCurrentUser();

if (!$user) {
  header('Location: ' . UserService::createLoginURL($_SERVER['REQUEST_URI']));
}
?>

<html>
 <head>
	 <link rel="stylesheet" href="static/main.css"
 </head>
 <body>
  <?php
  if ($user) {
    echo 'Hello, ' . htmlspecialchars($user->getNickname()) . '. ';
    echo 'You can <a href=' . UserService::createLogoutURL($_SERVER['REQUEST_URI']) . '>logout</a>';
  } else {
    echo 'Hello';
  }

  // Create a connection.
  $db = connect();
  try {
    // Show existing entries.
    foreach($db->query('SELECT * from post ORDER BY id DESC LIMIT 10') as $row) {
		echo "<div><strong>" . $row['author'] . "</strong> wrote <br> " .
		$row['content'];
		if ($row['img']) {
			echo "<br><img src=/img?id=" . $row['id'] . ">";
		}
		echo "</div><br>";
     }
  } catch (PDOException $ex) {
    echo "An error occurred.";
  }
  $db = null;
  ?>

  <form action="/sign" method="post">
    <div><textarea name="content" rows="3" cols="60"></textarea></div>
    <div><input name="url" type="text" placeholder="Paste a link to an image..."></div>
    <div><input type="submit"></div>
  </form>
  </body>
</html>
