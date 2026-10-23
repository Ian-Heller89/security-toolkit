# DeepTrace: Windows Native Incident Response Forensic Triage Harvester
# Language: Pure Windows PowerShell (.ps1) - Hardened Enterprise Baseline

function Show-Banner {
    Clear-Host
    Write-Output "================================================================================"
    Write-Output "                                  DEEP TRACE"
    Write-Output "                    ENTERPRISE INCIDENT RESPONSE HARVESTER"
    Write-Output "================================================================================"
    Write-Output ""
}

function Invoke-ForensicTriage {
    # Generate an explicit, timestamped forensic triage directory to house the dumps safely
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $triageDir = "C:\Users\Public\DeepTrace_Triage_$timestamp"
    
    try {
        New-Item -ItemType Directory -Path $triageDir -Force | Out-Null
        Write-Output "[*] Created centralized forensic collection matrix directory:"
        Write-Output "    -> $triageDir`n"
    } catch {
        Write-Output "[-] Critical Error: Failed to allocate triage dump directories."; return
    }

    # Initialize HTML report container data placeholders
    $netRows = ""
    $historyRows = ""
    $dnsRows = ""
    $userRows = ""

    # --- FORENSIC VECTOR 1: ACTIVE NETWORK SOCKETS ---
    Write-Output "[*] Harvesting volatile network socket and established port mappings..."
    try {
        $connections = Get-NetTCPConnection -ErrorAction SilentlyContinue
        foreach ($conn in $connections) {
            $netRows += "<tr><td>$($conn.LocalAddress)</td><td>$($conn.LocalPort)</td><td>$($conn.RemoteAddress)</td><td>$($conn.RemotePort)</td><td>$($conn.State)</td><td>$($conn.OwningProcess)</td></tr>"
        }
        Write-Output "    [+] Volatile network sockets successfully parsed into forensic matrix."
    } catch {
        Write-Output "    [-] Failed to aggregate network sockets."
    }

    # --- FORENSIC VECTOR 2: POWERSHELL TERMINAL HISTORY LOGS ---
    Write-Output "[*] Locating and carving plain-text PowerShell console execution history..."
    $historyPath = "$env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt"
    if (Test-Path $historyPath) {
        try {
            $historyLines = Get-Content -Path $historyPath -ErrorAction SilentlyContinue
            $lineNum = 1
            foreach ($line in $historyLines) {
                if (-not [string]::IsNullOrWhiteSpace($line)) {
                    # Escape HTML characters to protect the integrity of the dashboard report logs
                    $safeLine = [System.Web.HttpUtility]::HtmlEncode($line)
                    $historyRows += "<tr><td>$lineNum</td><td>$safeLine</td></tr>"
                    $lineNum++
                }
            }
            Write-Output "    [+] Plain-text console history file carved successfully."
        } catch {
            Write-Output "    [-] Failed to parse console history file."
        }
    } else {
        $historyRows = "<tr><td colspan='2' style='text-align:center; color:orange;'>No legacy PSReadLine terminal history file footprint discovered on this user profile.</td></tr>"
        Write-Output "    [-] Operational notice: Console history log file not present."
    }
    # --- FORENSIC VECTOR 3: MEMORY-RESIDENT DNS CLIENT CACHE ---
    Write-Output "[*] Harvesting memory-resident DNS client lookup cache..."
    try {
        $dnsCache = Get-DnsClientCache -ErrorAction SilentlyContinue
        if ($dnsCache) {
            foreach ($entry in $dnsCache) {
                if (-not [string]::IsNullOrWhiteSpace($entry.Name)) {
                    $dnsRows += "<tr><td>$($entry.Name)</td><td>$($entry.Type)</td><td>$($entry.Status)</td><td>$($entry.Data)</td></tr>"
                }
            }
            Write-Output "    [+] DNS lookup database cache successfully compiled."
        } else {
            $dnsRows = "<tr><td colspan='4' style='text-align:center;'>DNS client cache is currently empty.</td></tr>"
        }
    } catch {
        Write-Output "    [-] Failed to aggregate DNS client cache tables."
    }

    # --- FORENSIC VECTOR 4: CURRENT ACTIVE USER SESSIONS ---
    Write-Output "[*] Identifying logged-in profile tokens and active concurrent user sessions..."
    try {
        # Parsing native query user data structures safely
        $users = query user 2>$null
        if ($users) {
            foreach ($user in $users) {
                if (-not [string]::IsNullOrWhiteSpace($user)) {
                    # Standardize whitespace spacing format to keep columns human-readable
                    $cleanUser = $user -replace '\s+', ' '
                    $userRows += "<tr><td>$cleanUser</td></tr>"
                }
            }
            Write-Output "    [+] Active administrative connection parameters recorded."
        } else {
            $userRows = "<tr><td>Local query user session table returned empty or unavailable.</td></tr>"
        }
    } catch {
        Write-Output "    [-] Failed to gather active user sessions."
    }

    # --- AUTOMATED FORENSIC HTML REPORT GENERATION ---
    Write-Output "[*] Reconstituting raw forensics and compiling HTML Investigator Dashboard..."
    $htmlReportPath = Join-Path $triageDir "Triage_Report.html"

    $htmlContent = @"
<!DOCTYPE html>
<html>
<head>
    <title>DeepTrace Forensic Triage Report</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 30px; background-color: #f4f6f9; color: #333; }
        h1 { color: #1e3a8a; border-bottom: 3px solid #1e3a8a; padding-bottom: 10px; margin-bottom: 25px; }
        h2 { color: #2563eb; margin-top: 35px; border-bottom: 2px solid #e5e7eb; padding-bottom: 5px; }
        .banner { background-color: #1e3a8a; color: white; padding: 15px; font-weight: bold; border-radius: 5px; margin-bottom: 25px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-radius: 4px; overflow: hidden; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb; font-size: 14px; }
        th { background-color: #f8fafc; font-weight: 600; color: #475569; }
        tr:hover { background-color: #f8fafc; }
        .console-log { background-color: #0f172a; color: #38bdf8; font-family: 'Courier New', Courier, monospace; }
        .console-log th { background-color: #1e293b; color: #94a3b8; }
        .console-log tr:hover { background-color: #1e293b; }
    </style>
</head>
<body>
    <div class="banner">⚡ DEEPTRACE AUTOMATED INCIDENT RESPONSE HOST EXTRACTION SUMMARY</div>
    <h1>Forensic Triage Examination Report</h1>
    <p><strong>Execution Host Base Timestamp:</strong> $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")</p>
    <p><strong>Target Acquisition Folder Destination:</strong> $triageDir</p>

    <h2>1. Volatile Network Socket & Port Alignment Metrics</h2>
    <table>
        <thead>
            <tr><th>Local Address</th><th>Local Port</th><th>Remote Address</th><th>Remote Port</th><th>Socket State</th><th>Owning Process ID</th></tr>
        </thead>
        <tbody>
            $netRows
        </tbody>
    </table>

    <h2>2. Carved PowerShell Terminal Execution Log History</h2>
    <table class="console-log">
        <thead>
            <tr><th style="width: 80px;">Line</th><th>Executed Shell Command History String Log</th></tr>
        </thead>
        <tbody>
            $historyRows
        </tbody>
    </table>

    <h2>3. Memory-Resident System DNS Client Cache Records</h2>
    <table>
        <thead>
            <tr><th>Queried Web Domain Name Record</th><th>Record Type</th><th>Response Status</th><th>Resolved Endpoint Address Data</th></tr>
        </thead>
        <tbody>
            $dnsRows
        </tbody>
    </table>

    <h2>4. Logged-In User Sessions & Access Token Mapping</h2>
    <table>
        <thead>
            <tr><th>Raw Local Active Session Telemetry Data Record</th></tr>
        </thead>
        <tbody>
            $userRows
        </tbody>
    </table>
</body>
</html>
"@

    try {
        $htmlContent | Out-File $htmlReportPath -Encoding UTF8 -Force
        Write-Output "`n================================================================================"
        Write-Output "[+] SUCCESS: Fully automated forensic data collection completed!"
        Write-Output "[+] CENTRALIZED HARVEST DIRECTORY: $triageDir"
        Write-Output "[+] INTERACTIVE HTML DASHBOARD REPORT: $htmlReportPath"
        Write-Output "================================================================================"
    } catch {
        Write-Output "[-] Error compiling the interactive HTML forensic dashboard: $_"
    }
}

function Main {
    while ($true) {
        Show-Banner
        Write-Output "--- Windows Native Forensic Incident Response Menu ---"
        Write-Output " [1] Execute Live System Triage & Artifact Collection"
        Write-Output " [999] Exit Defensive Suite Entirely"
        Write-Output "--------------------------------------------------------------------------------"
        
        $choice = Read-Host "`n[?] Select Operational Mode (1 / 999)"
        if ($null -ne $choice) { $choice = $choice.Trim() }

        if ($choice -eq "999") {
            Write-Output "[*] Shutting down DeepTrace Harvester Module. Exiting."; break
        }
        elseif ($choice -eq "1") {
            Clear-Host
            Show-Banner
            Invoke-ForensicTriage
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
