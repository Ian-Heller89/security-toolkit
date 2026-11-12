<#
.SYNOPSIS
    HarnessCore: Automated Windows MITRE ATT&CK Emulation & Validation Harness (VM lab use).

.DESCRIPTION
    Triggers safe, non-destructive emulations of selected ATT&CK techniques, then validates
    that the artifact exists (CIM / filesystem) AND that your logging stack actually recorded it
    (Security 4688, PowerShell 4104, Sysmon 1/11). Results go to purple_validation_report.json.

    Techniques:
      T1059.001  Command and Scripting Interpreter: PowerShell
      T1564.001  Hide Artifacts: Hidden Files and Directories
      T1036.005  Masquerading: Match Legitimate Name or Location

.PARAMETER Technique
    Run a single technique non-interactively.

.PARAMETER All
    Run all techniques non-interactively.

.PARAMETER NoCleanup
    Leave mock artifacts on disk (default behavior is to clean up on exit).

.EXAMPLE
    .\HarnessCore.ps1                       # interactive menu
    .\HarnessCore.ps1 -All                  # run everything, print summary
    .\HarnessCore.ps1 -Technique T1564.001  # run one technique

.NOTES
    Run from an elevated PowerShell in an isolated lab VM only.
    If blocked by execution policy:  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#>

[CmdletBinding()]
param (
    [ValidateSet("T1059.001", "T1564.001", "T1036.005")]
    [string]$Technique,
    [switch]$All,
    [switch]$NoCleanup
)

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
$ScriptRoot = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$script:ReportPath = Join-Path $ScriptRoot "purple_validation_report.json"
$script:HiddenFile = Join-Path $env:TEMP "mock_hidden_attrib.tmp"
$script:SpoofDir   = Join-Path $env:TEMP "shadow_triage"
$script:SpoofFile  = Join-Path $script:SpoofDir "svchost.exe"
$script:Marker     = "HarnessCore"

$Techniques = [ordered]@{
    "1" = @{ Id = "T1059.001"; Name = "PowerShell Script Interpreter" }
    "2" = @{ Id = "T1564.001"; Name = "Hidden Files and Directories" }
    "3" = @{ Id = "T1036.005"; Name = "Masquerading: Match Legitimate Name" }
}

# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
function Test-IsAdmin {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    return ([Security.Principal.WindowsPrincipal]$id).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Show-Banner {
    Clear-Host
    Write-Host ("=" * 80) -ForegroundColor Cyan
    Write-Host "                                  HARNESS CORE" -ForegroundColor Cyan
    Write-Host "          MITRE ATT&CK AUTOMATED PURPLE TEAM HARNESS (WINDOWS)" -ForegroundColor Cyan
    Write-Host ("=" * 80) -ForegroundColor Cyan
    Write-Host ""
}

function Get-UtcStamp { [DateTime]::UtcNow.ToString("yyyy-MM-dd HH:mm:ss") }

function Test-EventTelemetry {
    <# Returns "Logged", "NotLogged", or "LogUnavailable" #>
    param (
        [string]$LogName,
        [int[]]$Ids,
        [string]$Pattern,
        [datetime]$Since
    )
    try {
        $events = Get-WinEvent -FilterHashtable @{ LogName = $LogName; Id = $Ids; StartTime = $Since } -ErrorAction Stop
        $hit = $events | Where-Object { $_.Message -like "*$Pattern*" } | Select-Object -First 1
        if ($hit) { return "Logged" } else { return "NotLogged" }
    } catch {
        if ($_.FullyQualifiedErrorId -like "*NoMatchingEventsFound*") { return "NotLogged" }
        return "LogUnavailable"
    }
}

# ------------------------------------------------------------------------------
# Red: emulation vectors (benign)
# ------------------------------------------------------------------------------
function Invoke-RedVector {
    param ([string]$TechniqueId)

    Write-Host "`n[!] EMULATING OFFENSIVE VECTOR: $TechniqueId" -ForegroundColor Yellow
    $start = Get-Date

    switch ($TechniqueId) {

        "T1059.001" {
            Write-Host "[*] Spawning hidden PowerShell child process (benign sleep)..."
            try {
                $cmd = "Start-Sleep -Seconds 15 # $($script:Marker)-T1059"
                $proc = Start-Process -FilePath "powershell.exe" `
                    -ArgumentList @("-NoProfile", "-NonInteractive", "-Command", $cmd) `
                    -WindowStyle Hidden -PassThru -ErrorAction Stop
                return @{ status = "Executed"; time = Get-UtcStamp; start = $start; pid = $proc.Id
                          msg = "Hidden PowerShell process started (PID $($proc.Id))." }
            } catch {
                return @{ status = "Failed"; time = Get-UtcStamp; start = $start; msg = $_.Exception.Message }
            }
        }

        "T1564.001" {
            Write-Host "[*] Creating file and setting the Hidden attribute..."
            try {
                if (Test-Path $script:HiddenFile) {
                    (Get-Item $script:HiddenFile -Force).Attributes = "Normal"
                    Remove-Item $script:HiddenFile -Force
                }
                "PurpleTeam_Hidden_Trace_Signature" | Out-File $script:HiddenFile -Encoding UTF8 -Force
                (Get-Item $script:HiddenFile -Force).Attributes = "Hidden"
                return @{ status = "Executed"; time = Get-UtcStamp; start = $start; target = $script:HiddenFile
                          msg = "Hidden attribute applied to mock file." }
            } catch {
                return @{ status = "Failed"; time = Get-UtcStamp; start = $start; msg = $_.Exception.Message }
            }
        }

        "T1036.005" {
            Write-Host "[*] Dropping a text file named svchost.exe in a non-system path..."
            try {
                if (-not (Test-Path $script:SpoofDir)) {
                    New-Item -ItemType Directory -Path $script:SpoofDir -Force | Out-Null
                }
                if (Test-Path $script:SpoofFile) { Remove-Item $script:SpoofFile -Force }
                "Simulated_Masquerade_Payload_Block" | Out-File $script:SpoofFile -Encoding UTF8 -Force
                return @{ status = "Executed"; time = Get-UtcStamp; start = $start; target = $script:SpoofFile
                          msg = "Non-executable file masquerading as svchost.exe created outside System32." }
            } catch {
                return @{ status = "Failed"; time = Get-UtcStamp; start = $start; msg = $_.Exception.Message }
            }
        }
    }
    return @{ status = "Skipped"; time = Get-UtcStamp; start = $start; msg = "Unmapped technique." }
}

# ------------------------------------------------------------------------------
# Blue: telemetry validation
# ------------------------------------------------------------------------------
function Get-BlueValidation {
    param (
        [string]$TechniqueId,
        [hashtable]$RedResult
    )

    Write-Host "[*] RUNNING BLUE TEAM validation for: $TechniqueId" -ForegroundColor Green

    if ($RedResult.status -ne "Executed") {
        Write-Host "[-] Skipped: emulation did not execute." -ForegroundColor DarkYellow
        return [ordered]@{ Verdict = "Unknown - Simulation Failed"; Artifact = "N/A"; Events = @{} }
    }

    Start-Sleep -Seconds 3   # let event log writers flush
    $since = ($RedResult.start).AddSeconds(-2)
    $artifact = "Missing"
    $events = [ordered]@{}

    switch ($TechniqueId) {

        "T1059.001" {
            $p = Get-CimInstance Win32_Process -Filter "ProcessId = $($RedResult.pid)" -ErrorAction SilentlyContinue
            if ($p -and $p.CommandLine -like "*$($script:Marker)*") {
                $artifact = "Present"
                Write-Host "[+] CIM: process $($RedResult.pid) visible with marker in command line." -ForegroundColor Green
            } elseif ($p) {
                $artifact = "Present"
                Write-Host "[+] CIM: process $($RedResult.pid) visible (command line not exposed)." -ForegroundColor Green
            } else {
                Write-Host "[!] CIM: process $($RedResult.pid) not found." -ForegroundColor Red
            }
            $events["Security_4688"]       = Test-EventTelemetry "Security" @(4688) $script:Marker $since
            $events["PowerShell_4104"]     = Test-EventTelemetry "Microsoft-Windows-PowerShell/Operational" @(4104) $script:Marker $since
            $events["Sysmon_1"]            = Test-EventTelemetry "Microsoft-Windows-Sysmon/Operational" @(1) $script:Marker $since
        }

        "T1564.001" {
            $item = Get-Item $RedResult.target -Force -ErrorAction SilentlyContinue
            if ($item -and ($item.Attributes -band [IO.FileAttributes]::Hidden)) {
                $artifact = "Present"
                Write-Host "[+] FS: Hidden attribute confirmed on $($RedResult.target)" -ForegroundColor Green
            } else {
                Write-Host "[!] FS: Hidden attribute not found." -ForegroundColor Red
            }
            $events["Sysmon_11_FileCreate"] = Test-EventTelemetry "Microsoft-Windows-Sysmon/Operational" @(11) "mock_hidden_attrib" $since
        }

        "T1036.005" {
            $item = Get-Item $RedResult.target -Force -ErrorAction SilentlyContinue
            if ($item -and $item.Length -gt 0 -and $item.DirectoryName -notlike "$env:SystemRoot\System32*") {
                $artifact = "Present"
                Write-Host "[+] FS: svchost.exe found outside System32 at $($RedResult.target)" -ForegroundColor Green
            } else {
                Write-Host "[!] FS: masquerade file missing or empty." -ForegroundColor Red
            }
            $events["Sysmon_11_FileCreate"] = Test-EventTelemetry "Microsoft-Windows-Sysmon/Operational" @(11) "shadow_triage" $since
        }
    }

    foreach ($k in $events.Keys) {
        $color = switch ($events[$k]) { "Logged" { "Green" } "NotLogged" { "Red" } default { "DarkYellow" } }
        Write-Host ("    {0,-22} {1}" -f $k, $events[$k]) -ForegroundColor $color
    }

    $logged = @($events.Values | Where-Object { $_ -eq "Logged" }).Count
    $verdict =
        if     ($artifact -ne "Present") { "Fail (Emulation Artifact Missing)" }
        elseif ($logged -gt 0)           { "Pass (Telemetry Visible)" }
        else                             { "Partial (Artifact Seen, No Log Telemetry)" }

    return [ordered]@{ Verdict = $verdict; Artifact = $artifact; Events = $events }
}

# ------------------------------------------------------------------------------
# Reporting
# ------------------------------------------------------------------------------
function Save-CycleReport {
    param ($Report)
    try {
        $reports = @()
        if (Test-Path $script:ReportPath) {
            $raw = Get-Content $script:ReportPath -Raw -ErrorAction Stop
            if ($raw.Trim()) { $reports = @($raw | ConvertFrom-Json) }
        }
        $reports += $Report
        ConvertTo-Json -InputObject @($reports) -Depth 6 | Out-File $script:ReportPath -Encoding UTF8 -Force
    } catch {
        Write-Host "[-] Failed to write report: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Show-Summary {
    if (-not (Test-Path $script:ReportPath)) {
        Write-Host "[-] No report found yet. Run a cycle first." -ForegroundColor DarkYellow
        return
    }
    $reports = @(Get-Content $script:ReportPath -Raw | ConvertFrom-Json)
    Write-Host ("`n" + ("=" * 80)) -ForegroundColor Cyan
    Write-Host "                         VALIDATION SUMMARY ($($reports.Count) runs)" -ForegroundColor Cyan
    Write-Host ("=" * 80) -ForegroundColor Cyan
    $reports | ForEach-Object {
        [pscustomobject]@{
            Time      = $_.Timestamp
            Technique = $_.TechniqueID
            Verdict   = $_.BlueValidation.Verdict
        }
    } | Format-Table -AutoSize | Out-String | Write-Host
    Write-Host "Report file: $script:ReportPath"
}

# ------------------------------------------------------------------------------
# Orchestration
# ------------------------------------------------------------------------------
function Invoke-PurpleCycle {
    param ([string]$TechniqueId)

    Write-Host ("=" * 80)
    Write-Host "               PURPLE TEAM VERIFICATION CYCLE: TECHNIQUE $TechniqueId"
    Write-Host ("=" * 80)

    $red  = Invoke-RedVector -TechniqueId $TechniqueId
    Write-Host "    $($red.msg)"
    $blue = Get-BlueValidation -TechniqueId $TechniqueId -RedResult $red

    $redClean = @{}
    foreach ($k in $red.Keys) { if ($k -ne "start") { $redClean[$k] = $red[$k] } }

    Save-CycleReport ([ordered]@{
        TechniqueID    = $TechniqueId
        Timestamp      = Get-UtcStamp
        RedSimulation  = $redClean
        BlueValidation = $blue
    })

    Write-Host ("`n" + ("-" * 80))
    Write-Host "[=] OUTCOME FOR ${TechniqueId}: $($blue.Verdict)" -ForegroundColor Cyan
    Write-Host ("-" * 80)
}

function Remove-MockArtifacts {
    try {
        if (Test-Path $script:HiddenFile) {
            (Get-Item $script:HiddenFile -Force).Attributes = "Normal"
            Remove-Item $script:HiddenFile -Force -ErrorAction SilentlyContinue
        }
        if (Test-Path $script:SpoofDir) { Remove-Item $script:SpoofDir -Recurse -Force -ErrorAction SilentlyContinue }
        Write-Host "[*] Mock artifacts cleaned up."
    } catch {
        Write-Host "[-] Cleanup issue: $($_.Exception.Message)" -ForegroundColor DarkYellow
    }
}

function Show-Menu {
    Show-Banner
    Write-Host "--- Windows Coordinated Purple Team Emulation Selector ---"
    foreach ($k in $Techniques.Keys) {
        Write-Host (" [{0}]   Run cycle: {1} ({2})" -f $k, $Techniques[$k].Id, $Techniques[$k].Name)
    }
    Write-Host " [4]   Run ALL cycles"
    Write-Host " [5]   Show summary report"
    Write-Host " [999] Exit and clean up"
    Write-Host ("-" * 80)
}

function Start-Menu {
    while ($true) {
        Show-Menu
        $choice = (Read-Host "`n[?] Select option").Trim()

        if ($choice -eq "999") {
            Write-Host "[*] Shutting down HarnessCore."
            if (-not $NoCleanup) { Remove-MockArtifacts }
            break
        }

        if ($Techniques.Contains($choice)) {
            Invoke-PurpleCycle -TechniqueId $Techniques[$choice].Id
        } elseif ($choice -eq "4") {
            foreach ($k in $Techniques.Keys) { Invoke-PurpleCycle -TechniqueId $Techniques[$k].Id }
        } elseif ($choice -eq "5") {
            Show-Summary
        } else {
            Write-Host "[-] Choice not recognized." -ForegroundColor DarkYellow
            Start-Sleep -Seconds 1
            continue
        }
        Read-Host "`n[*] Press Enter to return to menu" | Out-Null
    }
}

# ------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------
if (-not (Test-IsAdmin)) {
    Write-Host "[!] Not running as Administrator. Security log (4688) checks will report LogUnavailable." -ForegroundColor DarkYellow
}

if ($All) {
    foreach ($k in $Techniques.Keys) { Invoke-PurpleCycle -TechniqueId $Techniques[$k].Id }
    Show-Summary
    if (-not $NoCleanup) { Remove-MockArtifacts }
} elseif ($Technique) {
    Invoke-PurpleCycle -TechniqueId $Technique
    if (-not $NoCleanup) { Remove-MockArtifacts }
} else {
    Start-Menu
}
