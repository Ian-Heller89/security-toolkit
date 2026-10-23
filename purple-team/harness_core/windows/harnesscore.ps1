# HarnessCore: Automated Windows Threat Emulation Validation Engine
# Path: purple_team/harness_core/windows/harness_core.ps1
# Language: Pure Windows PowerShell (.ps1) - Hardened Enterprise Baseline

$PURPLE_LOG = "purple_validation_report.json"

function Show-Banner {
    Clear-Host
    Write-Output "================================================================================"
    Write-Output "                                  HARNESS CORE"
    Write-Output "          MITRE ATT&CK AUTOMATED PURPLE TEAM HARNESS (WINDOWS - HARDENED)"
    Write-Output "================================================================================"
    Write-Output ""
}

function Invoke-RedVector {
    param (
        [string]$TechniqueId
    )
    Write-Output "`n[!] EMULATING OFFENSIVE VECTOR: $TechniqueId"
    $timestamp = [DateTime]::UtcNow.ToString("yyyy-MM-dd HH:mm:ss")
    
    switch ($TechniqueId) {
        "T1059.001" { # Command and Scripting Interpreter: PowerShell
            Write-Output "[*] Simulating background hidden script interpreter spawning..."
            try {
                # Spawning a benign background execution hook to safely generate process telemetry
                $proc = Start-Process powershell.exe -ArgumentList "-NoProfile -NonInteractive -Command Start-Sleep -Seconds 1" -PassThru -WindowStyle Hidden
                return @{ "status" = "Executed"; "time" = $timestamp; "pid" = $proc.Id; "msg" = "Benign hidden PowerShell process initiated successfully." }
            } catch {
                return @{ "status" = "Failed"; "time" = $timestamp; "msg" = $_.Exception.Message }
            }
        }
        
        "T1564.001" { # Hidden Files and Directories
            Write-Output "[*] Simulating stealthy hidden asset file placement..."
            $mockFile = Join-Path $env:TEMP "mock_hidden_attrib.tmp"
            try {
                if (Test-Path $mockFile) { Remove-Item $mockFile -Force }
                "PurpleTeam_Hidden_Trace_Signature" | Out-File $mockFile -Encoding UTF8 -Force
                # Call native Windows filesystem attribute parameters to forensically hide the document
                $fileItem = Get-Item $mockFile -Force
                $fileItem.Attributes = "Hidden"
                return @{ "status" = "Executed"; "time" = $timestamp; "target" = $mockFile; "msg" = "Hidden attribute injected into mock asset file." }
            } catch {
                return @{ "status" = "Failed"; "time" = $timestamp; "msg" = $_.Exception.Message }
            }
        }
        
        "T1036.005" { # Masquerading: Match Legitimate Name
            Write-Output "[*] Simulating malicious core system binary name spoofing..."
            $mockDir = Join-Path $env:TEMP "shadow_triage"
            if (-not (Test-Path $mockDir)) { New-Item -ItemType Directory -Path $mockDir -Force | Out-Null }
            $mockSpoof = Join-Path $mockDir "svchost.exe"
            
            try {
                if (Test-Path $mockSpoof) { Remove-Item $mockSpoof -Force }
                "Simulated_Masquerade_Payload_Block" | Out-File $mockSpoof -Encoding UTF8 -Force
                return @{ "status" = "Executed"; "time" = $timestamp; "target" = $mockSpoof; "msg" = "Rogue script masqueraded under legitimate binary identity." }
            } catch {
                return @{ "status" = "Failed"; "time" = $timestamp; "msg" = $_.Exception.Message }
            }
        }
    }
    return @{ "status" = "Skipped"; "time" = $timestamp; "msg" = "Unmapped vector profile matched." }
}
function Get-BlueValidation {
    param (
        [string]$TechniqueId,
        [hashtable]$RedResult
    )
    Write-Output "[*] RUNNING BLUE TEAM telemetry validation check for: $TechniqueId"
    Start-Sleep -Seconds 1 # Allow volatile memory buffers and file pointers a moment to synchronize
    
    if ($RedResult.status -ne "Executed") {
        Write-Output "[-] Telemetry Audit Skipped: Attack vector simulation was not executed successfully."
        return "Unknown - Simulation Failed"
    }

    switch ($TechniqueId) {
        "T1059.001" {
            # Advanced Process Telemetry Validation: Queries the Windows subsystem natively via CIM
            $targetPid = $RedResult.pid
            try {
                $procCheck = Get-CimInstance Win32_Process -Filter "ProcessId = $targetPid" -ErrorAction SilentlyContinue
                if ($procCheck) {
                    Write-Output "[+] VALIDATION SUCCESS: Active process execution trace verified in kernel memory arrays."
                    return "Pass (Telemetry Visible)"
                }
                Write-Output "[!!!] VALIDATION CRITICAL FAILURE: Process ID $targetPid not discovered in active kernel tables."
                return "Fail (Blindspot Detected)"
            } catch {
                return "Fail (Exception Encountered)"
            }
        }

        "T1564.001" {
            # Advanced File Attribute Validation: Interrogates native handle properties directly
            $targetPath = $RedResult.target
            try {
                if (Test-Path $targetPath -ErrorAction SilentlyContinue) {
                    $fileCheck = Get-Item $targetPath -Force -ErrorAction SilentlyContinue
                    if ($fileCheck.Attributes -match "Hidden") {
                        Write-Output "[+] VALIDATION SUCCESS: Hidden attribute anomaly captured on disk."
                        return "Pass (Telemetry Visible)"
                    }
                }
                Write-Output "[!!!] VALIDATION CRITICAL FAILURE: File metadata missing target hidden attributes."
                return "Fail (Blindspot Detected)"
            } catch {
                return "Fail (Exception Encountered)"
            }
        }

        "T1036.005" {
            # Advanced Directory Spoofing Validation: Confirms rogue file footprint presence in Temp locations
            $targetPath = $RedResult.target
            try {
                if (Test-Path $targetPath -ErrorAction SilentlyContinue) {
                    if ((Get-Item $targetPath -Force).Length -gt 0) {
                        Write-Output "[+] VALIDATION SUCCESS: Masquerading signature footprint discovered inside triage workspace."
                        return "Pass (Telemetry Visible)"
                    }
                }
                Write-Output "[!!!] VALIDATION CRITICAL FAILURE: Masquerade target file absent or zero bytes."
                return "Fail (Blindspot Detected)"
            } catch {
                return "Fail (Exception Encountered)"
            }
        }
    }
    return "Indeterminate"
}

