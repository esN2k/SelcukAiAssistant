param(
  [string]$BaseUrl = "http://localhost:8000",
  [int]$TimeoutSec = 60,
  [string]$ReportPath
)

$ErrorActionPreference = "Stop"
$script:failures = 0
$script:results = @()
$curl = (Get-Command curl.exe -ErrorAction Stop).Source

$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding  = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

if ([string]::IsNullOrWhiteSpace($ReportPath)) {
  $ReportPath = Join-Path $PSScriptRoot ".tmp\smoke_report.md"
}

function Write-Result {
  param(
    [string]$Name,
    [bool]$Ok,
    [string]$Detail = ""
  )
  $status = if ($Ok) { "PASS" } else { "FAIL" }
  if (-not $Ok) { $script:failures++ }

  $script:results += [PSCustomObject]@{
    Name   = $Name
    Status = $status
    Detail = $Detail
  }

  if ($Ok) {
    Write-Host "PASS: $Name"
  } else {
    Write-Host "FAIL: $Name - $Detail"
  }
}

function Truncate-Text {
  param(
    [string]$Text,
    [int]$MaxLength = 500
  )
  if ($null -eq $Text) { return "" }
  if ($Text.Length -le $MaxLength) { return $Text }
  return $Text.Substring(0, $MaxLength) + "..."
}

function Write-Utf8NoBom {
  param(
    [string]$Path,
    [string]$Content
  )
  $utf8 = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $Content, $utf8)
}

function Quote-Arg {
  param([string]$Arg)
  if ($Arg -match '[\s"]') {
    return '"' + ($Arg -replace '"','\"') + '"'
  }
  return $Arg
}

function Invoke-Curl {
  param(
    [string[]]$CurlArgs
  )

  $argsString = ($CurlArgs | ForEach-Object { Quote-Arg $_ }) -join ' '
  $prev = $ErrorActionPreference
  $ErrorActionPreference = "Continue"

  try {
    $pinfo = New-Object System.Diagnostics.ProcessStartInfo
    $pinfo.FileName = $curl
    $pinfo.Arguments = $argsString
    $pinfo.UseShellExecute = $false
    $pinfo.RedirectStandardOutput = $true
    $pinfo.RedirectStandardError = $true

    $utf8 = [System.Text.UTF8Encoding]::new($false)
    $pinfo.StandardOutputEncoding = $utf8
    $pinfo.StandardErrorEncoding  = $utf8

    $p = New-Object System.Diagnostics.Process
    $p.StartInfo = $pinfo

    [void]$p.Start()
    $stdout = $p.StandardOutput.ReadToEnd()
    $stderr = $p.StandardError.ReadToEnd()
    $p.WaitForExit()

    $combined = $stdout
    if (-not [string]::IsNullOrWhiteSpace($stderr)) {
      if (-not [string]::IsNullOrWhiteSpace($combined)) { $combined += "`n" }
      $combined += $stderr
    }

    return [PSCustomObject]@{
      Output   = $combined
      ExitCode = $p.ExitCode
    }
  }
  finally {
    $ErrorActionPreference = $prev
  }
}

function Invoke-CurlWithRetry {
  param(
    [string[]]$CurlArgs,
    [int]$RetryCount = 1,
    [int]$RetryDelaySec = 2
  )
  $result = Invoke-Curl -CurlArgs $CurlArgs
  if ($RetryCount -le 0) { return $result }
  if ($result.Output -match 'Operation timed out') {
    Start-Sleep -Seconds $RetryDelaySec
    return Invoke-Curl -CurlArgs $CurlArgs
  }
  return $result
}

function Require-Model {
  param(
    [object[]]$Models,
    [string]$Provider,
    [string[]]$PreferredIds = @()
  )
  $available = $Models | Where-Object {
    $_.provider -eq $Provider -and $_.available -eq $true
  }
  foreach ($pref in $PreferredIds) {
    $match = $available | Where-Object { $_.id -eq $pref } | Select-Object -First 1
    if ($match) { return $match }
  }
  return $available | Select-Object -First 1
}

function Build-Payload {
  param(
    [string]$ModelId,
    [bool]$Stream
  )
  $payload = @{
    model = $ModelId
    messages = @(
      @{
        role = "user"
        content = "Merhaba"
      }
    )
    temperature = 0.2
    top_p = 0.9
    max_tokens = 128
    stream = $Stream
  }
  return ($payload | ConvertTo-Json -Depth 6)
}

