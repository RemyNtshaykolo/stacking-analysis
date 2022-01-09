locals {
  secrets          = jsondecode(data.aws_secretsmanager_secret_version.secrets.secret_string)
  bsc_scan_api_key = local.secrets["bsc_scan_api_key"]

}
