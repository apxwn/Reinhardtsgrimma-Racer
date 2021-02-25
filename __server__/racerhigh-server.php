<?php 
// Racerhigh Dataserver
// Aufruf mit URL-Parametern "name=" und "score=" , z.B.:
// https://chartophylakeion.de/racerhigh-server.php?name=Rolf&score=3333

ini_set('error_log', __DIR__ . '/racerhigh-php_errors.log');

// initialisiere Loggingsystem
include('./logsys.php');
$log = new Logging();
$log->lfile('./racerhigh.log');
$log->lwrite('---- racerhigh.php wurde aufgerufen ----');

// Name und Pfad der JSON-Datei:
$filename = 'racerhigh.json';
$filepath = __DIR__ . "/";

// hole URL-Parameter "name" und "score":
$name = false;
if (isset($_GET['name'])) {
    $name = $_GET['name'];
}

$score = false;
if (isset($_GET['score'])) {
    $score = $_GET['score'];
}

// prüfe, ob "name" und "score" vorhanden sind:
if ((!$name) || (!$score)) {
	$log->lwrite('Name und/oder Score wurden nicht per URLparam übergeben. URLparam war: ' . json_encode($_GET));
	die();
}

// (für alle Fälle) score zu int umwandeln:
$score = intval($score);

// Array des Highscore-Eintrags:
$entry = [$name, $score];
	$log->lwrite('Habe bekommen: ' . $name . ' mit ' . $score . 'Punkten.');

// hole gespeicherte Highscore-Liste aus Datei:
$str = file_get_contents($filepath . $filename);
$highscore = json_decode($str, true);

// Füge den aktuellen Namen mit Score ans Ende des Highscore-Arrays:
array_push($highscore, $entry);

// Sortiere den Array nach Score descending:
usort($highscore, function($a, $b) {
    return $b[1] <=> $a[1]; // erst b, dann a, dadurch reverse order
});

// reduziere auf die 10 ersten Einträge:
$highscore = array_slice($highscore, 0, 10);

// schreibe JSON:
file_put_contents($filepath . $filename, json_encode($highscore));
?>