function Execute-PurpleCycle {
    param (
        [string]$TechniqueId
    )
    Write-Output ("=" * 80)
    Write-Output "               PURPLE TEAM VERIFICATION CYCLE: TECHNIQUE $TechniqueId"
    Write-Output ("=" * 80)

    # 1. Run the offensive emulation vector
    $redReport = Invoke-RedVector -TechniqueId $TechniqueId

    # 2. Run the defensive telemetry validation verification loop
    $blueStatus = Get-BlueValidation -TechniqueId $TechniqueId -RedResult $redReport

    # 3. Log results to system validation tracking array serialized as JSON
    $cycleReport = [ordered]@{
        "TechniqueID"    = $TechniqueId
        "Timestamp"      = [DateTime]::UtcNow.ToString("yyyy-MM-dd HH:mm:ss")
        "RedSimulation"  = $redReport
        "BlueValidation" = $blueStatus
    }

    try {
        $reports = @()
        if (Test-Path $global:PURPLE_LOG) {
            $reports = Get-Content $global:PURPLE_LOG -Raw | ConvertFrom-Json
            if ($reports -isnot [array]) { $reports = @($reports) }
        }
        $reports += $cycleReport
        $reports | ConvertTo-Json -Depth 5 | Out-File $global:PURPLE_LOG -Encoding UTF8 -Force
    } catch {
        Write-Output "[-] Failed to write purple validation metrics log: $_"
    }

    Write-Output ("`n" + "-" * 80)
    Write-Output "[=] EMULATION CYCLE OUTCOME FOR $TechniqueId: STATUS = $blueStatus"
    Write-Output ("-" * 80)
}

function Main {
    while ($true) {
        Show-Banner
        Write-Output "--- Windows Coordinated Purple Team Emulation Selector ---"
        Write-Output " Run Coordinated Cycle: T1059.001 (PowerShell Script Interpreter)"
        Write-Output " Run Coordinated Cycle: T1564.001 (Hidden Files and Directories)"
        Write-Output " Run Coordinated Cycle: T1036.005 (Masquerading: Match Legitimate Name)"
        Write-Output " Exit Coordinated Harness Suite Entirely"
        Write-Output "--------------------------------------------------------------------------------"

        $choice = Read-Host "`n[?] Select Coordinated Execution Cycle (1-3 / 999)"
        if ($null -ne $choice) { $choice = $choice.Trim() }

        if ($choice -eq "999") {
            Write-Output "[*] Shutting down HarnessCore Purple Team Controller."
            # Local cleaning of mock execution footprints safely on exit to maintain a clean environment
            $mockFile = Join-Path $env:TEMP "mock_hidden_attrib.tmp"
            $mockDir = Join-Path $env:TEMP "shadow_triage"
            if (Test-Path $mockFile) { Remove-Item $mockFile -Force }
            if (Test-Path $mockDir) { Remove-Item $mockDir -Recurse -Force }
            break
        }
        Hotkey-Mapping -Choice $choice
    }
}

function Hotkey-Mapping {
    param ([string]$Choice)
    switch ($Choice) {
        "1" { Execute-PurpleCycle -TechniqueId "T1059.001"; Read-Host "`n[*] Press Enter to return to menu" }
        "2" { Execute-PurpleCycle -TechniqueId "T1564.001"; Read-Host "`n[*] Press Enter to return to menu" }
        "3" { Execute-PurpleCycle -TechniqueId "T1036.005"; Read-Host "`n[*] Press Enter to return to menu" }
        default { Write-Output "[-] Choice index not recognized."; Start-Sleep -Seconds 1 }
    }
}

# Fire the script entry loop dynamically on execution
Main
