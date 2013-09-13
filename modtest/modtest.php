#!/usr/bin/php
<?
$sample_rate = 10;
$total_tries = $argv[1];
$matches = array();
$nonmatches = array();
echo "$total_tries \n";
foreach (range(1, $total_tries) as $number) {

    $random_number = rand();

    if ($random_number % $sample_rate === 0) {
        $matches[] = $random_number;
        // if this were a real page you would submit your stat here
        // since it matches your sample rate
    }
    else {
        $nonmatches[] = $random_number;
    }
}

$matchcount = count($matches);
$nonmatchcount = count($nonmatches);
print "matches: $matchcount\n";
print "nonmatches: $nonmatchcount\n";
$dive = $matchcount * 100;
$prc = $dive / $total_tries;
echo "$prc" . "\n"
?>
