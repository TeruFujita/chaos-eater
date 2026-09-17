param(
    [string]$Mode = "C4",
    [string]$Config = "pipeline_v0/configs/nginx.yaml"
)
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "../.."))
python -m pipeline_v0 --config $Config --mode $Mode
