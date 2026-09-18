param(
    [string]$Config = "pipeline_v0/configs/nginx.yaml",
    [string]$Mode = "C3"
)
# Critical path: fixed deploy + verify + inject + verify (LLM=None). Needs kind + Chaos Mesh.
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "../.."))
Write-Host "Running critical path mode=$Mode config=$Config"
python -m pipeline_v0 --config $Config --mode $Mode --execute
