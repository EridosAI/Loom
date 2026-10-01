$ErrorActionPreference = 'Stop'
$packetSource = 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02'
$packetInbox = 'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX'
$packetDestination = Join-Path $packetInbox '2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02'
$resolvedInbox = (Resolve-Path -LiteralPath $packetInbox).Path
$resolvedDestination = [System.IO.Path]::GetFullPath($packetDestination)
if (-not $resolvedDestination.StartsWith($resolvedInbox + '\', [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Destination outside exact inbox' }
if (Test-Path -LiteralPath $packetDestination) { throw 'Existing delivery must be preserved' }
$packetReceipt = Get-Content -LiteralPath (Join-Path $packetSource 'PACKAGE_RECEIPT.json') -Raw | ConvertFrom-Json
foreach ($packetSection in @('public', 'privileged')) {
    $packetArchive = Join-Path $packetSource $packetReceipt.$packetSection.archive
    if ((Get-FileHash -LiteralPath $packetArchive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $packetReceipt.$packetSection.sha256) { throw 'Source archive mismatch' }
}
New-Item -ItemType Directory -Path $packetDestination | Out-Null
Copy-Item -LiteralPath (Join-Path $packetSource 'B1_OPERATOR_REVIEW') -Destination $packetDestination -Recurse
foreach ($packetName in @('B1_OPERATOR_REVIEW.zip', 'B1_PRIVILEGED_EVALUATOR_HOLD.zip', 'README.md', 'PACKAGE_RECEIPT.json', 'POST_SEAL_FILE_AUDIT.json')) {
    Copy-Item -LiteralPath (Join-Path $packetSource $packetName) -Destination (Join-Path $packetDestination $packetName)
}
$deliveredFiles = @{}
foreach ($packetFile in Get-ChildItem -LiteralPath $packetDestination -File -Recurse) {
    $relativeName = $packetFile.FullName.Substring($packetDestination.Length + 1)
    $originalPath = Join-Path $packetSource $relativeName
    $copiedHash = (Get-FileHash -LiteralPath $packetFile.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($copiedHash -ne (Get-FileHash -LiteralPath $originalPath -Algorithm SHA256).Hash.ToLowerInvariant()) { throw 'Delivered file mismatch' }
    $deliveredFiles[$relativeName] = @{ bytes = $packetFile.Length; sha256 = $copiedHash }
}
if (Test-Path -LiteralPath (Join-Path $packetDestination 'B1_PRIVILEGED_EVALUATOR_HOLD')) { throw 'Privileged directory must not be expanded in the workbench' }
$delivery = [ordered]@{
    status = 'Verified file delivery only; no execution'
    destination = $packetDestination
    held_review_sha256 = $packetReceipt.held_review_sha256
    copied_files = $deliveredFiles
    privileged_expanded_in_workbench = $false
    git_operations = 0
    navigation_or_canon_edits = 0
    simulation_steps = 0
    controller_calls = 0
}
$deliveryText = $delivery | ConvertTo-Json -Depth 8
[System.IO.File]::WriteAllText((Join-Path $packetDestination 'DELIVERY_RECEIPT.json'), $deliveryText + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
[System.IO.File]::WriteAllText((Join-Path $packetSource 'DELIVERY_RECEIPT.json'), $deliveryText + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
[ordered]@{ destination = $packetDestination; copied_files_verified = $deliveredFiles.Count; review_sha256 = $packetReceipt.held_review_sha256; privileged_archive_only = $true; no_execution = $true } | ConvertTo-Json
