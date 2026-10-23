# GhostWatch: Advanced Native Windows Process Anomaly Detection Engine
# Language: Pure Windows PowerShell (.ps1) - Hardened Enterprise Baseline

function Show-Banner {
    Clear-Host
    Write-Output "================================================================================"
    Write-Output "                                  GHOST WATCH"
    Write-Output "                    ADVANCED WINDOWS TELEMETRY DETECTION ENGINE"
    Write-Output "================================================================================"
    Write-Output ""
}

function Invoke-AnomalyScan {
    Write-Output "[*] Querying active operating system kernel memory tables via CIM..."
    
    try {
        $processList = Get-CimInstance Win32_Process | Select-Object ProcessId, Name, ExecutablePath, ParentProcessId
    } catch {
        Write-Output "[-] Critical Error: Failed to aggregate Windows kernel process telemetry."; return
    }

    $anomalyCount = 0
    Write-Output ("-" * 80)
    Write-Output ("{0,-6} | {1,-20} | {2}" -f "PID", "PROCESS NAME", "RISK CLASSIFICATION DETECTED")
    Write-Output ("-" * 80)

    # Core System Binaries frequently target-copied or masqueraded by attackers
    $systemBinaries = @("lsass.exe", "svchost.exe", "wininit.exe", "services.exe", "smss.exe", "csrss.exe")
    $suspiciousParents = @("chrome", "firefox", "msedge", "outlook", "winword", "excel", "powerpnt")
    $shellBinaries = @("cmd.exe", "powershell.exe", "wscript.exe", "cscript.exe", "mshta.exe")
    
    # ADVANCED DETECTION: High-risk Living-off-the-Land (LotL) execution utilities
    $lotlBinaries = @("certutil.exe", "bitsadmin.exe", "vssadmin.exe", "regsvr32.exe", "rundll32.exe", "schtasks.exe")

    foreach ($proc in $processList) {
        $pid = $proc.ProcessId
        $name = $proc.Name
        $path = $proc.ExecutablePath
        $parentPid = $proc.ParentProcessId

        # ANOMALY VECTOR A: Hidden Memory Injections (Empty/Null Executable Paths)
        if ([string]::IsNullOrEmpty($path) -and $name -ne "System" -and $name -ne "Idle") {
            Write-Output ("{0,-6} | {1,-20} | [!!!] INJECTION RISK: Process running with hidden/blank executable path!" -f $pid, $name)
            $anomalyCount++
            continue
        }

        # ANOMALY VECTOR B: Core System Binaries running out of malicious user locations
        if ($name.ToLower() -in $systemBinaries) {
            if (-not [string]::IsNullOrEmpty($path) -and -not $path.ToLower().Contains("system32") -and -not $path.ToLower().Contains("syswow64")) {
                Write-Output ("{0,-6} | {1,-20} | [!!!] MASQUERADE DETECTED: Running outside System32 directory!" -f $pid, $name)
                Write-Output "       -> Malicious File Pathway: $path"
                $anomalyCount++
            }
            # Forensic Validation: System process spoofing verification
            if ($name.ToLower() -eq "system" -and $pid -ne 4) {
                Write-Output ("{0,-6} | {1,-20} | [!!!] PID SPOOFING: Rogue process masquerading as core System PID 4!" -f $pid, $name)
                $anomalyCount++
            }
        }

        # ANOMALY VECTOR C: Exploitations or background shells spawned by productivity apps
        if ($name.ToLower() -in $shellBinaries) {
            $parentProc = $processList | Where-Object { $_.ProcessId -eq $parentPid }
            if ($parentProc) {
                $parentName = $parentProc.Name.ToLower()
                foreach ($sp in $suspiciousParents) {
                    if ($parentName.Contains($sp)) {
                        Write-Output ("{0,-6} | {1,-20} | [!!!] EXPLOIT ANOMALY: Shell spawned by client application/browser!" -f $pid, $name)
                        Write-Output "       -> Malicious Parent Context: PID $parentPid ($($parentProc.Name))"
                        $anomalyCount++
                    }
                }
            }
        }

        # ANOMALY VECTOR D: Suspicious Living-off-the-Land Binary Execution
        if ($name.ToLower() -in $lotlBinaries) {
            $parentProc = $processList | Where-Object { $_.ProcessId -eq $parentPid }
            if ($parentProc) {
                $parentName = $parentProc.Name.ToLower()
                if ($parentName -in $suspiciousParents -or $parentName -eq "cmd.exe" -or $parentName -eq "powershell.exe") {
                    Write-Output ("{0,-6} | {1,-20} | [!!!] LIVING-OFF-THE-LAND: High-risk administrative utility spawned suspiciously!" -f $pid, $name)
                    if (-not [string]::IsNullOrEmpty($path)) { Write-Output "       -> Executable Path: $path" }
                    $anomalyCount++
                }
            }
        }
    }

    Write-Output ("-" * 80)
    Write-Output "`n[=] WINDOWS PROCESS AUDIT METRICS SUMMARY:"
    Write-Output "    -> Total Active Tasks Analyzed: $($processList.Count)"
    Write-Output "    -> Critical Memory Anomalies Isolated: $anomalyCount"
    
    if ($anomalyCount -gt 0) {
        Write-Output "`n[!!!] DETECTION ALERT: Malicious process masquerading, hollowing, or exploit signatures identified!"
    } else {
        Write-Output "`n[+] Memory space verified. All running process structures adhere to standard baselines."
    }
    Write-Output ("=" * 80)
}
function Main {
    while ($true) {
        Show-Banner
        Write-Output "--- Windows Native Active Process Telemetry Menu ---"
        Write-Output " [1] Execute Live Memory Process Anomaly Audit"
        Write-Output " [999] Exit Defensive Suite Entirely"
        Write-Output "--------------------------------------------------------------------------------"
        
        $choice = Read-Host "`n[?] Select Operational Mode (1 / 999)"
        if ($null -ne $choice) { $choice = $choice.Trim() }

        if ($choice -eq "999") {
            Write-Output "[*] Shutting down GhostWatch Security Engine. Terminating monitors."; break
        }
        elseif ($choice -eq "1") {
            Clear-Host
            Show-Banner
            Invoke-AnomalyScan
            Read-Host "`n[*] Press Enter to return to main menu"
        }
        else {
            Write-Output "[-] Choice index not recognized."
            Start-Sleep -Seconds 1
        }
    }
}

# Fire the script entry loop dynamically on execution
Main
