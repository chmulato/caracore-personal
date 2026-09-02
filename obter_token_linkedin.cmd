@echo off
setlocal

rem Troca o codigo OAuth por um Access Token do LinkedIn.
rem Os valores sensiveis sao digitados nos prompts do PowerShell e nao aparecem
rem como argumentos deste comando.

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference = 'Stop'; try { $clientId = Read-Host 'Client ID'; $clientSecretSecure = Read-Host 'Client Secret (nao sera exibido)' -AsSecureString; $codeSecure = Read-Host 'Codigo OAuth (nao sera exibido)' -AsSecureString; $personId = Read-Host 'ID pessoal do LinkedIn'; $secretPtr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($clientSecretSecure); $clientSecret = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($secretPtr); $codePtr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($codeSecure); $code = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($codePtr); if ([string]::IsNullOrWhiteSpace($clientId) -or [string]::IsNullOrWhiteSpace($clientSecret) -or [string]::IsNullOrWhiteSpace($code)) { throw 'Client ID, Client Secret e Codigo OAuth sao obrigatorios. Digite os campos protegidos mesmo que nada apareca na tela.' }; $body = @{ grant_type = 'authorization_code'; code = $code; redirect_uri = 'http://localhost:8000/callback'; client_id = $clientId; client_secret = $clientSecret }; try { $response = Invoke-RestMethod -Method Post -Uri 'https://www.linkedin.com/oauth/v2/accessToken' -ContentType 'application/x-www-form-urlencoded' -Body $body } catch { $errorResponse = $_.Exception.Response; if ($null -ne $errorResponse) { $reader = New-Object IO.StreamReader($errorResponse.GetResponseStream()); $details = $reader.ReadToEnd(); throw ('LinkedIn HTTP ' + [int]$errorResponse.StatusCode + ': ' + $details) }; throw }; if ([string]::IsNullOrWhiteSpace($response.access_token)) { throw 'O LinkedIn nao retornou access_token.' }; @('ACCESS_TOKEN=' + $response.access_token, 'PERSON_ID=' + $personId) | Set-Content -Path 'token.txt' -Encoding UTF8; [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($secretPtr); [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($codePtr); Write-Host 'Access Token salvo em token.txt com sucesso.' } catch { Write-Error ('Falha ao obter o token: ' + $_.Exception.Message); exit 1 }"

if errorlevel 1 (
    echo A troca OAuth falhou. O token.txt nao foi atualizado.
    exit /b 1
)

endlocal
