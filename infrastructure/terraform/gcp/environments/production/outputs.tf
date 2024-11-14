output "load_balancer_ip" {
  value = module.load_balancing.load_balancer_ip
  description = "ロードバランサーの IP アドレス。この IP アドレスをドメインの DNS レコードに指定してください。"
}