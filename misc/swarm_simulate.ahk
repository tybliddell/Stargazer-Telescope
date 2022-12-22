^k::
	SendRaw $DT OK*34
	Send ^j
	Sleep 50
	SendRaw $GN OK*2d
	Send ^j
	Sleep 50
	SendRaw $RT OK*22
	Send ^j
	Sleep 50
	FormatTime, output_time,,yyyyMMddhhmmss
	Send $DT{space}%output_time%,V*44
	Send ^j
	Sleep 50
	SendRaw $GN 40.8921,-111.0155,1449,89,2*01
	Send ^j
	Sleep 50

^l::
	FormatTime, output_time,,yyyyMMddhhmmss
	Send $DT{space}%output_time%,V*44
	Send ^j
	Sleep 50
	SendRaw $GN 40.8921,-111.0155,77,89,2*01
	Send ^j
	Sleep 50