function Write-Report {
  param(
    [string]$Path
  )
  $dir = Split-Path -Path $Path -Parent
  if ($dir) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
  }

  $lines = @(
    "# Selcuk YZ Asistan Smoke Raporu",
    "",
    "Zaman: $(Get-Date -Format o)",
    "Taban URL: $BaseUrl",
    "Host: $env:COMPUTERNAME",
    "OS: $([System.Environment]::OSVersion)",
    "PowerShell: $($PSVersionTable.PSVersion)",
    "",
    "| Kontrol | Durum | Detay |",
    "| --- | --- | --- |"
  )

  foreach ($result in $script:results) {
    $detail = ($result.Detail -replace '\|', '/')
    $lines += "| $($result.Name) | $($result.Status) | $detail |"
  }

  Write-Utf8NoBom -Path $Path -Content ($lines -join "`n")
}

Write-Host "== Selcuk YZ Asistan smoke =="
Write-Host "Taban URL: $BaseUrl"

Write-Result "Ortam" $true "OS: $([System.Environment]::OSVersion)"

$health = Invoke-Curl @("-sS", "--max-time", "$TimeoutSec", "$BaseUrl/health")
$healthOk = $false
if ($health.ExitCode -eq 0) {
  try {
    $healthJson = $health.Output | ConvertFrom-Json
    $healthOk = $healthJson.status -eq "ok"
  } catch {
    $healthOk = $false
  }
}
Write-Result "GET /health" $healthOk (Truncate-Text $health.Output)

$ollama = Invoke-Curl @("-sS", "--max-time", "$TimeoutSec", "$BaseUrl/health/ollama")
$ollamaOk = $false
if ($ollama.ExitCode -eq 0) {
  try {
    $ollamaJson = $ollama.Output | ConvertFrom-Json
    $ollamaOk = ($ollamaJson.status -ne "unhealthy") -and ($ollamaJson.model_available -eq $true)
  } catch {
    $ollamaOk = $false
  }
}
Write-Result "GET /health/ollama" $ollamaOk (Truncate-Text $ollama.Output)

$hf = Invoke-Curl @("-sS", "--max-time", "$TimeoutSec", "$BaseUrl/health/hf")
$hfOk = $false
if ($hf.ExitCode -eq 0) {
  try {
    $hfJson = $hf.Output | ConvertFrom-Json
    $hfOk = -not [string]::IsNullOrWhiteSpace($hfJson.status)
  } catch {
    $hfOk = $false
  }
}
Write-Result "GET /health/hf" $hfOk (Truncate-Text $hf.Output)

$models = Invoke-Curl @("-sS", "--max-time", "$TimeoutSec", "$BaseUrl/models")
$modelsOk = $false
$modelsJson = $null
if ($models.ExitCode -eq 0) {
  try {
    $modelsJson = $models.Output | ConvertFrom-Json
    $count = @($modelsJson.models).Count
    $modelsOk = $count -ge 1
  } catch {
    $modelsOk = $false
  }
}
Write-Result "GET /models" $modelsOk (Truncate-Text $models.Output)

$tmpDir = Join-Path $PSScriptRoot ".tmp"
New-Item -ItemType Directory -Path $tmpDir -Force | Out-Null

$invalidBodyPath = Join-Path $tmpDir "payload_invalid.json"
Write-Utf8NoBom -Path $invalidBodyPath -Content '{ "foo": "bar" }'
$invalidBodyOut = Join-Path $tmpDir "payload_invalid_response.json"
$invalid = Invoke-Curl @(
  "-sS",
  "--max-time", "$TimeoutSec",
  "-H", "Content-Type: application/json",
  "-X", "POST",
  "$BaseUrl/chat",
  "--data-binary", "@$invalidBodyPath",
  "-o", "$invalidBodyOut",
  "-w", "%{http_code}"
)
$invalidCode = [regex]::Match($invalid.Output, '\d{3}').Value
$invalidOk = $false
if ($invalidCode) {
  $invalidOk = [int]$invalidCode -ge 400
}
$invalidBody = ""
if (Test-Path $invalidBodyOut) {
  $invalidBody = Get-Content -Path $invalidBodyOut -Raw
}
Write-Result "POST /chat (gecersiz payload)" $invalidOk "HTTP $invalidCode $(Truncate-Text $invalidBody)"

if (-not $modelsOk) {
  Write-Result "POST /chat (ollama)" $false "Atlandi: uygun model yok"
  Write-Result "POST /chat/stream (ollama)" $false "Atlandi: uygun model yok"
  Write-Result "POST /chat (hf)" $false "Atlandi: uygun model yok"
  Write-Result "POST /chat/stream (hf)" $false "Atlandi: uygun model yok"
  Write-Report -Path $ReportPath
  Write-Host "Rapor kaydedildi: $ReportPath"
  exit 1
}

$availableModels = @($modelsJson.models)
$ollamaModel = Require-Model -Models $availableModels -Provider "ollama" -PreferredIds @(
  "gemma2:2b",
  "mistral",
  "qwen2.5:7b",
  "llama3.1",
  "selcuk_ai_assistant",
  "selcuk-assistant"
)
$hfModel = Require-Model -Models $availableModels -Provider "huggingface" -PreferredIds @(
  "hf_qwen2_5_1_5b",
  "hf_phi3_mini"
)

