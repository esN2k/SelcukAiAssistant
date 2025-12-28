param(
  [string]$BaseUrl = "http://localhost:8000",
  [int]$TimeoutSec = 60,
  [switch]$AllowNoModel
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

function Write-Skipped {
  param(
    [string]$Name,
    [string]$Detail = ""
  )
  if ([string]::IsNullOrWhiteSpace($Detail)) {
    Write-Host "SKIP: $Name"
  } else {
    Write-Host "SKIP: $Name - $Detail"
  }
}

function Limit-Text {
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

function Format-Argument {
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

  $argsString = ($CurlArgs | ForEach-Object { Format-Argument $_ }) -join ' '

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

function Get-Model {
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

Write-Host "== Selçuk AI Asistanı API smoke testi =="
Write-Host "Taban URL: $BaseUrl"

$health = Invoke-Curl @("-sS", "--max-time", "$TimeoutSec", "$BaseUrl/health")
$healthOk = $false
$healthMessage = ""
if ($health.ExitCode -eq 0) {
  try {
    $healthJson = $health.Output | ConvertFrom-Json
    $healthOk = $healthJson.status -eq "ok"
    $healthMessage = $healthJson.message
  } catch {
    $healthOk = $false
  }
}
Write-Result "GET /health" $healthOk (Limit-Text $health.Output)

$encodingOk = $false
if (-not [string]::IsNullOrWhiteSpace($healthMessage)) {
  $containsTurkish = $healthMessage -match '[çğıİöşüÇĞİÖŞÜ]'
  $containsMojibake = $healthMessage -match '[\u00C3\u00C5\u00C4\u00C2\u00D0\u00DE\uFFFD]'
  $encodingOk = $containsTurkish -and (-not $containsMojibake)
}
Write-Result "UTF-8/Türkçe karakter kontrolü" $encodingOk (Limit-Text $healthMessage)

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
Write-Result "GET /models" $modelsOk (Limit-Text $models.Output)

if (-not $modelsOk) {
  Write-Host "/chat ve /chat/stream atlandı (uygun model yok)."
  if (-not $AllowNoModel) {
    exit 1
  }
}

$availableModels = @($modelsJson.models)
$ollamaModel = Get-Model -Models $availableModels -Provider "ollama" -PreferredIds @(
  "gemma2:2b",
  "mistral",
  "qwen2.5:7b",
  "llama3.1",
  "selcuk_ai_assistant",
  "selcuk-assistant"
)
$hfModel = Get-Model -Models $availableModels -Provider "huggingface" -PreferredIds @(
  "hf_qwen2_5_1_5b",
  "hf_phi3_mini"
)

if (-not $ollamaModel) {
  if ($AllowNoModel) {
    Write-Skipped "Ollama modeli seçimi" "/models içinde uygun ollama modeli yok"
  } else {
    Write-Result "Ollama modeli seçimi" $false "/models içinde uygun ollama modeli yok"
  }
}
if (-not $hfModel) {
  if ($AllowNoModel) {
    Write-Skipped "HuggingFace modeli seçimi" "/models içinde uygun huggingface modeli yok"
  } else {
    Write-Result "HuggingFace modeli seçimi" $false "/models içinde uygun huggingface modeli yok"
  }
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
  Write-Result "POST /chat (ollama: $($ollamaModel.id))" $chatOk (Limit-Text $chat.Output)

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
  Write-Result "POST /chat/stream (ollama: $($ollamaModel.id))" $streamOk (Limit-Text $streamText)
  Write-Host "SSE örnek (ollama):"
  ($streamText -split "`r?`n" | Where-Object { $_ -ne "" } | Select-Object -First 20) | ForEach-Object { Write-Host $_ }
} elseif ($AllowNoModel) {
  Write-Skipped "POST /chat (ollama)" "Uygun model yok"
  Write-Skipped "POST /chat/stream (ollama)" "Uygun model yok"
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
  Write-Result "POST /chat (hf: $($hfModel.id))" $chatOk (Limit-Text $chat.Output)

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
  Write-Result "POST /chat/stream (hf: $($hfModel.id))" $streamOk (Limit-Text $streamText)
  Write-Host "SSE örnek (hf):"
  ($streamText -split "`r?`n" | Where-Object { $_ -ne "" } | Select-Object -First 20) | ForEach-Object { Write-Host $_ }
} elseif ($AllowNoModel) {
  Write-Skipped "POST /chat (hf)" "Uygun model yok"
  Write-Skipped "POST /chat/stream (hf)" "Uygun model yok"
}

if ($script:failures -gt 0) {
  Write-Host "BAŞARISIZ: $script:failures kontrol başarısız."
  exit 1
}

Write-Host "Tüm kontroller başarılı."
