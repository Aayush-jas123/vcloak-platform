$headers = @{
    "Authorization" = "token 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"
    "Accept" = "application/vnd.github.v3+json"
}

$body = @{
    name = "vcloak"
    description = "Secure luggage storage platform connecting travelers with local storage providers"
    private = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