if ($ollamaModel) {
  $ollamaPayload = Build-Payload -ModelId $ollamaModel.id -Stream:$false
  $ollamaPayloadPath = Join-Path $tmpDir "payload_ollama.json"
  Write-Utf8NoBom -Path $ollamaPayloadPath -Content $ollamaPayload

  $chat = Invoke-CurlWithRetry @(
    "-sS",
    "--max-time", "$TimeoutSec",
    "-H", "Content-Type: application/json",
    "-H", "Accept-Language: tr",
    "-X", "POST",
    "$BaseUrl/chat",
    "--data-binary", "@$ollamaPayloadPath"
  )
  $chatOk = $false
  if ($chat.ExitCode -eq 0) {
    try {
      $chatJson = $chat.Output | ConvertFrom-Json
      $chatOk = -not [string]::IsNullOrWhiteSpace($chatJson.answer)
    } catch {
      $chatOk = $false
    }
  }
  Write-Result "POST /chat (ollama: $($ollamaModel.id))" $chatOk (Truncate-Text $chat.Output)

  $ollamaStreamPayload = Build-Payload -ModelId $ollamaModel.id -Stream:$true
  $ollamaStreamPath = Join-Path $tmpDir "payload_ollama_stream.json"
  Write-Utf8NoBom -Path $ollamaStreamPath -Content $ollamaStreamPayload

  $stream = Invoke-CurlWithRetry @(
    "-sS",
    "-N",
    "--max-time", "$TimeoutSec",
    "-H", "Content-Type: application/json",
    "-H", "Accept-Language: tr",
    "-X", "POST",
    "$BaseUrl/chat/stream",
    "--data-binary", "@$ollamaStreamPath"
  )

  $streamText = $stream.Output
  $hasToken = $streamText -match '"type"\s*:\s*"token"'
  $hasEnd = $streamText -match '"type"\s*:\s*"end"'
  $hasError = $streamText -match '"type"\s*:\s*"error"'
  $streamOk = ($hasToken -or $hasEnd) -and (-not $hasError)
  Write-Result "POST /chat/stream (ollama: $($ollamaModel.id))" $streamOk (Truncate-Text $streamText)
} else {
  Write-Result "Ollama modeli secimi" $false "/models icinde uygun ollama modeli yok"
}

if ($hfModel) {
  $hfPayload = Build-Payload -ModelId $hfModel.id -Stream:$false
  $hfPayloadPath = Join-Path $tmpDir "payload_hf.json"
  Write-Utf8NoBom -Path $hfPayloadPath -Content $hfPayload

  $chat = Invoke-CurlWithRetry @(
    "-sS",
    "--max-time", "$TimeoutSec",
    "-H", "Content-Type: application/json",
    "-H", "Accept-Language: tr",
    "-X", "POST",
    "$BaseUrl/chat",
    "--data-binary", "@$hfPayloadPath"
  )
  $chatOk = $false
  if ($chat.ExitCode -eq 0) {
    try {
      $chatJson = $chat.Output | ConvertFrom-Json
      $chatOk = -not [string]::IsNullOrWhiteSpace($chatJson.answer)
    } catch {
      $chatOk = $false
    }
  }
  Write-Result "POST /chat (hf: $($hfModel.id))" $chatOk (Truncate-Text $chat.Output)

  $hfStreamPayload = Build-Payload -ModelId $hfModel.id -Stream:$true
  $hfStreamPath = Join-Path $tmpDir "payload_hf_stream.json"
  Write-Utf8NoBom -Path $hfStreamPath -Content $hfStreamPayload

  $stream = Invoke-CurlWithRetry @(
    "-sS",
    "-N",
    "--max-time", "$TimeoutSec",
    "-H", "Content-Type: application/json",
    "-H", "Accept-Language: tr",
    "-X", "POST",
    "$BaseUrl/chat/stream",
    "--data-binary", "@$hfStreamPath"
  )

  $streamText = $stream.Output
  $hasToken = $streamText -match '"type"\s*:\s*"token"'
  $hasEnd = $streamText -match '"type"\s*:\s*"end"'
  $hasError = $streamText -match '"type"\s*:\s*"error"'
  $streamOk = ($hasToken -or $hasEnd) -and (-not $hasError)
  Write-Result "POST /chat/stream (hf: $($hfModel.id))" $streamOk (Truncate-Text $streamText)
} else {
  Write-Result "HuggingFace modeli secimi" $false "/models icinde uygun huggingface modeli yok"
}

Write-Report -Path $ReportPath
Write-Host "Rapor kaydedildi: $ReportPath"

if ($script:failures -gt 0) {
  Write-Host "FAILED: $script:failures kontrol basarisiz."
  exit 1
}

Write-Host "Tum kontroller basarili."
