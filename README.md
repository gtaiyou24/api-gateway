# 🔌 API Gateway

[システムアーキテクチャ図](./infrastructure/SYSTEM_ARCHITECTURE.md)

<details><summary><b>🌏 インフラを構築する</b></summary>

事前に [Google Cloud のコンソール画面](https://console.cloud.google.com/welcome) にてプロジェクトを作成してください。プロジェクトを作成したら、以下の作業を行なってください。

- `infrastructure/terraform/gcp/environments/production/terraform.tfvars` に情報を記載してください。
- [お支払い画面](https://console.cloud.google.com/billing/linkedaccount) にて請求先アカウントをリンクしてください。

システムを構築するにあたり、ローカル PC にて Google 認証を完了させてください。
```bash
# Google Cloud SDK と Google アカウントを連携させる
gcloud auth login

# プロジェクトを確認
gcloud projects list

# プロジェクトを変更する
gcloud config set project {PROJECT_ID}
```

最後に Terraform を実行し、システムを構築してください。
```bash
# 適切な環境フォルダを選択してください
cd ./infrastructure/terraform/gcp/environments/production

terraform init  # 初めて実行する場合のみ初期化する
terraform plan  # 定義内容のチェック

terraform apply -auto-approve  # インフラを構築
```

システムを削除する場合は以下のコマンドを実行してください。
```bash
terraform destroy
```

</details>
