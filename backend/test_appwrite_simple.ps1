# Appwrite Connection Test Script
Write-Host "Testing Appwrite Connection..." -ForegroundColor Cyan

$headers = @{
    "X-Appwrite-Project" = "69407f8200300e7093d8"
    "X-Appwrite-Key" = "standard_26cd773293db96c9c9552975851221c90042f4f188c1daef00fb988dd823af265af7ebe768bc4e6fa4df64faff9aead5d93fe7fb8f1a776949e84ae913cecd0c453b6f52ee028e216adb5f98bccca9ee078a8f2f28a907e60cbb8d921f05f4b3099bf37ee1cdc4406f80220d4319b65297dc8458d296429bad14ac3d6c40c7ce"
    "Content-Type" = "application/json"
}

$randomId = "test_$( Get-Random -Minimum 1000 -Maximum 9999 )"

$body = @{
    documentId = $randomId
    data = @{
        question = "Test question - Appwrite working?"
        answer = "Test answer - Yes, working successfully!"
        timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
    }
} | ConvertTo-Json

Write-Host "Sending test document..." -ForegroundColor Yellow
Write-Host "Document ID: $randomId" -ForegroundColor Gray

try
{
    $response = Invoke-WebRequest -Uri "https://fra.cloud.appwrite.io/v1/databases/694083cb0031903b17d5/collections/chat_logs/documents" -Method POST -Headers $headers -Body $body -ErrorAction Stop

    if ($response.StatusCode -eq 201)
    {
        Write-Host "SUCCESS! Appwrite connection working!" -ForegroundColor Green
        Write-Host "Status Code: $( $response.StatusCode )" -ForegroundColor Green
        Write-Host "Document ID: $randomId" -ForegroundColor Green
        Write-Host ""
        Write-Host "Check: https://fra.cloud.appwrite.io/console" -ForegroundColor Cyan
        Write-Host "Databases > chat_logs > Documents" -ForegroundColor Blue
    }
}
catch
{
    Write-Host "ERROR! Appwrite connection failed!" -ForegroundColor Red
    Write-Host "Error: $( $_.Exception.Message )" -ForegroundColor Red

    if ($_.Exception.Response)
    {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Detail: $responseBody" -ForegroundColor Red
    }

    Write-Host ""
    Write-Host "Solutions:" -ForegroundColor Yellow
    Write-Host "1. Check permissions (Create: Any)" -ForegroundColor White
    Write-Host "2. Verify API Key" -ForegroundColor White
    Write-Host "3. Verify Database/Collection ID" -ForegroundColor White
}

