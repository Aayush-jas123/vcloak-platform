$headers = @{
    "Authorization" = "token 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"
    "Accept"        = "application/vnd.github.v3+json"
}

# Delete old repository
try {
    Invoke-RestMethod -Uri "https://api.github.com/repos/Aayush-jas123/vcloak" -Method Delete -Headers $headers
    Write-Host "Old repository deleted"
}
catch {
    Write-Host "Repository may not exist or already deleted"
}

Start-Sleep -Seconds 2

# Create new repository
$body = @{
    name        = "vcloak"
    description = "Secure luggage storage platform connecting travelers with local storage providers"
    private     = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
