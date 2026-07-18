# FieldRise AI社員 連携ルール

本文書は、COO（Manus）・CTO（ChatGPT）・Automation担当（GitHub Actions）がFieldRiseリポジトリを介して連携するための運用ルールを定めるものです。最終的な判断と責任は常に社長が担い、AI社員はそのための情報整理・実行・提案を行います。

## 1. 連携の基本原則

すべてのAI社員間の情報の受け渡しは、原則としてこのリポジトリ上のMarkdownファイルを通じて行います。ファイルとして残すことで、誰がいつ何を依頼し、どのような回答が得られたかが履歴（コミットログ）として自動的に記録され、後から検証・改善できるようになります。

## 2. COO → CTO への依頼（cto/inbox/）

COO（Manus）がCTO（ChatGPT）に技術相談や設計レビューを依頼する場合、`cto/inbox/` に依頼書を作成します。

| 項目 | ルール |
|---|---|
| ファイル名 | `YYYY-MM-DD_件名.md`（例: `2026-07-18_ai-secretary-architecture.md`） |
| 記載内容 | 背景、依頼内容、期待する成果物、期限、参考資料 |
| 渡し方 | 社長がChatGPTに該当ファイルのURL（本リポジトリはpublicのため閲覧可能）を渡す、または内容を貼り付ける |

## 3. CTO → COO への回答（cto/outbox/）

ChatGPTの回答・成果物は `cto/outbox/` に保存します。ファイル名は対応するinboxの依頼書と同じ名前に `_reply` を付けます（例: `2026-07-18_ai-secretary-architecture_reply.md`）。保存は社長の貼り付け、またはCOOが代行します。

## 4. COO の報告（coo/reports/）

COO（Manus）は調査結果・作業報告を `coo/reports/` に `YYYY-MM-DD_件名.md` 形式で保存します。重要事項（リスク発見、規約変更、大きな成果）は、リポジトリへの保存と同時に社長へ直接報告します。

## 5. Automation担当（.github/workflows/）

定期実行や自動化はGitHub Actionsで行い、ワークフロー定義は `.github/workflows/` に、設計書・スクリプトは `automation/` に置きます。実行結果はリポジトリへのコミットまたはIssueとして記録します。

## 6. プロジェクト管理（projects/）

各プロジェクトは `projects/project-XXX-名前/` ディレクトリで管理します。各プロジェクトには `README.md`（目的・現状・次のアクション）を必ず置き、誰が見ても状況がわかる状態を保ちます。

## 7. 情報セキュリティ

本リポジトリは**public（公開）**です。以下を厳守します。

1. APIキー・パスワード・トークン・個人情報は絶対にコミットしない
2. 機密値はGitHub Secrets（Settings → Secrets and variables → Actions）で管理する
3. 売上の詳細数値など非公開情報を扱う必要が生じた場合は、リポジトリのprivate化を社長に提案する

## 8. トークン管理

COO（Manus）はFine-grained PAT「FieldRise-Manus-COO」（FieldRiseリポジトリ限定、有効期限30日）でアクセスします。期限が近づいた際は、COOが社長に更新を依頼します。
