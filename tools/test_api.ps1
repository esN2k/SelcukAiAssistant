param(
  [string]$BaseUrl = "http://localhost:8000",
  [int]$TimeoutSec = 60
)

$ErrorActionPreference = "Stop"
$script:failures = 0
$curl = (Get-Command curl.exe -ErrorAction Stop).Source

$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding  = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

function Write-Result {
  param(
    [string]$Name,
    [bool]$Ok,
    [string]$Detail = ""
  )
  if ($Ok) {
    Write-Host "PASS: $Name"
    return
  }
  $script:failures++
  if ([string]::IsNullOrWhiteSpace($Detail)) {
    Write-Host "FAIL: $Name"
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

Write-Host "== Selcuk YZ Asistan API smoke =="
Write-Host "Taban URL: $BaseUrl"

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

if (-not $modelsOk) {
  Write-Host "/chat ve /chat/stream atlandi (uygun model yok)."
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

if (-not $ollamaModel) {
  Write-Result "Ollama modeli secimi" $false "/models icinde uygun ollama modeli yok"
}
if (-not $hfModel) {
  Write-Result "HuggingFace modeli secimi" $false "/models icinde uygun huggingface modeli yok"
}

$tmpDir = Join-Path $PSScriptRoot ".tmp"
New-Item -ItemType Directory -Path $tmpDir -Force | Out-Null

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
  Write-Host "SSE ornek (ollama):"
  ($streamText -split "`r?`n" | Where-Object { $_ -ne "" } | Select-Object -First 20) | ForEach-Object { Write-Host $_ }
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
  Write-Host "SSE ornek (hf):"
  ($streamText -split "`r?`n" | Where-Object { $_ -ne "" } | Select-Object -First 20) | ForEach-Object { Write-Host $_ }
}

if ($script:failures -gt 0) {
  Write-Host "FAILED: $script:failures kontrol basarisiz."
  exit 1
}

Write-Host "Tum kontroller basarili."
